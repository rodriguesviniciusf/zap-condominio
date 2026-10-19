import json
import tempfile
import unittest
from pathlib import Path
from game import SindicoGame


class MandatoTests(unittest.TestCase):
    def test_banco_completo(self):
        eventos = SindicoGame().todos_eventos
        self.assertGreaterEqual(len(eventos), 10)
        self.assertEqual(len({e['id'] for e in eventos}), len(eventos))
        for evento in eventos:
            self.assertEqual(len(evento['opcoes']), 4)
            self.assertIn('consequencia', evento['opcoes'][3])

    def test_resolvido_nao_vira_pendencia_nem_paga_duas_vezes(self):
        g = SindicoGame(seed=1)
        evento = g.evento_atual
        g.responder_evento(evento, 2)
        caixa = g.caixa
        g.responder_evento(evento, 2)
        self.assertEqual(g.caixa, caixa)
        g.avancar_dia()
        self.assertEqual(g.pendencias, [])
        self.assertEqual(g.dia, 2)

    def test_adiar_e_resolver_chamado(self):
        g = SindicoGame(seed=1)
        g.avancar_dia()
        self.assertEqual(len(g.pendencias), 1)
        atual = g.evento_atual
        g.responder_evento(g.pendencias[0], 0)
        self.assertEqual(g.pendencias, [])
        self.assertIs(g.evento_atual, atual)
        self.assertFalse(g.encerrado)

    def test_sorteio_estavel_ao_atualizar_tela(self):
        g = SindicoGame(seed=1)
        g.dia = 20
        g.evento_atual = g._sortear_evento()
        evento = g.evento_atual
        g.comprar_cameras()
        self.assertIs(g.evento_atual, evento)

    def test_conselho_tem_efeito_tres_dias_depois(self):
        g = SindicoGame(seed=1)
        g.responder_evento(g.evento_atual, 3)
        for _ in range(2):
            g.avancar_dia()
            g.responder_evento(g.evento_atual, 0)
        self.assertEqual(len(g.consequencias), 1)
        g.avancar_dia()
        self.assertEqual(g.consequencias, [])
        self.assertTrue(any('coral' in h['texto'] for h in g.historico))

    def test_mensalidade_uma_vez_e_com_despesas(self):
        g = SindicoGame(seed=1)
        g.dia = 30
        g.encerrado = True
        g.avancar_dia()
        self.assertEqual(g.caixa, 6800)
        g.responder_evento(g.evento_atual, 1)
        g.avancar_dia()
        self.assertEqual(g.caixa, 6800)

    def test_cameras_reduzem_custo_de_seguranca(self):
        g = SindicoGame(seed=1)
        g.dia = 3
        g.evento_atual = g._sortear_evento()
        g.comprar_cameras()
        saldo = g.caixa
        g.responder_evento(g.evento_atual, 0)
        self.assertEqual(g.caixa, saldo - 30)

    def test_falencia_e_estresse_encerram_imediatamente(self):
        for atributo, valor in [('caixa', 0), ('paciencia', 1)]:
            g = SindicoGame(seed=1)
            setattr(g, atributo, valor)
            g.responder_evento(g.evento_atual, 0)
            self.assertFalse(g.jogo_ativo)
            g.avancar_dia()
            self.assertEqual(g.dia, 1)

    def test_vitoria_apenas_apos_365_dias(self):
        g = SindicoGame(seed=1)
        for dia in range(1, 366):
            self.assertEqual(g.dia, dia)
            self.assertFalse(g.vitoria)
            # Alterna recuperação de paciência e aprovação; finanças sustentáveis.
            opcao = 1 if g.paciencia < 80 else 0
            g.responder_evento(g.evento_atual, opcao)
            g.avancar_dia()
        self.assertTrue(g.vitoria)
        self.assertFalse(g.jogo_ativo)

    def test_save_preserva_chamados_e_consequencias(self):
        g = SindicoGame(seed=1)
        g.responder_evento(g.evento_atual, 3)
        g.avancar_dia()
        g.avancar_dia()
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / 'mandato.json'
            g.salvar(caminho)
            outro = SindicoGame()
            outro.carregar(caminho)
            self.assertEqual(outro.dia, g.dia)
            self.assertEqual(outro.consequencias, g.consequencias)
            self.assertEqual(outro.pendencias, g.pendencias)
            outro.responder_evento(outro.pendencias[0], 0)
            self.assertFalse(outro.pendencias)


if __name__ == '__main__':
    unittest.main()
