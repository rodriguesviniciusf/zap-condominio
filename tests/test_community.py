import copy
import json
import tempfile
import unittest
from pathlib import Path
from game import SindicoGame
from community import CASOS, PANELINHAS
from preferences import Preferencias


class CommunityTests(unittest.TestCase):
    def setUp(self):
        self.g = SindicoGame(seed=31)
        self.e = self.g.evento_atual
        self.e['investigacao'] = copy.deepcopy(CASOS[0])
        self.e['investigacao']['consultadas'] = []

    def test_pistas_custam_so_uma_vez_e_nao_usam_sorteio(self):
        estado = self.g.rng.getstate()
        caixa = self.g.caixa
        self.g.investigar(self.e, 0)
        self.g.investigar(self.e, 0)
        self.assertEqual(self.g.caixa, caixa-60)
        self.assertEqual(self.g.rng.getstate(), estado)
        self.g.melhorias['cameras'] = True
        self.assertEqual(self.g.custo_pista(0), 20)

    def test_duas_fontes_e_conclusao_correta_recompensam_so_uma_vez(self):
        self.g.investigar(self.e, 0)
        self.g.investigar(self.e, 1)
        apoio = self.g.aprovacao
        self.g.concluir_caso(self.e, 0)
        self.g.concluir_caso(self.e, 0)
        self.assertEqual(self.g.aprovacao, apoio+8)
        self.assertEqual(self.g.casos_resolvidos, 1)
        self.assertTrue(self.g.encerrado)

    def test_boato_nao_conta_como_segunda_prova(self):
        self.g.investigar(self.e, 0)
        self.g.investigar(self.e, 2)
        caixa = self.g.caixa
        self.g.concluir_caso(self.e, 0)
        self.assertEqual(self.g.caixa, caixa-200)
        self.assertEqual(self.g.casos_resolvidos, 0)

    def test_acusacao_errada_com_provas_exige_retratacao(self):
        self.g.investigar(self.e, 0)
        self.g.investigar(self.e, 1)
        self.g.concluir_caso(self.e, 1)
        self.assertEqual(self.g.aprovacao, 40)

    def test_arquivar_nao_acusa_nem_recompensa(self):
        self.g.concluir_caso(self.e, None)
        self.assertEqual(self.g.caixa, 5000)
        self.assertEqual(self.g.casos_resolvidos, 0)
        self.assertTrue(self.g.encerrado)

    def test_caso_pendente_resolve_sem_encerrar_atual(self):
        e = self.e
        self.g.avancar_dia()
        self.g.concluir_caso(e, None)
        self.assertNotIn(e, self.g.pendencias)
        self.assertFalse(self.g.encerrado)

    def test_assembleia_bloqueia_caso_e_mediacao(self):
        self.g.assembleia = dict(tipo='ordinaria')
        self.g.investigar(self.e, 0)
        self.g.concluir_caso(self.e, 0)
        self.g.mediar_grupo('sossego')
        self.assertEqual(self.g.caixa, 5000)
        self.assertFalse(self.g.encerrado)

    def test_multar_sem_apurar_nao_gera_receita(self):
        impacto = self.g.impacto_opcao(self.e, dict(tipo='multa', caixa_condominio=500))
        self.assertEqual(impacto, dict(caixa=-200, paciencia=-6, aprovacao=-10))

    def test_grupos_tem_interesses_opostos_e_influenciam_votos(self):
        self.g.atualizar_panelinhas('multa')
        self.assertGreater(self.g.panelinhas['sossego'], 50)
        self.assertLess(self.g.panelinhas['resenha'], 50)
        for m in self.g.moradores.values():
            m.update(confianca=50, irritacao=0)
        proposta = dict(apoio=0)
        self.g.panelinhas = dict.fromkeys(PANELINHAS, 0)
        contra = sum(v['sim'] for v in self.g.prever_votos(proposta))
        self.g.panelinhas = dict.fromkeys(PANELINHAS, 100)
        favor = sum(v['sim'] for v in self.g.prever_votos(proposta))
        self.assertGreater(favor, contra)

    def test_mediacao_diaria_tem_troca_e_limite(self):
        self.g.mediar_grupo('sossego')
        self.g.mediar_grupo('planilha')
        self.assertEqual(self.g.caixa, 4900)
        self.assertEqual(self.g.panelinhas['sossego'], 62)
        self.assertEqual(self.g.panelinhas['resenha'], 48)

    def test_save_preserva_pistas_grupos_e_migracao_04(self):
        self.g.investigar(self.e, 0)
        self.g.mediar_grupo('resenha')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'save.json'
            self.g.salvar(p)
            novo = SindicoGame(seed=1)
            novo.carregar(p)
            self.assertEqual(novo.panelinhas, self.g.panelinhas)
            self.assertEqual(novo.evento_atual['investigacao']['consultadas'], [0])
            self.assertEqual(novo.mediacao_dia, self.g.dia)
            estado = json.loads(p.read_text(encoding='utf-8'))
            del estado['comunidade']
            p.write_text(json.dumps(estado), encoding='utf-8')
            novo.carregar(p)
            self.assertEqual(set(novo.panelinhas.values()), {50})

    def test_casos_especiais_nao_repetem(self):
        g = SindicoGame(seed=6)
        casos = []
        for e in g.todos_eventos:
            novo = g.preparar_caso(copy.deepcopy(e))
            if novo.get('investigacao'):
                casos.append(novo['investigacao']['id'])
        self.assertEqual(len(casos), len(set(casos)))

    def test_preferencias_persistem_e_vibracao_inicia_desligada(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'prefs.json'
            prefs = Preferencias(p)
            self.assertFalse(prefs.valores['vibracao'])
            prefs.valores.update(som=False, texto=1.3, tutorial=True)
            prefs.salvar()
            self.assertEqual(Preferencias(p).valores, prefs.valores)
            p.write_text('{', encoding='utf-8')
            self.assertEqual(Preferencias(p).valores['texto'], 1.0)


if __name__ == '__main__':
    unittest.main()
