"""Regras, sorteio persistente e memória do mandato, sem dependência do Kivy."""
import copy
import json
import random
import secrets
from pathlib import Path
from lore import PERFIS, MELHORIAS, PROPOSTAS, calendario

CAMPOS = ('dia', 'caixa', 'paciencia', 'aprovacao', 'pendencias', 'consequencias',
          'historico', 'jogo_ativo', 'vitoria', 'encerrado', 'evento_atual',
          'semente', 'vistos', 'melhorias', 'moradores', 'dias_revolta',
          'assembleia', 'ultima_votacao', 'ultima_assembleia', 'fim_motivo',
          'descanso_dia', 'delegacao_dia', 'social_dia', 'fechamento_dia',
          'contador_crises', 'escolhas')


def limite(valor):
    return max(0, min(100, valor))


def tuplas(valor):
    return tuple(tuplas(v) for v in valor) if isinstance(valor, list) else valor


class SindicoGame:
    def __init__(self, seed=None, evitar_inicio=None):
        self.semente = seed if seed is not None else secrets.randbits(64)
        self.rng = random.Random(self.semente)
        self.dia, self.caixa, self.paciencia, self.aprovacao = 1, 5000, 100, 50
        self.pendencias, self.consequencias, self.historico, self.vistos = [], [], [], []
        self.jogo_ativo, self.vitoria, self.encerrado = True, False, False
        self.melhorias = {k: False for k in MELHORIAS}
        self.moradores = {nome: dict(confianca=50, irritacao=0, ultima='Ainda não teve um chamado atendido.')
                          for nome in PERFIS}
        self.dias_revolta, self.contador_crises, self.fechamento_dia = 0, 0, 0
        self.assembleia, self.ultima_votacao, self.ultima_assembleia = None, None, 0
        self.fim_motivo = ''
        self.descanso_dia = self.delegacao_dia = self.social_dia = False
        self.escolhas = dict(passiva=0, debochada=0, multa=0, conselho=0, melhoria=0, delegacao=0)
        self.todos_eventos = json.loads(Path(__file__).with_name('eventos.json').read_text(encoding='utf-8'))
        if not self.todos_eventos:
            raise ValueError('O banco de eventos está vazio.')
        self.evento_atual = self._sortear_evento(evitar_inicio)

    @property
    def tem_cameras(self):
        return self.melhorias['cameras']

    @property
    def evento_foco(self):
        return next((e for e in self.pendencias if e.get('tipo_evento') == 'crise'), self.evento_atual)

    @property
    def custo_mensal(self):
        return 9000 + sum(MELHORIAS[k]['mensal'] for k, ativa in self.melhorias.items() if ativa)

    @property
    def titulo_final(self):
        if not self.vitoria:
            return {'destituicao': 'Banido do próprio grupo', 'paciencia': 'A última gota de paciência',
                    'caixa': 'O caixa pediu demissão'}.get(self.fim_motivo, 'Fim de mandato')
        if self.consequencias or self.pendencias:
            return 'Abacaxi para o próximo síndico'
        if self.aprovacao >= 70:
            return 'Diplomata do Bloco B'
        if self.escolhas['multa'] > self.escolhas['passiva']:
            return 'Mão de ferro da garagem'
        return 'Sobrevivente do Zap'

    def _log(self, texto, **extra):
        self.historico.append(dict(dia=self.dia, texto=texto, **extra))

    def _sortear_evento(self, evitar=None):
        mes, dia_mes = calendario(self.dia)
        livres = [e for e in self.todos_eventos if e['id'] not in self.vistos]
        candidatos = [e for e in livres if e.get('mes') == mes] or livres
        if evitar and len(candidatos) > 1:
            candidatos = [e for e in candidatos if e['id'] != evitar]
        if not candidatos:
            raise ValueError('Não há ocorrências inéditas disponíveis.')
        evento = copy.deepcopy(self.rng.choice(candidatos))
        self.vistos.append(evento['id'])
        evento['dia_roteiro'] = evento['dia']
        evento.update(dia=self.dia, mes=mes, dia_mes=dia_mes, abertura=self.dia,
                      ticket=f"{self.dia}-{evento['id']}", tipo_evento='normal')
        return evento

    def verificar_status_jogo(self):
        self.paciencia, self.aprovacao = limite(self.paciencia), limite(self.aprovacao)
        for estado in self.moradores.values():
            estado['confianca'] = limite(estado['confianca'])
            estado['irritacao'] = limite(estado['irritacao'])
        if self.jogo_ativo and (self.caixa < 0 or self.paciencia == 0):
            self.fim_motivo = 'caixa' if self.caixa < 0 else 'paciencia'
            self.jogo_ativo = False
        return self.jogo_ativo

    def opcoes_evento(self, evento):
        opcoes = copy.deepcopy(evento['opcoes'])
        if evento.get('tipo_evento') == 'crise':
            return opcoes
        categoria = evento['categoria']
        ordem = ['portaria', 'cameras'] if categoria == 'seguranca' else ['manutencao', 'reservas']
        for chave in ordem:
            melhoria = MELHORIAS[chave]
            if self.melhorias[chave] and categoria in melhoria['categoria']:
                opcoes.append(dict(tipo='melhoria', texto={
                    'portaria': 'Acionar a equipe da portaria remota.',
                    'cameras': 'Conferir as gravações e identificar o responsável.',
                    'manutencao': 'Acionar o plano de manutenção preventiva.',
                    'reservas': 'Resolver com a agenda digital e o registro de uso.'
                }[chave], paciencia_sindico=2, aprovacao=3, caixa_condominio=-35,
                    resposta_morador=f"{melhoria['nome']} resolveu o chamado sem improviso."))
                break
        return opcoes

    def impacto_opcao(self, evento, opcao):
        caixa = opcao.get('caixa_condominio', 0)
        paciencia = opcao.get('paciencia_sindico', 0)
        aprovacao = opcao.get('aprovacao', 0)
        tipo = opcao.get('tipo', 'passiva')
        cat = evento['categoria']
        if caixa < 0 and evento.get('tipo_evento') != 'crise':
            if self.tem_cameras and cat == 'seguranca':
                caixa = round(caixa * .5)
            if self.melhorias['manutencao'] and cat in ('agua', 'manutencao') and tipo == 'passiva':
                caixa = round(caixa * .55)
                paciencia = max(0, paciencia)
            if self.melhorias['reservas'] and cat in MELHORIAS['reservas']['categoria'] and tipo == 'passiva':
                caixa = round(caixa * .6)
        morador = self.moradores.get(evento['remetente'])
        if morador and morador['irritacao'] >= 40 and tipo in ('debochada', 'multa', 'conselho'):
            aprovacao -= 2
        return dict(caixa=caixa, paciencia=paciencia, aprovacao=aprovacao)

    def _memoria(self, evento, tipo):
        afetado = evento['remetente']
        ganho = {'passiva': 7, 'debochada': -10, 'multa': -7, 'conselho': -5, 'melhoria': 9, 'delegacao': 4}.get(tipo, 0)
        irritacao = {'passiva': -6, 'debochada': 12, 'multa': 8, 'conselho': 7, 'melhoria': -8, 'delegacao': -4}.get(tipo, 0)
        for nome, estado in self.moradores.items():
            if nome == afetado:
                estado['confianca'] += ganho
                estado['irritacao'] += irritacao
                estado['ultima'] = f"Dia {self.dia}: {tipo} no chamado {evento.get('titulo', 'do grupo')}."
            elif PERFIS[nome]['interesse'] == evento['categoria']:
                estado['confianca'] += 2 if ganho > 0 else -2
        self.verificar_status_jogo()

    def responder_evento(self, evento, indice_opcao):
        if not self.jogo_ativo:
            return 'O mandato terminou.'
        if self.assembleia:
            return 'A assembleia precisa ser votada antes dos chamados.'
        atual = evento is self.evento_atual and not self.encerrado
        pendente = next((p for p in self.pendencias if p is evento), None)
        if not atual and pendente is None:
            return 'Este chamado já foi encerrado.'
        opcoes = self.opcoes_evento(evento)
        if not 0 <= indice_opcao < len(opcoes):
            raise ValueError('Opção inválida.')
        opcao = opcoes[indice_opcao]
        impacto = self.impacto_opcao(evento, opcao)
        self.caixa += impacto['caixa']
        self.paciencia += impacto['paciencia']
        self.aprovacao += impacto['aprovacao']
        tipo = opcao.get('tipo', ['passiva', 'debochada', 'multa', 'conselho'][min(indice_opcao, 3)])
        self.escolhas[tipo] = self.escolhas.get(tipo, 0)+1
        self._memoria(evento, tipo)
        if opcao.get('consequencia'):
            fonte = dict(titulo=evento.get('titulo', 'O conselho do grupo'), remetente=evento['remetente'],
                         categoria=evento['categoria'], conselheiro=evento.get('conselheiro', 'Toninho'),
                         custo=abs(opcao['consequencia']['caixa']), etapa=1)
            self.consequencias.append(dict(tipo='crise', vence=self.dia+3, fonte=fonte))
        if opcao.get('agravar'):
            fonte = copy.deepcopy(evento['fonte'])
            fonte.update(etapa=2, custo=round(fonte['custo']*1.4))
            self.consequencias.append(dict(tipo='crise', vence=self.dia+2, fonte=fonte))
        resposta = opcao['resposta_morador']
        self._log(resposta, id=evento['id'], tipo=tipo)
        if atual:
            self.encerrado = True
        else:
            self.pendencias.remove(pendente)
        self.verificar_status_jogo()
        return resposta

    def _abrir_crise(self, fonte):
        self.contador_crises += 1
        custo = fonte['custo']
        if self.melhorias['manutencao'] and fonte['categoria'] in ('agua', 'manutencao'):
            custo = round(custo*.7)
        etapa = fonte['etapa']
        id_crise = f"crise-{self.contador_crises}"
        opcoes = [
            dict(tipo='passiva', texto=f"Contratar a correção definitiva por R$ {custo}.",
                 caixa_condominio=-custo, paciencia_sindico=-3, aprovacao=6,
                 resposta_morador='A correção foi feita e a crise foi encerrada. O conselho ficou em silêncio.'),
            dict(tipo='passiva', texto=f"Negociar reparação e um plano simplificado por R$ {round(custo*.65)}.",
                 caixa_condominio=-round(custo*.65), paciencia_sindico=-8, aprovacao=-3,
                 resposta_morador='A reparação foi acordada, com desgaste na negociação. O chamado foi encerrado.'),
        ]
        if etapa == 1:
            opcoes.append(dict(tipo='conselho', texto='Aceitar outra gambiarra do conselho e empurrar a conta.',
                              caixa_condominio=-50, paciencia_sindico=4, aprovacao=-5, agravar=True,
                              resposta_morador='A gambiarra adiou o reparo. A segunda crise chega em dois dias.'))
        crise = dict(id=id_crise, ticket=id_crise, tipo_evento='crise', etapa=etapa,
                     dia=self.dia, abertura=self.dia, prazo=self.dia+2,
                     titulo=('Efeito borboleta: ' if etapa == 1 else 'A gambiarra voltou: ')+fonte['titulo'],
                     mensagem=f"O plano de {fonte['conselheiro']} deu errado. Precisamos decidir como reparar os danos antes do prazo.",
                     remetente=fonte['remetente'], categoria=fonte['categoria'],
                     conselheiro=fonte['conselheiro'], conselheiro_pitaco='Dessa vez eu tenho um plano melhor.',
                     opcoes=opcoes, fonte=copy.deepcopy(fonte))
        self.pendencias.insert(0, crise)
        self._log(f"CRISE ABERTA: {fonte['titulo']}. Prazo: dia {crise['prazo']}.", tipo='crise')

    def _prazos(self):
        for evento in list(self.pendencias):
            if evento.get('tipo_evento') == 'crise' and evento['prazo'] <= self.dia:
                custo = round(evento['fonte']['custo']*1.5)
                self.caixa -= custo
                self.paciencia -= 8
                self.aprovacao -= 10
                self.pendencias.remove(evento)
                self._memoria(evento, 'conselho')
                self._log(f"Prazo perdido: {evento['titulo']}. Reparo emergencial: R$ {custo}.", tipo='crise')

    def avancar_dia(self):
        if not self.jogo_ativo:
            return 'O mandato terminou.'
        if self.assembleia:
            return 'Vote a assembleia antes de encerrar o dia.'
        if self.fechamento_dia != self.dia:
            if not self.encerrado:
                self.pendencias.append(self.evento_atual)
                self.encerrado = True
            self._prazos()
            penalidade = min(12, len(self.pendencias))
            self.paciencia -= penalidade
            self.aprovacao -= penalidade
            self.fechamento_dia = self.dia
            self.verificar_status_jogo()
            if not self.jogo_ativo:
                return 'O mandato terminou.'
            self.dias_revolta = self.dias_revolta+1 if self.aprovacao < 20 else 0
            if self.dias_revolta >= 3:
                self.assembleia = dict(tipo='crise', dia=self.dia, titulo='Assembleia de destituição')
                self._log('Três dias de aprovação abaixo de 20%. Os moradores convocaram uma assembleia de crise.')
                return 'Assembleia de crise convocada. O mandato está em votação.'
        if self.dia == 365:
            self.vitoria, self.jogo_ativo, self.fim_motivo = True, False, 'vitoria'
            return 'Mandato concluído.'
        self.dia += 1
        self.descanso_dia = self.delegacao_dia = self.social_dia = False
        if self.dia % 30 == 1:
            inadimplencia = round(12000*(100-self.aprovacao)/500)
            self.caixa += 12000-inadimplencia-self.custo_mensal
            self._log(f'Fechamento mensal: taxas R$ {12000-inadimplencia}; despesas R$ {self.custo_mensal}.', tipo='financeiro')
            self.assembleia = dict(tipo='ordinaria', dia=self.dia, titulo='Assembleia do mês')
        for efeito in list(self.consequencias):
            if efeito['vence'] <= self.dia:
                if efeito.get('tipo') == 'crise':
                    self._abrir_crise(efeito['fonte'])
                else:
                    # Consequências contratadas em saves antigos mantêm seu custo original.
                    self.caixa += efeito.get('caixa', 0)
                    self.paciencia += efeito.get('paciencia', 0)
                    self.aprovacao += efeito.get('aprovacao', 0)
                    self._log(efeito.get('texto', 'Uma consequência antiga chegou.'), tipo='crise')
                self.consequencias.remove(efeito)
        self.encerrado = False
        self.verificar_status_jogo()
        if self.jogo_ativo:
            self.evento_atual = self._sortear_evento()
        return 'Novo dia. O grupo está digitando...'

    def propostas(self):
        return copy.deepcopy(PROPOSTAS[self.assembleia['tipo']]) if self.assembleia else []

    def prever_votos(self, proposta):
        votos = []
        for nome, estado in self.moradores.items():
            nota = estado['confianca']*.6+self.aprovacao*.4+proposta['apoio']-estado['irritacao']*.12
            sim = nota >= 50+PERFIS[nome]['rigor']
            votos.append(dict(nome=nome, sim=sim, motivo='Confia no plano apresentado.' if sim else 'Confiança insuficiente ou irritação acumulada.'))
        return votos

    def votar(self, indice):
        if not self.jogo_ativo or not self.assembleia:
            return 'Não há assembleia em votação.'
        propostas = self.propostas()
        if not 0 <= indice < len(propostas):
            raise ValueError('Proposta inválida.')
        proposta = propostas[indice]
        if self.caixa < proposta['custo']:
            return 'O caixa não cobre essa proposta. Escolha uma alternativa.'
        votos = self.prever_votos(proposta)
        sim = sum(v['sim'] for v in votos)
        aprovada = sim >= len(votos)//2+1
        tipo = self.assembleia['tipo']
        self.ultima_votacao = dict(dia=self.dia, titulo=proposta['titulo'], votos=votos,
                                   sim=sim, total=len(votos), aprovada=aprovada, tipo=tipo)
        self.ultima_assembleia = self.dia
        self.assembleia = None
        self.dias_revolta = 0
        if aprovada:
            self.caixa += proposta['receita']-proposta['custo']
            self.paciencia += proposta['paciencia']
            self.aprovacao += proposta['aprovacao']
            for estado in self.moradores.values():
                estado['confianca'] += proposta['confianca']
                estado['irritacao'] -= 8
            resultado = f"Proposta aprovada: {sim}/{len(votos)} votos. {proposta['titulo']}."
        else:
            self.paciencia -= 5
            self.aprovacao -= 5
            resultado = f"Proposta rejeitada: {sim}/{len(votos)} votos."
            if tipo == 'crise':
                self.jogo_ativo, self.fim_motivo = False, 'destituicao'
                resultado += ' Os moradores encerraram seu mandato.'
        self._log(resultado, tipo='assembleia')
        self.verificar_status_jogo()
        return resultado

    def comprar_melhoria(self, chave):
        if chave not in MELHORIAS:
            raise ValueError('Melhoria inválida.')
        spec = MELHORIAS[chave]
        if not self.jogo_ativo or self.melhorias[chave] or self.caixa < spec['custo']:
            return False
        self.caixa -= spec['custo']
        self.melhorias[chave] = True
        self.aprovacao += 10 if chave == 'cameras' else 5
        self._log(f"{spec['nome']} instalado. Manutenção mensal: R$ {spec['mensal']}.", tipo='melhoria')
        self.verificar_status_jogo()
        return True

    def comprar_cameras(self):
        return self.comprar_melhoria('cameras')

    def descansar(self):
        if not self.jogo_ativo or self.descanso_dia or self.caixa < 180:
            return 'Descanso indisponível: custa R$ 180 e pode ser usado uma vez por dia.'
        self.caixa -= 180
        self.paciencia += 14
        self.aprovacao -= 2
        self.descanso_dia = True
        self._log('Uma pausa com cobertura da gestão: R$ 180, +14 de paciência.', tipo='descanso')
        self.verificar_status_jogo()
        return 'Você silenciou o grupo por uma hora. +14 de paciência; -2 de aprovação.'

    def delegar(self):
        if not self.jogo_ativo or self.delegacao_dia or self.assembleia:
            return 'Delegação indisponível agora.'
        evento = next((e for e in self.pendencias if e.get('tipo_evento') != 'crise'), None)
        atual = False
        if evento is None and not self.encerrado:
            evento, atual = self.evento_atual, True
        custo = 160 if self.melhorias['portaria'] else 240
        if evento is None or self.caixa < custo:
            return 'Sem chamado comum para delegar ou saldo insuficiente.'
        self.caixa -= custo
        self.paciencia += 4
        self.aprovacao += 2
        self._memoria(evento, 'delegacao')
        self.escolhas['delegacao'] += 1
        if atual:
            self.encerrado = True
        else:
            self.pendencias.remove(evento)
        self.delegacao_dia = True
        self.verificar_status_jogo()
        self._log(f"Equipe resolveu {evento.get('titulo', 'o chamado')} por R$ {custo}.", tipo='delegacao')
        return 'Chamado delegado e resolvido. A equipe não aceita executar palpites dos conselheiros.'

    def reconciliar(self, nome):
        if nome not in self.moradores:
            raise ValueError('Morador inválido.')
        if not self.jogo_ativo or self.social_dia or self.caixa < 120:
            return 'Uma conversa por dia, com custo de R$ 120 para organizar a mediação.'
        estado = self.moradores[nome]
        if estado['confianca'] >= 100 and estado['irritacao'] == 0:
            return 'Essa relação já está em paz.'
        self.caixa -= 120
        self.paciencia -= 3
        self.aprovacao += 5
        estado['confianca'] = limite(estado['confianca']+15)
        estado['irritacao'] = limite(estado['irritacao']-18)
        estado['ultima'] = f'Dia {self.dia}: ouviu você numa conversa de reconciliação.'
        self.social_dia = True
        self.verificar_status_jogo()
        self._log(f'Conversa de reconciliação com {nome}.', tipo='social')
        return 'Conversa registrada: +15 de confiança e menos irritação.'

    def salvar(self, caminho):
        estado = {k: copy.deepcopy(getattr(self, k)) for k in CAMPOS}
        estado.update(versao_save=2, rng_state=self.rng.getstate())
        destino = Path(caminho)
        destino.parent.mkdir(parents=True, exist_ok=True)
        temporario = destino.with_suffix('.tmp')
        temporario.write_text(json.dumps(estado, ensure_ascii=False), encoding='utf-8')
        temporario.replace(destino)

    def carregar(self, caminho):
        estado = json.loads(Path(caminho).read_text(encoding='utf-8'))
        if not isinstance(estado, dict) or not isinstance(estado.get('dia'), int) or not 1 <= estado['dia'] <= 365:
            raise ValueError('Save incompatível.')
        novo = SindicoGame(seed=estado.get('semente', self.semente))
        if estado.get('versao_save') == 2:
            if not all(k in estado for k in CAMPOS) or 'rng_state' not in estado:
                raise ValueError('Save incompleto.')
            for campo in CAMPOS:
                setattr(novo, campo, copy.deepcopy(estado[campo]))
            novo.rng.setstate(tuplas(estado['rng_state']))
        elif 'versao_save' not in estado:
            basicos = ('dia', 'caixa', 'paciencia', 'aprovacao', 'pendencias', 'consequencias',
                       'historico', 'jogo_ativo', 'vitoria', 'encerrado', 'evento_atual')
            if not all(k in estado for k in basicos):
                raise ValueError('Save antigo incompleto.')
            for campo in basicos:
                setattr(novo, campo, copy.deepcopy(estado[campo]))
            novo.melhorias['cameras'] = bool(estado.get('tem_cameras', False))
            ids = {e['id'] for e in novo.todos_eventos}
            vistos = [h.get('id') for h in novo.historico]+[e.get('id') for e in novo.pendencias]+[novo.evento_atual.get('id')]
            novo.vistos = list(dict.fromkeys(i for i in vistos if i in ids))
            novo.fim_motivo = 'vitoria' if novo.vitoria else ('paciencia' if novo.paciencia <= 0 else 'caixa' if novo.caixa < 0 else '')
        else:
            raise ValueError('Versão de save desconhecida.')
        ids = {e['id'] for e in novo.todos_eventos}
        if not isinstance(novo.vistos, list) or len(novo.vistos) != len(set(novo.vistos)) or not set(novo.vistos) <= ids:
            raise ValueError('Histórico de sorteio inválido.')
        if set(novo.melhorias) != set(MELHORIAS) or set(novo.moradores) != set(PERFIS):
            raise ValueError('Estado de gestão inválido.')
        if not isinstance(novo.evento_atual, dict) or not isinstance(novo.evento_atual.get('opcoes'), list):
            raise ValueError('Chamado inválido.')
        for atributo in ('caixa', 'paciencia', 'aprovacao'):
            if not isinstance(getattr(novo, atributo), (int, float)):
                raise ValueError('Indicador inválido.')
        for morador in novo.moradores.values():
            if not all(isinstance(morador.get(k), (int, float)) for k in ('confianca', 'irritacao')):
                raise ValueError('Memória inválida.')
        for campo in CAMPOS:
            setattr(self, campo, getattr(novo, campo))
        self.rng = novo.rng
