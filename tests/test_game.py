import copy
import json
import tempfile
import unittest
from pathlib import Path
from game import SindicoGame
from lore import PERFIS, MELHORIAS, PROPOSTAS


class MandatoTests(unittest.TestCase):
    def evento(self, g, categoria):
        e = copy.deepcopy(next(e for e in g.todos_eventos if e['categoria'] == categoria))
        e.update(ticket='teste', abertura=g.dia, tipo_evento='normal')
        g.evento_atual = e
        return e

    def test_sorteio_reproduzivel_com_seed_e_diverso_sem_seed_fixa(self):
        self.assertEqual(SindicoGame(seed=23).evento_atual['id'], SindicoGame(seed=23).evento_atual['id'])
        starts = {SindicoGame(seed=s).evento_atual['id'] for s in range(30)}
        self.assertGreater(len(starts), 12)

    def test_novo_mandato_evitar_mesmo_primeiro_evento(self):
        primeiro = SindicoGame(seed=4).evento_atual['id']
        self.assertNotEqual(primeiro, SindicoGame(seed=4, evitar_inicio=primeiro).evento_atual['id'])

    def test_atualizar_opcoes_nao_refaz_sorteio(self):
        g = SindicoGame(seed=1)
        state, event = g.rng.getstate(), copy.deepcopy(g.evento_atual)
        for _ in range(10):
            g.opcoes_evento(g.evento_atual)
        self.assertEqual(event, g.evento_atual)
        self.assertEqual(state, g.rng.getstate())

    def test_responder_uma_vez_nao_reabre_pendencia(self):
        g = SindicoGame(seed=1)
        event = g.evento_atual
        g.responder_evento(event, 0)
        saldo = g.caixa
        g.responder_evento(event, 0)
        self.assertEqual(g.caixa, saldo)
        g.avancar_dia()
        self.assertFalse(g.pendencias)

    def test_memoria_afeta_votos(self):
        g = SindicoGame(seed=1)
        g.aprovacao = 40
        event = copy.deepcopy(g.evento_atual)
        event['remetente'] = 'Beto (401)'
        g.evento_atual = event
        p = PROPOSTAS['ordinaria'][2]
        antes = next(v for v in g.prever_votos(p) if v['nome'] == 'Beto (401)')
        g.responder_evento(event, 1)
        depois = next(v for v in g.prever_votos(p) if v['nome'] == 'Beto (401)')
        self.assertTrue(antes['sim'])
        self.assertFalse(depois['sim'])
        self.assertGreater(g.moradores['Beto (401)']['irritacao'], 0)

    def test_conversar_repara_memoria_so_uma_vez_por_dia(self):
        g = SindicoGame(seed=1)
        nome = next(iter(PERFIS))
        g.moradores[nome].update(confianca=20, irritacao=60)
        g.reconciliar(nome)
        self.assertEqual(g.moradores[nome]['confianca'], 35)
        self.assertEqual(g.moradores[nome]['irritacao'], 42)
        saldo = g.caixa
        g.reconciliar(nome)
        self.assertEqual(g.caixa, saldo)

    def test_cameras_desbloqueiam_opcao_e_reduzem_custo(self):
        g = SindicoGame(seed=1)
        event = self.evento(g, 'seguranca')
        self.assertEqual(len(g.opcoes_evento(event)), 4)
        original = g.impacto_opcao(event, g.opcoes_evento(event)[0])['caixa']
        self.assertTrue(g.comprar_cameras())
        self.assertEqual(len(g.opcoes_evento(event)), 5)
        self.assertEqual(g.impacto_opcao(event, g.opcoes_evento(event)[0])['caixa'], round(original*.5))
        self.assertEqual(g.opcoes_evento(event)[4]['tipo'], 'melhoria')

    def test_todas_melhorias_tem_efeito_e_compra_nao_repete(self):
        for key, spec in MELHORIAS.items():
            g = SindicoGame(seed=1)
            g.caixa = 10000
            self.evento(g, spec['categoria'][0])
            self.assertTrue(g.comprar_melhoria(key))
            self.assertEqual(len(g.opcoes_evento(g.evento_atual)), 5)
            saldo = g.caixa
            self.assertFalse(g.comprar_melhoria(key))
            self.assertEqual(g.caixa, saldo)
            self.assertEqual(g.custo_mensal, 9000+spec['mensal'])

    def test_plano_preventivo_reduz_desgaste(self):
        g = SindicoGame(seed=1)
        event = self.evento(g, 'manutencao')
        g.comprar_melhoria('manutencao')
        impacto = g.impacto_opcao(event, g.opcoes_evento(event)[0])
        self.assertGreaterEqual(impacto['paciencia'], 0)

    def test_descansar_uma_vez_por_dia(self):
        g = SindicoGame(seed=1)
        g.paciencia = 30
        g.descansar()
        self.assertEqual((g.caixa, g.paciencia), (4820, 44))
        g.descansar()
        self.assertEqual((g.caixa, g.paciencia), (4820, 44))
        g.responder_evento(g.evento_atual, 0)
        g.avancar_dia()
        self.assertFalse(g.descanso_dia)

    def test_delegar_pendencia_sem_afetar_chamado_atual(self):
        g = SindicoGame(seed=1)
        g.avancar_dia()
        atual = g.evento_atual
        g.delegar()
        self.assertFalse(g.pendencias)
        self.assertIs(g.evento_atual, atual)
        self.assertFalse(g.encerrado)
        saldo = g.caixa
        g.delegar()
        self.assertEqual(g.caixa, saldo)

    def test_portaria_reduz_custo_da_delegacao(self):
        g = SindicoGame(seed=1)
        g.comprar_melhoria('portaria')
        saldo = g.caixa
        g.delegar()
        self.assertEqual(g.caixa, saldo-160)
        self.assertTrue(g.encerrado)

    def crise(self):
        g = SindicoGame(seed=1)
        g.responder_evento(g.evento_atual, 3)
        for _ in range(3):
            g.avancar_dia()
            if not g.encerrado and g.dia < 4:
                g.responder_evento(g.evento_atual, 0)
        return g

    def test_conselho_abre_crise_com_nova_decisao(self):
        g = self.crise()
        crise = g.evento_foco
        self.assertEqual(crise['tipo_evento'], 'crise')
        self.assertEqual(crise['etapa'], 1)
        self.assertEqual(crise['prazo'], 6)
        self.assertEqual(len(g.opcoes_evento(crise)), 3)
        saldo = g.caixa
        g.responder_evento(crise, 0)
        self.assertLess(g.caixa, saldo)
        self.assertFalse(g.pendencias)
        self.assertFalse(g.encerrado)

    def test_segunda_gambiarra_abre_ultima_etapa(self):
        g = self.crise()
        g.responder_evento(g.evento_foco, 2)
        for _ in range(2):
            g.responder_evento(g.evento_atual, 0)
            g.avancar_dia()
        crise = g.evento_foco
        self.assertEqual(crise['etapa'], 2)
        self.assertEqual(len(g.opcoes_evento(crise)), 2)
        self.assertFalse(any(o.get('agravar') for o in crise['opcoes']))

    def test_crise_ignorada_tem_reparo_emergencial(self):
        g = self.crise()
        for _ in range(3):
            g.responder_evento(g.evento_atual, 0)
            g.avancar_dia()
        self.assertFalse(any(e.get('tipo_evento') == 'crise' for e in g.pendencias))
        self.assertTrue(any('Prazo perdido' in h['texto'] for h in g.historico))

    def test_assembleia_mensal_e_cobranca_uma_vez(self):
        g = SindicoGame(seed=1)
        g.dia, g.encerrado = 30, True
        g.avancar_dia()
        self.assertEqual(g.caixa, 6800)
        self.assertEqual(g.assembleia['tipo'], 'ordinaria')
        g.avancar_dia()
        self.assertEqual(g.dia, 31)
        g.votar(0)
        self.assertIsNone(g.assembleia)
        saldo = g.caixa
        g.responder_evento(g.evento_atual, 0)
        custo = g.caixa
        g.avancar_dia()
        self.assertEqual(g.caixa, custo)
        self.assertEqual(g.ultima_votacao['total'], 8)

    def test_revolta_convoca_e_rejeicao_destitui(self):
        g = SindicoGame(seed=1)
        for _ in range(3):
            g.aprovacao, g.encerrado = 0, True
            g.avancar_dia()
        self.assertEqual(g.assembleia['tipo'], 'crise')
        for estado in g.moradores.values():
            estado.update(confianca=0, irritacao=100)
        g.votar(2)
        self.assertFalse(g.jogo_ativo)
        self.assertEqual(g.fim_motivo, 'destituicao')

    def test_so_debochar_nao_vence_mais(self):
        g = SindicoGame(seed=1)
        for _ in range(500):
            if not g.jogo_ativo:
                break
            if g.assembleia:
                g.votar(2)
            else:
                g.responder_evento(g.evento_atual, 1)
                g.avancar_dia()
        self.assertFalse(g.vitoria)
        self.assertFalse(g.jogo_ativo)

    def test_mandato_365_dias_viavel_com_diplomacia_e_descanso(self):
        g = SindicoGame(seed=1)
        for _ in range(800):
            if not g.jogo_ativo:
                break
            if g.assembleia:
                g.votar(0)
            else:
                if g.paciencia < 70:
                    g.descansar()
                g.responder_evento(g.evento_atual, 0)
                g.avancar_dia()
        self.assertTrue(g.vitoria, (g.dia, g.caixa, g.paciencia, g.fim_motivo))
        self.assertEqual(g.dia, 365)
        self.assertEqual(len(g.vistos), 365)
        self.assertEqual(len(set(g.vistos)), 365)

    def test_save_preserva_sorteio_memoria_e_limites_diarios(self):
        g = SindicoGame(seed=22)
        g.paciencia = 70
        g.descansar()
        g.responder_evento(g.evento_atual, 1)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'mandato.json'
            g.salvar(path)
            novo = SindicoGame(seed=900)
            novo.carregar(path)
            self.assertEqual(novo.evento_atual, g.evento_atual)
            self.assertEqual(novo.moradores, g.moradores)
            self.assertTrue(novo.descanso_dia)
            g.avancar_dia()
            novo.avancar_dia()
            self.assertEqual(novo.evento_atual, g.evento_atual)

    def test_save_antigo_mantem_chamado_e_migra_indicadores(self):
        g = SindicoGame(seed=1)
        campos = ('dia', 'caixa', 'paciencia', 'aprovacao', 'pendencias', 'consequencias',
                  'historico', 'jogo_ativo', 'vitoria', 'encerrado', 'evento_atual')
        old = {k: copy.deepcopy(getattr(g, k)) for k in campos}
        old.update(tem_cameras=True, dia=90)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'mandato.json'
            path.write_text(json.dumps(old), encoding='utf-8')
            novo = SindicoGame(seed=2)
            novo.carregar(path)
            self.assertEqual(novo.evento_atual, old['evento_atual'])
            self.assertTrue(novo.tem_cameras)
            self.assertEqual(novo.dia, 90)
            self.assertEqual(novo.caixa, old['caixa'])

    def test_save_invalido_nao_altera_partida(self):
        g = SindicoGame(seed=3)
        before = copy.deepcopy(g.evento_atual)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'mandato.json'
            path.write_text('{"dia": 90}', encoding='utf-8')
            with self.assertRaises(ValueError):
                g.carregar(path)
            self.assertEqual(g.evento_atual, before)
            self.assertEqual(g.dia, 1)

    def test_derrota_por_caixa_e_paciencia_continua_existindo(self):
        for campo, valor in [('caixa', -1), ('paciencia', 0)]:
            g = SindicoGame(seed=1)
            setattr(g, campo, valor)
            g.verificar_status_jogo()
            self.assertFalse(g.jogo_ativo)
            dia = g.dia
            g.avancar_dia()
            self.assertEqual(g.dia, dia)


if __name__ == '__main__':
    unittest.main()
