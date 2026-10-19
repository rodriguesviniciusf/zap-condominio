import calendar
import unittest
from game import SindicoGame
from calendar_content import MONTHS


class CalendarTests(unittest.TestCase):
    def test_banco_completo_365_historias_e_1460_escolhas(self):
        events = SindicoGame(seed=1).todos_eventos
        self.assertEqual(len(events), 365)
        self.assertEqual(sorted(e['dia'] for e in events), list(range(1, 366)))
        for field in ('id', 'titulo', 'mensagem', 'conselheiro_pitaco'):
            self.assertEqual(len({e[field] for e in events}), 365)
        self.assertEqual(sum(len(e['opcoes']) for e in events), 1460)

    def test_meses_tem_quantidade_correta(self):
        events = SindicoGame(seed=1).todos_eventos
        for month in range(1, 13):
            self.assertEqual([e['dia_mes'] for e in events if e['mes'] == month],
                             list(range(1, calendar.monthrange(2027, month)[1]+1)))

    def test_sorteio_respeita_tema_e_nao_repete_ao_longo_do_ano(self):
        g = SindicoGame(seed=19)
        g.vistos = []
        ids = []
        for day in range(1, 366):
            g.dia = day
            event = g._sortear_evento()
            self.assertEqual(event['dia'], day)
            original = next(e for e in g.todos_eventos if e['id'] == event['id'])
            self.assertEqual(original['mes'], event['mes'])
            ids.append(event['id'])
        self.assertEqual(len(set(ids)), 365)

    def test_fontes_editoriais_completas(self):
        self.assertEqual(sum(m[2] for m in MONTHS), 365)
        self.assertEqual(sum(len([l for l in m[3].splitlines() if l.strip()]) for m in MONTHS), 353)


if __name__ == '__main__':
    unittest.main()
