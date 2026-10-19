"""Investigações e interesses coletivos do condomínio."""
import copy

PANELINHAS = {
    'sossego': dict(nome='Liga do Sossego', lema='Silêncio depois das 22h. Até no áudio.', membros=['Dona Cida (101)', 'Patrícia (502)', 'Gilberto (601)'], gostos=dict(passiva=2, multa=4, debochada=-3, conselho=-5, melhoria=3, delegacao=1)),
    'resenha': dict(nome='Turma da Resenha', lema='Área comum também serve para viver.', membros=['Beto (401)', 'Nanda (704)', 'Júnior (203)'], gostos=dict(passiva=2, multa=-5, debochada=2, conselho=-3, melhoria=2, delegacao=1)),
    'planilha': dict(nome='Fiscalizadores do Pix', lema='Cadê a nota? E os três orçamentos?', membros=['Lúcia (302)', 'Rogério (805)'], gostos=dict(passiva=-1, multa=2, debochada=-2, conselho=-6, melhoria=4, delegacao=-1)),
}

# Os fatos são roteirizados: boatos nunca são tratados como prova.
CASOS = [
 dict(id='bike', categoria='seguranca', titulo='A bicicleta que saiu sozinha', mensagem='Uma bicicleta sumiu do bicicletário. Há três versões no grupo. Descubra o que aconteceu antes de apontar culpados.', suspeitos=['Morador que retirou por engano', 'Visitante sem autorização', 'Entrega na garagem errada'], verdade=0,
      provas=[('Registro do portão', 'O acesso ocorreu com a tag de um morador, sem entrada de visitante.', True), ('Comprovante da devolução', 'O morador da tag devolveu a bicicleta e reconheceu a troca com a sua.', True), ('Áudio encaminhado', 'Um áudio sem autor acusa um entregador que nem entrou no prédio.', False)]),
 dict(id='vaga', categoria='garagem', titulo='O carro atravessado', mensagem='Um carro ocupa duas vagas. Um vizinho quer multar o primeiro nome que apareceu no grupo. Confira a ocorrência.', suspeitos=['Motorista da mudança', 'Prestador da pintura', 'Morador com autorização de carga'], verdade=2,
      provas=[('Livro da portaria', 'Há autorização de carga para um morador, no horário da foto.', True), ('Aviso da mudança', 'A placa da foto consta na autorização e o prazo de carga ainda não terminou.', True), ('Print recortado', 'Um print sem data afirma que seria o carro do pintor.', False)]),
 dict(id='caixa', categoria='encomendas', titulo='O pacote desaparecido', mensagem='Uma encomenda foi dada como entregue, mas não chegou ao apartamento. O grupo já está montando um tribunal.', suspeitos=['Entrega no bloco vizinho', 'Retirada pelo destinatário', 'Troca de etiquetas na portaria'], verdade=0,
      provas=[('Recibo de entrega', 'O recibo registra o bloco vizinho, com assinatura da portaria de lá.', True), ('Conferência do rastreio', 'A transportadora confirmou o endereço errado e localizou o pacote nesse bloco.', True), ('Mensagem de um vizinho', 'Alguém disse que o destinatário já abriu a caixa, sem ter visto a entrega.', False)]),
 dict(id='som', categoria='barulho', titulo='O grave atravessa a parede', mensagem='Há música alta, mas o áudio ecoa no pátio. Antes de multar um apartamento, localize a origem.', suspeitos=['Festa no salão', 'Caixa de som na janela', 'Comércio do outro lado da rua'], verdade=2,
      provas=[('Ronda no pátio', 'O som fica mais alto no muro voltado à rua; o salão está vazio.', True), ('Contato com o comércio', 'O comércio confirmou o teste de som e desligou a caixa: o ruído cessou.', True), ('Enquete do grupo', 'Uma enquete acusa o apartamento 704 porque ele gosta de festa.', False)]),
 dict(id='lixo', categoria='lixo', titulo='O saco rasgado do corredor', mensagem='O lixo apareceu espalhado. Tem vizinho acusando cachorro, criança e até o aspirador robô. Vamos aos fatos.', suspeitos=['Saco rompido no transporte', 'Animal sem coleira', 'Coleta fora do horário'], verdade=0,
      provas=[('Inspeção do saco', 'A alça estava rasgada; há um rastro contínuo desde o elevador de serviço.', True), ('Relato de quem levou', 'O responsável confirmou que a alça rompeu enquanto carregava o saco.', True), ('Foto antiga', 'Uma foto de cachorro no corredor é de outra semana e outro andar.', False)]),
 dict(id='alarme', categoria='seguranca', titulo='O alarme e o suspeito de chinelo', mensagem='O alarme disparou. Uma foto borrada virou prova no grupo. Investigue antes de acusar alguém.', suspeitos=['Falha no sensor', 'Entrada forçada', 'Teste não autorizado'], verdade=0,
      provas=[('Laudo do sensor', 'O técnico registrou curto por umidade, sem sinal de violação.', True), ('Log do sistema', 'Nenhuma porta foi aberta no horário; apenas o sensor com defeito disparou.', True), ('Foto borrada', 'A pessoa de chinelo na foto é de um vídeo antigo, sem ligação com o disparo.', False)]),
]


class ComunidadeMixin:
    def iniciar_comunidade(self):
        self.panelinhas = {k: 50 for k in PANELINHAS}
        self.mediacao_dia = 0
        self.casos_resolvidos = 0
        self.casos_vistos = []

    def preparar_caso(self, evento):
        candidatos = [c for c in CASOS if c['categoria'] == evento['categoria'] and c['id'] not in self.casos_vistos]
        if candidatos and self.rng.random() < .5:
            caso = copy.deepcopy(self.rng.choice(candidatos))
            self.casos_vistos.append(caso['id'])
            ordem = list(range(len(caso['suspeitos'])))
            self.rng.shuffle(ordem)
            caso['verdade'] = ordem.index(caso['verdade'])
            caso['suspeitos'] = [caso['suspeitos'][i] for i in ordem]
            caso['consultadas'] = []
            evento['investigacao'] = caso
            textos = ['Resolver administrativamente sem acusar ninguém.', 'Responder com deboche e encerrar a apuração.', 'Aplicar cobrança sem apurar os fatos.', 'Seguir a ideia do conselheiro.']
            for i, opcao in enumerate(evento['opcoes']):
                opcao['texto'] = textos[min(i, 3)]
                opcao['resposta_morador'] = ['O caso foi tratado por diálogo, sem acusação.', 'O deboche encerrou a conversa e deixou vizinhos irritados.', 'A cobrança sem apuração exigiu retratação.', 'O conselho foi ouvido. Isso ainda vai dar problema.'][min(i, 3)]
            evento['titulo'], evento['mensagem'] = caso['titulo'], caso['mensagem']
            evento['conselheiro_pitaco'] = 'Vamos multar o apartamento inteiro por ordem alfabética. Estatisticamente alguém acerta.'
        return evento

    def grupo_morador(self, nome):
        return next((k for k, g in PANELINHAS.items() if nome in g['membros']), None)

    def efeito_panelinhas(self, tipo):
        return {k: g['gostos'].get(tipo, 0) for k, g in PANELINHAS.items()}

    def atualizar_panelinhas(self, tipo):
        for k, delta in self.efeito_panelinhas(tipo).items():
            self.panelinhas[k] = max(0, min(100, self.panelinhas[k]+delta))

    def bonus_panelinha(self, nome):
        chave = self.grupo_morador(nome)
        return (self.panelinhas[chave]-50)*.12 if chave else 0

    def mediar_grupo(self, chave):
        if chave not in PANELINHAS:
            raise ValueError('Grupo inválido.')
        if not self.jogo_ativo or self.assembleia or self.mediacao_dia == self.dia or self.caixa < 100:
            return 'Mediação disponível fora da assembleia: R$ 100, uma vez por dia.'
        if self.panelinhas[chave] >= 100:
            return 'Este grupo já está plenamente satisfeito.'
        self.caixa -= 100
        self.paciencia -= 3
        self.mediacao_dia = self.dia
        for k in self.panelinhas:
            self.panelinhas[k] = max(0, min(100, self.panelinhas[k]+(12 if k == chave else -2)))
        self._log('Mediação com '+PANELINHAS[chave]['nome']+'. Outros grupos cobraram atenção igual.', tipo='panelinha')
        self.verificar_status_jogo()
        return 'Grupo ouvido: +12 de apoio. Os demais perderam 2. A conversa custou 3 de paciência.'

    def caso_aberto(self, evento):
        return (self.jogo_ativo and not self.assembleia and bool(evento.get('investigacao')) and
                ((evento is self.evento_atual and not self.encerrado) or any(p is evento for p in self.pendencias)))

    def custo_pista(self, indice):
        return 20 if indice == 0 and self.tem_cameras else 60

    def investigar(self, evento, indice):
        if not self.caso_aberto(evento):
            return 'Este caso não está disponível agora.'
        caso = evento['investigacao']
        if not 0 <= indice < len(caso['provas']):
            raise ValueError('Pista inválida.')
        if indice in caso['consultadas']:
            return 'Essa fonte já foi consultada.'
        custo = self.custo_pista(indice)
        if self.caixa < custo:
            return 'O caixa não cobre esta consulta.'
        self.caixa -= custo
        self.paciencia -= 2
        caso['consultadas'].append(indice)
        self._log('Pista consultada: '+caso['provas'][indice][0]+'.', tipo='investigacao')
        self.verificar_status_jogo()
        return caso['provas'][indice][1]

    def concluir_caso(self, evento, suspeito):
        if not self.caso_aberto(evento):
            return 'Este caso já foi encerrado ou está bloqueado.'
        caso = evento['investigacao']
        if suspeito is not None and (not isinstance(suspeito, int) or not 0 <= suspeito < len(caso['suspeitos'])):
            raise ValueError('Conclusão inválida.')
        provas = sum(caso['provas'][i][2] for i in caso['consultadas'])
        if suspeito is None:
            texto = 'Caso arquivado sem acusação. Sem multa nem recompensa; é possível agir sem culpar alguém.'
            self.paciencia -= 2
            tipo = 'passiva'
        elif suspeito == caso['verdade'] and provas >= 2:
            self.aprovacao += 8
            self.paciencia += 4
            self.casos_resolvidos += 1
            texto = 'Conclusão confirmada por duas fontes: '+caso['suspeitos'][suspeito]+'. +8 de apoio, +4 de paciência.'
            tipo = 'melhoria'
        else:
            self.caixa -= 200
            self.aprovacao -= 10
            self.paciencia -= 6
            texto = 'Acusação incorreta ou sem duas fontes verificadas. Retratação: R$ 200, -10 de apoio, -6 de paciência.'
            tipo = 'multa'
        self._memoria(evento, tipo)
        self.atualizar_panelinhas(tipo)
        self._log(texto, id=evento['id'], tipo='investigacao')
        if evento is self.evento_atual:
            self.encerrado = True
        else:
            self.pendencias.remove(evento)
        self.verificar_status_jogo()
        return texto
