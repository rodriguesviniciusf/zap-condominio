"""Um grupo, 365 dias e escolhas ruins: interface do Zap do Condomínio."""
import os
from pathlib import Path
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from game import SindicoGame
from ui import BG, PANEL, PANEL2, EDGE, INK, MUTED, MINT, AMBER, CORAL
from ui import Avatar, Card, CondoArt, Meter, TapCard, Text, button, row, stack

MONTH_NAMES = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
TYPE_NAMES = ('DIPLOMACIA', 'DEBOCHE', 'COBRANÇA', 'CONSELHO DO CAOS')
CATEGORIES = {'agua': 'ÁGUA', 'seguranca': 'SEGURANÇA', 'manutencao': 'MANUTENÇÃO',
              'barulho': 'BARULHO', 'garagem': 'GARAGEM', 'lixo': 'LIMPEZA',
              'convivencia': 'CONVIVÊNCIA', 'assembleia': 'ASSEMBLEIA', 'encomendas': 'ENTREGAS'}


def money(value):
    return f'{value:,.0f}'.replace(',', '.')


class ZapCondominioApp(App):
    def build(self):
        self.title = 'Zap do Condomínio'
        Window.clearcolor = BG
        self.game = SindicoGame()
        self.save_path = Path(os.environ.get('ZAP_SAVE_DIR', self.user_data_dir)) / 'mandato.json'
        self.aviso = ''
        self.tem_save = self.save_path.exists()
        if self.tem_save:
            try:
                self.game.carregar(self.save_path)
            except (OSError, ValueError, TypeError, KeyError):
                self.aviso = 'O save anterior não pôde ser lido. Um novo mandato está pronto.'
                self.tem_save = False
        self.aba, self.ticket_selecionado, self.no_menu = 'chat', None, True
        self.root = AnchorLayout(anchor_x='center', anchor_y='center')
        self.shell = BoxLayout(orientation='vertical', padding=(dp(16), dp(12)),
                               spacing=dp(10), size_hint_x=None)
        self.root.add_widget(self.shell)
        self.root.bind(width=lambda _, width: setattr(self.shell, 'width', min(width, dp(560))))
        self.shell.width = min(Window.width, dp(560))
        self.render()
        return self.root

    def salvar(self):
        try:
            self.game.salvar(self.save_path)
            self.tem_save = True
        except OSError:
            self.aviso = 'Não foi possível salvar agora. Confira o espaço livre do aparelho.'

    def scroll_area(self):
        self.scroll = ScrollView(do_scroll_x=False, bar_width=dp(3), bar_color=(*MINT[:3], .45))
        self.content = stack(12, (0, dp(2), 0, dp(10)))
        self.scroll.add_widget(self.content)
        self.shell.add_widget(self.scroll)

    def brand(self, pause=False):
        header = row(42)
        logo = Card(adaptive=False, radius=12, bg=MINT, stroke=MINT,
                    size_hint_x=None, width=dp(40), padding=0)
        logo.add_widget(Label(text='Z', font_size='25sp', bold=True, color=BG))
        header.add_widget(logo)
        header.add_widget(Text('ZAP DO\nCONDOMÍNIO', size=15, bold=True))
        if pause:
            btn = button('MENU', self.menu)
            btn.size_hint_x, btn.width, btn.height = None, dp(76), dp(40)
            header.add_widget(btn)
        else:
            tag = Text('365 DIAS\nDE MANDATO', size=10, color=MUTED)
            tag.size_hint_x, tag.width = None, dp(88)
            header.add_widget(tag)
        self.shell.add_widget(header)

    def render(self):
        self.shell.clear_widgets()
        if self.no_menu:
            self.render_menu()
        else:
            self.render_game()

    def render_menu(self):
        self.brand()
        self.scroll_area()
        self.content.add_widget(Text('SIMULADOR DE SÍNDICO', size=10, color=MINT, bold=True))
        self.content.add_widget(CondoArt(size_hint_y=None, height=dp(190)))
        self.content.add_widget(Text('O cargo é seu.\nO caos é de todos.', size=32, bold=True))
        self.content.add_widget(Text('Sobreviva a um ano de boletos, vizinhos e conselhos que ninguém deveria ouvir.',
                                     size=15, color=MUTED))
        summary = Card(spacing=dp(7))
        summary.add_widget(Text('UM GRUPO. NENHUMA PAZ.', size=10, bold=True, color=MINT))
        summary.add_widget(Text('365 situações / 1.460 escolhas / 3 conselheiros', size=12))
        if self.tem_save:
            summary.add_widget(Text(f'Mandato salvo · dia {self.game.dia} · R$ {money(self.game.caixa)}',
                                    size=12, color=MUTED))
        self.content.add_widget(summary)
        if self.aviso:
            self.content.add_widget(Text(self.aviso, size=12, color=AMBER))
        title = 'Continuar mandato' if self.tem_save and self.game.jogo_ativo else (
            'Ver resultado' if not self.game.jogo_ativo else 'Assumir o grupo')
        self.shell.add_widget(button(title+'   >', self.iniciar, primary=True))
        if self.tem_save:
            self.shell.add_widget(button('Novo mandato', self.confirmar_reinicio))
        self.shell.add_widget(Text('Seu progresso é salvo neste aparelho.', size=11, color=MUTED))

    def render_game(self):
        g = self.game
        self.brand(pause=True)
        event = g.evento_atual
        month = event.get('mes', min(12, (g.dia-1)//30+1))
        timeline = row(20)
        timeline.add_widget(Text(f'{MONTH_NAMES[month-1].upper()} / MÊS {month:02d}',
                                 size=10, color=MUTED, bold=True))
        day = Text(f'DIA {g.dia:03d} / 365', size=11, color=MINT, bold=True)
        day.size_hint_x, day.width = None, dp(104)
        timeline.add_widget(day)
        self.shell.add_widget(timeline)
        self.shell.add_widget(Meter(value=g.dia/365*100))
        metrics = row(80, 7)
        stats = [('CAIXA', 'R$ '+money(g.caixa), None, MINT),
                 ('PACIÊNCIA', f'{g.paciencia}%', g.paciencia, CORAL if g.paciencia < 30 else MINT),
                 ('APROVAÇÃO', f'{g.aprovacao}%', g.aprovacao, AMBER)]
        for name, value, percent, accent in stats:
            metric = Card(adaptive=False, radius=13, padding=dp(10), spacing=dp(3))
            metric.add_widget(Text(name, size=9, color=MUTED, bold=True))
            metric.add_widget(Text(value, size=16 if name == 'CAIXA' else 20, bold=True, color=accent))
            metric.add_widget(Meter(value=percent, accent=accent) if percent is not None
                              else Text('saldo disponível', size=8, color=MUTED))
            metrics.add_widget(metric)
        self.shell.add_widget(metrics)
        self.scroll_area()
        if not g.jogo_ativo:
            self.render_result()
        elif self.aba == 'chat':
            self.render_chat()
        elif self.aba == 'pendencias':
            self.render_pending()
        else:
            self.render_management()
        if g.jogo_ativo:
            caption = 'Encerrar o dia   >' if g.encerrado else 'Adiar chamado e encerrar o dia   >'
            self.shell.add_widget(button(caption, self.avancar, primary=g.encerrado))
        nav = row(44, 7)
        for title, tab in [('CHAT', 'chat'), (f'CHAMADOS {len(g.pendencias)}', 'pendencias'), ('GESTÃO', 'gestao')]:
            selected = self.aba == tab
            item = button(title, lambda tab=tab: self.mudar_aba(tab), font=11)
            item.bg = item.rest = list(PANEL2 if selected else BG)
            item.stroke, item.height = (MINT if selected else BG), dp(44)
            nav.add_widget(item)
        self.shell.add_widget(nav)
        self.content.opacity = 0
        Animation(opacity=1, duration=.16).start(self.content)

    def section(self, eyebrow, title, subtitle=None):
        self.content.add_widget(Text(eyebrow, size=10, color=MINT, bold=True))
        self.content.add_widget(Text(title, size=23, bold=True))
        if subtitle:
            self.content.add_widget(Text(subtitle, size=13, color=MUTED))

    def notice(self):
        if self.aviso:
            card = Card(bg=(.08, .19, .18, 1), stroke=(.17, .35, .29, 1), padding=dp(12))
            card.add_widget(Text('RESPOSTA DO GRUPO', size=9, bold=True, color=MINT))
            card.add_widget(Text(self.aviso, size=13))
            self.content.add_widget(card)

    def render_chat(self):
        g = self.game
        event = g.evento_atual
        self.content.add_widget(Text(event.get('capitulo', 'Zap da Gestão').upper(),
                                     size=10, bold=True, color=MUTED))
        self.notice()
        if g.consequencias:
            self.content.add_widget(Text(f'{len(g.consequencias)} conselho(s) com efeito futuro. A conta ainda vem.',
                                         size=11, color=AMBER))
        self.event_card(event)
        if g.encerrado:
            card = Card(bg=(.08, .19, .18, 1))
            card.add_widget(Text('Chamado resolvido.', size=18, bold=True, color=MINT))
            card.add_widget(Text('Cuide das pendências ou encerre o dia. Amanhã tem mais.', size=13, color=MUTED))
            self.content.add_widget(card)
        else:
            self.choices(event)

    def event_card(self, event):
        card = Card(bg=PANEL2, padding=dp(15), spacing=dp(9))
        header = row(38)
        name = event['remetente']
        header.add_widget(Avatar(''.join(part[0] for part in name.split()[:2])))
        names = stack(0)
        names.add_widget(Text(name, size=13, bold=True))
        names.add_widget(Text('GRUPO DOS MORADORES · 08:32', size=9, color=MUTED))
        header.add_widget(names)
        card.add_widget(header)
        card.add_widget(Text(event.get('titulo', 'Ocorrência no condomínio'), size=20, bold=True))
        card.add_widget(Text(event['mensagem'], size=15))
        category = CATEGORIES.get(event['categoria'], event['categoria'].upper())
        card.add_widget(Text(f"{category} / CHAMADO DO DIA {event.get('abertura', self.game.dia)}",
                             size=9, color=MUTED, bold=True))
        self.content.add_widget(card)

    def choices(self, event):
        self.content.add_widget(Text('COMO VOCÊ VAI RESPONDER?', size=10, color=MUTED, bold=True))
        for index, option in enumerate(event['opcoes']):
            chaos = index == 3
            card = TapCard(action=lambda e=event, i=index: self.responder(e, i),
                           bg=(.18, .145, .11, 1) if chaos else PANEL,
                           stroke=(.42, .32, .18, 1) if chaos else EDGE,
                           padding=dp(13), spacing=dp(5), radius=15)
            label = event.get('conselheiro', 'CONSELHO')+' / PALPITE DO CAOS' if chaos else TYPE_NAMES[index]
            card.add_widget(Text(f'0{index+1}   {label}', size=9, color=AMBER if chaos else MINT, bold=True))
            message = option['texto']
            for prefix in ('Passiva: ', 'Debochada: ', 'Multa: ', 'Conselho: '):
                if message.startswith(prefix):
                    message = message[len(prefix):]
            if chaos and event['dia'] <= 12:
                message = event['conselheiro_pitaco'].split(': ', 1)[-1]
            card.add_widget(Text(message, size=14))
            cash = option.get('caixa_condominio', 0)
            if self.game.tem_cameras and event['categoria'] == 'seguranca' and cash < 0:
                cash = round(cash*.5)
            effect = f"R$ {cash:+.0f} · paciência {option.get('paciencia_sindico', 0):+d} · aprovação {option.get('aprovacao', 0):+d}"
            card.add_widget(Text(effect, size=10, color=MUTED))
            if chaos:
                card.add_widget(Text('Parece fácil. A conta chega depois.', size=10, color=AMBER))
            self.content.add_widget(card)

    def render_pending(self):
        g = self.game
        self.section('CENTRAL DE CHAMADOS', 'Nada fica esquecido.',
                     'Cada pendência cobra 1 ponto de paciência e aprovação ao encerrar o dia, até 12 por dia.')
        self.notice()
        if not g.pendencias:
            card = Card()
            card.add_widget(Text('Fila zerada.', size=22, color=MINT, bold=True))
            card.add_widget(Text('Aproveite a paz. O grupo está digitando...', size=14, color=MUTED))
            self.content.add_widget(card)
        for event in g.pendencias:
            selected = event['ticket'] == self.ticket_selecionado
            card = TapCard(action=lambda t=event['ticket']: self.selecionar(t), bg=PANEL2 if selected else PANEL)
            card.add_widget(Text(f"ABERTO NO DIA {event['abertura']:03d}", size=9, color=AMBER, bold=True))
            card.add_widget(Text(event.get('titulo', event['remetente']), size=16, bold=True))
            card.add_widget(Text(event['remetente']+' / '+('Fechar detalhes' if selected else 'Toque para resolver >'),
                                 size=11, color=MUTED))
            self.content.add_widget(card)
            if selected:
                self.event_card(event)
                self.choices(event)

    def render_management(self):
        g = self.game
        self.section('SALA DA GESTÃO', 'O caixa não se cuida sozinho.')
        self.notice()
        budget = Card()
        budget.add_widget(Text('PRÓXIMO FECHAMENTO', size=9, color=MUTED, bold=True))
        next_day = ((g.dia-1)//30+1)*30+1
        budget.add_widget(Text('Dia '+str(next_day) if next_day <= 365 else 'Mandato em fase final', size=22, bold=True))
        budget.add_widget(Text('Taxas: R$ 12.000 / Despesas: R$ 9.000\nA inadimplência reduz a receita conforme a aprovação.',
                              size=13, color=MUTED))
        self.content.add_widget(budget)
        cameras = Card()
        cameras.add_widget(Text('MELHORIA DO CONDOMÍNIO', size=9, color=MINT, bold=True))
        cameras.add_widget(Text('Câmeras de segurança', size=20, bold=True))
        cameras.add_widget(Text('Metade do custo imediato das escolhas em segurança. Não anula a consequência dos conselhos.',
                               size=13, color=MUTED))
        cameras.add_widget(Text('INSTALADAS E FUNCIONANDO', size=11, color=MINT, bold=True) if g.tem_cameras
                           else button('Instalar por R$ 1.500', self.comprar, primary=True))
        self.content.add_widget(cameras)
        self.content.add_widget(Text('LIVRO DE OCORRÊNCIAS', size=10, color=MUTED, bold=True))
        if not g.historico:
            self.content.add_widget(Text('O livro ainda está em branco. Aproveite para respirar.', size=13, color=MUTED))
        for item in reversed(g.historico[-20:]):
            entry = Card(padding=dp(12), radius=12, spacing=dp(4))
            entry.add_widget(Text(f"DIA {item['dia']:03d}", size=9, color=MINT, bold=True))
            entry.add_widget(Text(item['texto'], size=13))
            self.content.add_widget(entry)

    def render_result(self):
        g = self.game
        self.content.add_widget(CondoArt(size_hint_y=None, height=dp(140)))
        self.section('FIM DE MANDATO', 'Você sobreviveu ao grupo.' if g.vitoria else 'O grupo venceu desta vez.',
                     '365 dias. Uma história para a próxima assembleia.' if g.vitoria else (
                         'A paciência acabou antes do mandato.' if g.paciencia <= 0 else 'O caixa ficou negativo.'))
        card = Card()
        card.add_widget(Text(f'Dia {g.dia} · R$ {money(g.caixa)} em caixa', size=18, bold=True))
        card.add_widget(Text(f'Aprovação {g.aprovacao}% · {len(g.pendencias)} chamado(s) aberto(s)', size=13, color=MUTED))
        self.content.add_widget(card)
        self.content.add_widget(button('Tentar outro mandato', self.confirmar_reinicio, primary=True))

    def iniciar(self):
        self.no_menu = False
        self.salvar()
        self.render()

    def menu(self):
        self.no_menu = True
        self.salvar()
        self.render()

    def mudar_aba(self, aba):
        self.aba, self.ticket_selecionado = aba, None
        self.render()

    def selecionar(self, ticket):
        self.ticket_selecionado = None if self.ticket_selecionado == ticket else ticket
        self.render()

    def responder(self, evento, indice):
        self.aviso = self.game.responder_evento(evento, indice)
        self.ticket_selecionado = None
        self.salvar()
        self.render()

    def avancar(self):
        antes = len(self.game.historico)
        self.game.avancar_dia()
        self.aviso = '\n'.join(item['texto'] for item in self.game.historico[antes:])
        self.ticket_selecionado, self.aba = None, 'chat'
        self.salvar()
        self.render()

    def comprar(self):
        self.aviso = 'Câmeras instaladas. O grupo já quer fiscalizar o fiscal.' if self.game.comprar_cameras() else 'O caixa precisa de R$ 1.500 para instalar as câmeras.'
        self.salvar()
        self.render()

    def confirmar_reinicio(self):
        box = stack(12, dp(16))
        box.add_widget(Text('Começar do dia 1 substitui o mandato salvo neste aparelho.', size=15))
        popup = Popup(title='Novo mandato?', content=box, size_hint=(.9, None), height=dp(300),
                      background_color=BG, separator_color=MINT)
        def reiniciar():
            popup.dismiss()
            self.game = SindicoGame()
            self.aba, self.aviso, self.ticket_selecionado, self.no_menu = 'chat', '', None, False
            self.salvar()
            self.render()
        box.add_widget(button('Começar novo mandato', reiniciar, primary=True))
        box.add_widget(button('Continuar o atual', popup.dismiss))
        popup.open()

    def on_pause(self):
        self.salvar()
        return True

    def on_stop(self):
        if hasattr(self, 'game') and hasattr(self, 'save_path'):
            self.salvar()


if __name__ == '__main__':
    ZapCondominioApp().run()
