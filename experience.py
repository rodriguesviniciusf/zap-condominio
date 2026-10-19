"""Telas de investigação, grupos, ajuda e acessibilidade."""
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from community import PANELINHAS
from ui import BG, INK, MINT, MUTED, AMBER, CORAL, PANEL2, Card, Text, button, stack, set_text_scale

PASSOS = [
 ('1 / 4 · Seu mandato', 'Você tem 365 dias para administrar o condomínio. Caixa negativo ou paciência zerada encerram a partida. Aprovação baixa pode provocar uma assembleia de destituição.'),
 ('2 / 4 · Leia antes de responder', 'As respostas mostram seus custos. Palpites do conselho podem virar crises com prazo. Deixar para amanhã cria pendências que desgastam sua gestão; consulte a aba Pautas.'),
 ('3 / 4 · Apure os fatos', 'Alguns chamados abrem uma investigação. Consulte fontes por R$ 60 e 2 de paciência; a primeira custa R$ 20 com câmeras. São necessárias duas fontes verificadas e uma conclusão correta. Boato não é prova. Você também pode arquivar sem acusar.'),
 ('4 / 4 · Ninguém governa sozinho', 'Em Gente, acompanhe confiança e panelinhas: silêncio, liberdade e economia geram votos diferentes. Em Prédio, descanse, delegue ou invista. As preferências de som, vibração, texto e transições ficam no menu. O jogo salva suas decisões automaticamente.'),
]


class ExperienceMixin:
    def dialogo(self, titulo):
        box = stack(10, dp(14))
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(box)
        popup = Popup(title=titulo, content=scroll, size_hint=(.94, .85),
                      background='', background_color=BG, title_color=INK, separator_color=MINT)
        return popup, box

    def tutorial(self, passo=0):
        popup, box = self.dialogo('Guia rápido do síndico')
        titulo, texto = PASSOS[passo]
        box.add_widget(Text(titulo, size=23, bold=True))
        box.add_widget(Text(texto, size=17))
        def seguir():
            popup.dismiss()
            if passo < len(PASSOS)-1:
                self.tutorial(passo+1)
            else:
                self.terminar_tutorial()
        box.add_widget(button('Próximo' if passo < 3 else 'Assumir a gestão', seguir, primary=True))
        box.add_widget(button('Pular tutorial', lambda: (popup.dismiss(), self.terminar_tutorial())))
        popup.open()

    def terminar_tutorial(self):
        self.preferencias.valores['tutorial'] = True
        self.salvar_preferencias()

    def salvar_preferencias(self):
        try:
            self.preferencias.salvar()
        except OSError:
            self.aviso = 'Não foi possível salvar as preferências no aparelho.'
            return False
        return True

    def ajustes(self):
        popup, box = self.dialogo('Preferências do jogo')
        p = self.preferencias.valores
        box.add_widget(Text('Do seu jeito.', size=26, bold=True))
        box.add_widget(Text('Áudio curto original, sem música contínua. A vibração depende do aparelho e começa desligada.', size=14, color=MUTED))
        def alternar(chave):
            p[chave] = not p[chave]
            if chave == 'vibracao' and p[chave] and not self.preferencias.testar_vibracao():
                p[chave] = False
                self.aviso = 'Vibração indisponível neste aparelho.'
            self.salvar_preferencias()
            self.preferencias.tocar('toque')
            popup.dismiss()
            self.render()
            self.ajustes()
        for chave, nome, ligado, desligado in [('som', 'Sons', 'ligados', 'desligados'), ('vibracao', 'Vibração', 'ligada', 'desligada'), ('transicoes', 'Transições entre dias', 'ligadas', 'desligadas')]:
            box.add_widget(button(nome+' · '+(ligado if p[chave] else desligado), lambda k=chave: alternar(k)))
        box.add_widget(Text('Tamanho do texto de leitura', size=17, bold=True))
        def tamanho(valor):
            p['texto'] = valor
            set_text_scale(valor)
            self.salvar_preferencias()
            popup.dismiss()
            self.render()
            self.ajustes()
        for valor, nome in [(1.0, 'Padrão'), (1.15, 'Grande'), (1.3, 'Muito grande')]:
            box.add_widget(button(nome+(' · selecionado' if p['texto'] == valor else ''), lambda v=valor: tamanho(v)))
        if self.aviso:
            box.add_widget(Text(self.aviso, size=13, color=CORAL))
        box.add_widget(button('Rever tutorial', lambda: (popup.dismiss(), self.tutorial())))
        box.add_widget(button('Voltar ao jogo', popup.dismiss, primary=True))
        popup.open()

    def investigation_card(self, evento):
        caso = evento['investigacao']
        card = Card(bg=PANEL2)
        card.add_widget(Text('APURAÇÃO ABERTA', size=11, color=MINT, bold=True))
        card.add_widget(Text('O grupo acusa. Você verifica.', size=21, bold=True))
        card.add_widget(Text('Cada consulta custa 2 de paciência, além do preço indicado. Acerte a conclusão com duas fontes verificadas: +8 de apoio e +4 de paciência. Acusação errada ou insuficiente: R$ 200 de retratação, -10 de apoio e -6 de paciência. Não há prêmio por adivinhar.', size=13))
        verificadas = sum(caso['provas'][i][2] for i in caso['consultadas'])
        card.add_widget(Text(f'Fontes verificadas consultadas: {verificadas}/2', size=12, color=MINT, bold=True))
        for i, (titulo, texto, confiavel) in enumerate(caso['provas']):
            if i in caso['consultadas']:
                card.add_widget(Text(titulo+(' · VERIFICADA' if confiavel else ' · BOATO'), size=13, bold=True, color=MINT if confiavel else AMBER))
                card.add_widget(Text(texto, size=14))
            else:
                card.add_widget(button(f'{titulo} · R$ {self.game.custo_pista(i)}', lambda i=i: self.acao(lambda: self.game.investigar(evento, i))))
        card.add_widget(Text('CONCLUIR A APURAÇÃO', size=11, color=MINT, bold=True))
        for i, nome in enumerate(caso['suspeitos']):
            card.add_widget(button(nome, lambda i=i: self.confirmar_acusacao(evento, i)))
        card.add_widget(button('Arquivar sem acusação · -2 paciência', lambda: self.acao(lambda: self.game.concluir_caso(evento, None))))
        card.add_widget(Text('Responder abaixo também encerra a apuração. Cobrança sem apurar gera retratação.', size=12, color=AMBER))
        self.content.add_widget(card)

    def confirmar_acusacao(self, evento, indice):
        popup, box = self.dialogo('Confirmar conclusão')
        caso = evento['investigacao']
        box.add_widget(Text(caso['suspeitos'][indice], size=22, bold=True))
        box.add_widget(Text('São necessárias duas fontes verificadas e uma conclusão correta. Uma acusação errada ou sem provas custa R$ 200, 10 de apoio e 6 de paciência.', size=15))
        box.add_widget(button('Registrar conclusão', lambda: (popup.dismiss(), self.acao(lambda: self.game.concluir_caso(evento, indice))), primary=True))
        box.add_widget(button('Voltar às pistas', popup.dismiss))
        popup.open()

    def groups_cards(self):
        self.content.add_widget(Text('PANELINHAS DO CONDOMÍNIO', size=12, color=MINT, bold=True))
        self.content.add_widget(Text('O apoio coletivo altera o voto de cada integrante em até 6 pontos. Mediação: +12 para um grupo, -2 para os demais; R$ 100 e 3 de paciência, uma vez por dia.', size=13, color=MUTED))
        for chave, grupo in PANELINHAS.items():
            card = Card(bg=PANEL2)
            card.add_widget(Text(grupo['nome']+f' · {self.game.panelinhas[chave]}%', size=19, bold=True))
            card.add_widget(Text(grupo['lema'], size=13, color=MUTED))
            card.add_widget(Text(' / '.join(grupo['membros']), size=12))
            card.add_widget(Text({'sossego': 'Prefere cobrança e silêncio. Rejeita deboche e improviso.', 'resenha': 'Prefere diálogo e tolerância. Rejeita multas.', 'planilha': 'Prefere investimentos e prestação de contas. Rejeita gastos improvisados.'}[chave], size=13))
            if self.game.mediacao_dia != self.game.dia:
                card.add_widget(button('Ouvir este grupo · R$ 100', lambda k=chave: self.acao(lambda: self.game.mediar_grupo(k))))
            self.content.add_widget(card)

    def transicao_dia(self):
        if getattr(self, 'transitando', False):
            return
        anterior = self.game.dia
        self.aba, self.ticket_selecionado = 'chat', None
        self.aviso = self.game.avancar_dia()
        self.salvar()
        self.render()
        if self.game.dia == anterior:
            return
        self.preferencias.tocar('dia', haptico=True)
        import os
        if not self.preferencias.valores['transicoes'] or os.environ.get('ZAP_QA_SEED'):
            return
        self.transitando = True
        box = stack(14, dp(22))
        box.add_widget(Text(f'DIA {self.game.dia:03d}', size=35, bold=True, color=MINT))
        frases = ['O café esquentou. O grupo também.', 'Você acordou. O grupo nunca dormiu.', 'Bom dia! Já tem áudio de três minutos.', 'Mais um dia sem silenciar todo mundo.', 'O elevador subiu. A pressão também.', 'A pauta de hoje já chegou com 47 mensagens.']
        box.add_widget(Text(frases[self.game.dia % len(frases)], size=17))
        popup = Popup(title='Um novo dia', content=box, auto_dismiss=False, size_hint=(.9, None), height=dp(220),
                      background='', background_color=BG, title_color=INK, separator_color=MINT)
        def fechar(_):
            popup.dismiss()
            self.transitando = False
        popup.open()
        from kivy.animation import Animation
        popup.opacity = 0
        Animation(opacity=1, duration=.18).start(popup)
        def apagar(_):
            animacao = Animation(opacity=0, duration=.15)
            animacao.bind(on_complete=lambda *_: fechar(None))
            animacao.start(popup)
        Clock.schedule_once(apagar, .7)
