"""Regras do mandato, independentes da interface Kivy."""
import copy
import json
import random
from pathlib import Path


class SindicoGame:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.dia = 1
        self.caixa = 5000
        self.paciencia = 100
        self.aprovacao = 50
        self.tem_cameras = False
        self.pendencias = []
        self.consequencias = []
        self.historico = []
        self.jogo_ativo = True
        self.vitoria = False
        self.encerrado = False
        self.todos_eventos = json.loads(Path(__file__).with_name('eventos.json').read_text(encoding='utf-8'))
        if not self.todos_eventos:
            raise ValueError('O banco de eventos está vazio.')
        self.evento_atual = self._sortear_evento()

    def _sortear_evento(self):
        candidatos = [e for e in self.todos_eventos if e['dia'] == self.dia]
        if not candidatos:
            recentes = [h.get('id') for h in self.historico[-4:]]
            candidatos = [e for e in self.todos_eventos if e['id'] not in recentes] or self.todos_eventos
        evento = copy.deepcopy(self.rng.choice(candidatos))
        evento['abertura'] = self.dia
        evento['ticket'] = f"{self.dia}-{evento['id']}"
        return evento

    def verificar_status_jogo(self):
        self.paciencia = max(0, min(100, self.paciencia))
        self.aprovacao = max(0, min(100, self.aprovacao))
        if self.caixa < 0 or self.paciencia == 0:
            self.jogo_ativo = False
        return self.jogo_ativo

    def responder_evento(self, evento, indice_opcao):
        if not self.jogo_ativo:
            return 'O mandato terminou.'
        atual = evento is self.evento_atual and not self.encerrado
        pendente = next((p for p in self.pendencias if p is evento), None)
        if not atual and pendente is None:
            return 'Este chamado já foi encerrado.'
        opcao = evento['opcoes'][indice_opcao]
        custo = opcao.get('caixa_condominio', 0)
        if self.tem_cameras and evento['categoria'] == 'seguranca' and custo < 0:
            custo = round(custo * 0.5)
        self.caixa += custo
        self.paciencia += opcao.get('paciencia_sindico', 0)
        self.aprovacao += opcao.get('aprovacao', 0)
        if opcao.get('consequencia'):
            self.consequencias.append(dict(opcao['consequencia'], vence=self.dia + 3))
        self.historico.append({'dia': self.dia, 'id': evento['id'], 'texto': opcao['resposta_morador']})
        if atual:
            self.encerrado = True
        else:
            self.pendencias.remove(pendente)
        self.verificar_status_jogo()
        return opcao['resposta_morador']

    def avancar_dia(self):
        if not self.jogo_ativo:
            return
        if not self.encerrado:
            self.pendencias.append(self.evento_atual)
        penalidade = min(12, len(self.pendencias))
        self.paciencia -= penalidade
        self.aprovacao -= penalidade
        self.verificar_status_jogo()
        if not self.jogo_ativo:
            return
        # Só vence depois de terminar o dia 365, incluindo problemas pendentes.
        if self.dia == 365:
            self.vitoria = True
            self.jogo_ativo = False
            return
        self.dia += 1
        if self.dia % 30 == 1:
            inadimplencia = round(12000 * (100 - self.aprovacao) / 500)
            self.caixa += 12000 - inadimplencia - 9000
            self.historico.append({'dia': self.dia, 'texto': f'Fechamento mensal: taxas R$ {12000-inadimplencia}; despesas R$ 9000.'})
        for efeito in list(self.consequencias):
            if efeito['vence'] <= self.dia:
                self.caixa += efeito['caixa']
                self.paciencia += efeito['paciencia']
                self.aprovacao += efeito['aprovacao']
                self.historico.append({'dia': self.dia, 'texto': efeito['texto']})
                self.consequencias.remove(efeito)
        self.encerrado = False
        self.verificar_status_jogo()
        if self.jogo_ativo:
            self.evento_atual = self._sortear_evento()

    def comprar_cameras(self):
        if self.jogo_ativo and not self.tem_cameras and self.caixa >= 1500:
            self.caixa -= 1500
            self.tem_cameras = True
            self.aprovacao += 10
            self.verificar_status_jogo()
            return True
        return False

    def salvar(self, caminho):
        estado = {k: v for k, v in vars(self).items() if k not in ('rng', 'todos_eventos')}
        destino = Path(caminho)
        destino.parent.mkdir(parents=True, exist_ok=True)
        temporario = destino.with_suffix('.tmp')
        temporario.write_text(json.dumps(estado, ensure_ascii=False), encoding='utf-8')
        temporario.replace(destino)

    def carregar(self, caminho):
        estado = json.loads(Path(caminho).read_text(encoding='utf-8'))
        campos = set(vars(self)) - {'rng', 'todos_eventos'}
        if set(estado) != campos or not 1 <= estado['dia'] <= 365:
            raise ValueError('Save incompatível.')
        for nome in campos:
            setattr(self, nome, estado[nome])
