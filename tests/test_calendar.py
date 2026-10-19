import calendar
import json
import tempfile
import unittest
from pathlib import Path
from game import SindicoGame


class CalendarTests(unittest.TestCase):
    def test_um_evento_distinto_por_dia(self):
        events = SindicoGame().todos_eventos
        self.assertEqual(len(events), 365)
        self.assertEqual(sorted(e['dia'] for e in events), list(range(1, 366)))
        for field in ['id', 'titulo', 'mensagem', 'conselheiro_pitaco']:
            self.assertEqual(len({e[field] for e in events}), 365, field)
        for event in events:
            self.assertEqual([o['tipo'] for o in event['opcoes']], ['passiva', 'debochada', 'multa', 'conselho'])
            self.assertIn(event['conselheiro'], ['Seu Valdir', 'Dona Marlene', 'Toninho'])
            self.assertLess(event['opcoes'][3]['consequencia']['caixa'], 0)

    def test_calendario_de_janeiro_a_dezembro(self):
        events = SindicoGame().todos_eventos
        for month in range(1, 13):
            days = [e['dia_mes'] for e in events if e['mes'] == month]
            self.assertEqual(days, list(range(1, calendar.monthrange(2027, month)[1]+1)))

    def test_cada_dia_seleciona_seu_roteiro(self):
        g = SindicoGame()
        ids = []
        for day in range(1, 366):
            g.dia = day
            event = g._sortear_evento()
            self.assertEqual(event['dia'], day)
            self.assertEqual(event['abertura'], day)
            ids.append(event['id'])
        self.assertEqual(len(set(ids)), 365)

    def test_save_antigo_migra_o_dia_mas_preserva_pendencias(self):
        g = SindicoGame()
        old = dict(g.evento_atual)
        old.pop('titulo', None)
        g.pendencias = [old]
        g.dia = 90
        g.evento_atual = old
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'mandato.json'
            g.salvar(path)
            restored = SindicoGame()
            restored.carregar(path)
            self.assertEqual(restored.evento_atual['dia'], 90)
            self.assertEqual(restored.pendencias, [old])
            restored.responder_evento(restored.pendencias[0], 0)
            self.assertFalse(restored.pendencias)

    def test_roteiro_materializado_reproduzivel(self):
        from calendar_content import MONTHS
        self.assertEqual(sum(month[2] for month in MONTHS), 365)
        self.assertEqual(sum(len([r for r in month[3].splitlines() if r.strip()]) for month in MONTHS), 353)


if __name__ == '__main__':
    unittest.main()
