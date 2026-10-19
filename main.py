"""Zap do Condomínio: elenco ilustrado e gestão de um mandato imprevisível."""
import os
from pathlib import Path
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from game import SindicoGame
from lore import PERFIS, CONSELHEIROS, MELHORIAS, MESES, calendario
from ui import BG, PANEL, PANEL2, EDGE, INK, MUTED, MINT, AMBER, CORAL
from ui import Card, Cover, Icon, Meter, Portrait, TapCard, Text, button, row, stack

CATEGORIAS = {'agua': 'ÁGUA', 'seguranca': 'SEGURANÇA', 'manutencao': 'MANUTENÇÃO',
              'barulho': 'BARULHO', 'garagem': 'GARAGEM', 'lixo': 'LIMPEZA',
              'convivencia': 'CONVIVÊNCIA', 'assembleia': 'ASSEMBLEIA', 'encomendas': 'ENTREGAS'}
TIPOS = dict(passiva='DIPLOMACIA', debochada='DEBOCHE', multa='COBRANÇA',
             conselho='CONSELHO DO CAOS', melhoria='SOLUÇÃO DESBLOQUEADA')


def money(value):
    return f'{value:,.0f}'.replace(',', '.')


class ZapCondominioApp(App):
    def build(self):
        self.title = 'Zap do Condomínio'
        Window.clearcolor = BG
        seed = os.environ.get('ZAP_QA_SEED')
        self.game = SindicoGame(seed=int(seed) if seed else None)
        self.save_path = Path(os.environ.get('ZAP_SAVE_DIR', self.user_data_dir))/'mandato.json'
        self.aviso = ''
        self.tem_save = self.save_path.exists()
        if self.tem_save:
            try:
                self.game.carregar(self.save_path)
            except (OSError, ValueError, TypeError, KeyError):
                self.tem_save = False
                self.aviso = 'Não foi possível abrir o save. Um novo mandato está pronto.'
        self.aba, self.ticket_selecionado, self.no_menu = 'chat', None, True
        self.root = AnchorLayout()
        with self.root.canvas.before:
            Color(*BG)
            self.background = Rectangle(pos=self.root.pos, size=self.root.size)
        self.root.bind(pos=self.paint_background, size=self.paint_background)
        self.shell = BoxLayout(orientation='vertical', spacing=dp(9),
                               padding=(dp(14), dp(12)), size_hint_x=None)
        self.root.add_widget(self.shell)
        self.root.bind(width=lambda _, w: setattr(self.shell, 'width', min(w, dp(560))))
        self.shell.width = min(Window.width, dp(560))
        self.render()
        return self.root

    def paint_background(self, *_):
        self.background.pos, self.background.size = self.root.pos, self.root.size

    def salvar(self):
        try:
            self.game.salvar(self.save_path)
            self.tem_save = True
        except OSError:
            self.aviso = 'Não foi possível salvar. Confira o espaço disponível no aparelho.'

    def scroll_area(self):
        self.scroll = ScrollView(do_scroll_x=False, bar_width=dp(3), bar_color=(*MINT[:3], .4))
        self.content = stack(11, (0, dp(3), 0, dp(10)))
        self.scroll.add_widget(self.content)
        self.shell.add_widget(self.scroll)

    def brand(self, pause=False):
        header = row(42)
        mark = Card(adaptive=False, bg=MINT, stroke=MINT, radius=12,
                    size_hint_x=None, width=dp(40), padding=0)
        mark.add_widget(Label(text='Z', bold=True, font_size='27sp', color=(1, 1, .96, 1)))
        header.add_widget(mark)
        header.add_widget(Text('ZAP DO\nCONDOMÍNIO', size=15, bold=True))
        if pause:
            b = button('MENU', self.menu, font=11)
            b.size_hint_x, b.width, b.height = None, dp(66), dp(38)
            header.add_widget(b)
        else:
            t = Text('VILA DO\nSOSSEGO', size=10, color=MUTED, bold=True)
            t.size_hint_x, t.width = None, dp(80)
            header.add_widget(t)
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
        self.content.add_widget(Text('UM GRUPO. OITO VIZINHOS. ZERO SOSSEGO.', size=10, color=MINT, bold=True))
        self.content.add_widget(Cover(size_hint_y=None, height=dp(235)))
        self.content.add_widget(Text('Seu mandato.\nO caos de todos.', size=33, bold=True))
        self.content.add_widget(Text('Converse, negocie e sobreviva a 365 dias. Cada mandato embaralha as histórias. Os moradores lembram das suas escolhas.',
                                     size=14, color=MUTED))
        cast = Card(orientation='horizontal', adaptive=False, height=dp(80), padding=dp(10), spacing=dp(8), bg=PANEL2)
        for name in CONSELHEIROS:
            cast.add_widget(Portrait(name, diameter=52))
        notes = stack(2)
        notes.add_widget(Text('O CONSELHO', size=10, color=MINT, bold=True))
        notes.add_widget(Text('Ajuda que sai caro.', size=12))
        cast.add_widget(notes)
        self.content.add_widget(cast)
        if self.tem_save:
            self.content.add_widget(Text(f'Dia {self.game.dia} salvo · R$ {money(self.game.caixa)} · apoio {self.game.aprovacao}%',
                                         size=12, color=MUTED))
        if self.aviso:
            self.content.add_widget(Text(self.aviso, size=12, color=CORAL))
        self.shell.add_widget(button('Continuar mandato' if self.tem_save else 'Assumir o grupo', self.iniciar, primary=True))
        if self.tem_save:
            self.shell.add_widget(button('Novo mandato · novos problemas', self.confirmar_reinicio))
        self.shell.add_widget(Text('Continuar mantém a partida. Novo mandato embaralha tudo.', size=10, color=MUTED))

    def render_game(self):
        g = self.game
        self.brand(pause=True)
        month, day_month = calendario(g.dia)
        time = row(18)
        time.add_widget(Text(f'{day_month:02d} DE {MESES[month-1].upper()}', size=10, color=MUTED, bold=True))
        label = Text(f'DIA {g.dia:03d} / 365', size=11, color=MINT, bold=True)
        label.size_hint_x, label.width = None, dp(102)
        time.add_widget(label)
        self.shell.add_widget(time)
        metrics = row(70, 7)
        for title, value, percent, color in [('CAIXA', 'R$ '+money(g.caixa), None, MINT),
                ('PACIÊNCIA', f'{g.paciencia}%', g.paciencia, CORAL if g.paciencia < 30 else MINT),
                ('APROVAÇÃO', f'{g.aprovacao}%', g.aprovacao, CORAL if g.aprovacao < 20 else AMBER)]:
            card = Card(adaptive=False, radius=14, padding=dp(9), spacing=dp(2))
            card.add_widget(Text(title, size=9, color=MUTED, bold=True))
            card.add_widget(Text(value, size=16 if percent is None else 20, color=color, bold=True))
            card.add_widget(Meter(value=g.dia/365*100 if percent is None else percent, accent=color))
            metrics.add_widget(card)
        self.shell.add_widget(metrics)
        self.scroll_area()
        if not g.jogo_ativo:
            self.render_result()
        elif self.aba == 'chat':
            self.render_chat()
        elif self.aba == 'pendencias':
            self.render_pending()
        elif self.aba == 'moradores':
            self.render_people()
        else:
            self.render_management()
        if g.jogo_ativo:
            if g.assembleia:
                self.shell.add_widget(button('Assembleia aberta · decidir agora', lambda: self.mudar_aba('pendencias'), primary=True))
            else:
                self.shell.add_widget(button('Encerrar o dia  >' if g.encerrado else 'Deixar para amanhã  >',
                                             self.avancar, primary=g.encerrado))
        nav = row(48, 4)
        for title, tab, icon in [('GRUPO', 'chat', 'chat'), ('PAUTAS', 'pendencias', 'board'),
                                  ('GENTE', 'moradores', 'people'), ('PRÉDIO', 'gestao', 'building')]:
            active = self.aba == tab
            item = TapCard(action=lambda a=tab: self.mudar_aba(a), adaptive=False, height=dp(48),
                           padding=dp(4), spacing=dp(1), radius=13,
                           bg=PANEL2 if active else BG, stroke=MINT if active else BG)
            center = AnchorLayout(size_hint_y=None, height=dp(23))
            center.add_widget(Icon(icon, accent=MINT if active else MUTED))
            item.add_widget(center)
            text = Label(text=title, font_size='9sp', bold=True, color=MINT if active else MUTED, size_hint_y=None, height=dp(13))
            item.add_widget(text)
            nav.add_widget(item)
        self.shell.add_widget(nav)

    def section(self, eyebrow, title, subtitle=None):
        self.content.add_widget(Text(eyebrow, size=10, color=MINT, bold=True))
        self.content.add_widget(Text(title, size=24, bold=True))
        if subtitle:
            self.content.add_widget(Text(subtitle, size=13, color=MUTED))

    def notice(self):
        if self.aviso:
            card = Card(bg=PANEL2, padding=dp(12), radius=14, spacing=dp(4))
            card.add_widget(Text('ÚLTIMA MOVIMENTAÇÃO', size=9, color=MINT, bold=True))
            card.add_widget(Text(self.aviso, size=13))
            self.content.add_widget(card)

    def render_chat(self):
        g = self.game
        self.content.add_widget(Cover(size_hint_y=None, height=dp(118)))
        self.content.add_widget(Text(f'VILA DO SOSSEGO  /  {len(g.pendencias)} PAUTA(S) ABERTA(S)', size=10, color=MUTED, bold=True))
        self.notice()
        if g.assembleia:
            self.assembly_card()
            return
        if g.dias_revolta:
            self.content.add_widget(Text(f'REVOLTA: {g.dias_revolta}/3 dias com apoio abaixo de 20%. Uma assembleia pode encerrar o mandato.',
                                         size=12, color=CORAL, bold=True))
        event = g.evento_foco
        if event.get('tipo_evento') == 'crise':
            self.content.add_widget(Text(f"CRISE · ETAPA {event['etapa']}/2 · PRAZO DIA {event['prazo']}", size=11, color=CORAL, bold=True))
            self.event_card(event)
            self.choices(event)
        else:
            self.event_card(g.evento_atual)
            if g.encerrado:
                done = Card(bg=PANEL2)
                done.add_widget(Text('Resolvido por hoje.', size=21, color=MINT, bold=True))
                done.add_widget(Text('As outras pautas e a gestão continuam disponíveis.', size=13, color=MUTED))
                self.content.add_widget(done)
            else:
                name = event.get('conselheiro', 'Toninho')
                pitaco = Card(bg=(1, .94, .80, 1), stroke=(.89, .75, .48, 1), spacing=dp(6))
                head = row(52)
                head.add_widget(Portrait(name, diameter=52))
                names = stack(1)
                names.add_widget(Text(name, size=15, bold=True))
                names.add_widget(Text(CONSELHEIROS.get(name, {}).get('papel', 'Conselho do caos'), size=10, color=AMBER))
                head.add_widget(names)
                pitaco.add_widget(head)
                pitaco.add_widget(Text(event['conselheiro_pitaco'].split(': ', 1)[-1], size=14, italic=True))
                self.content.add_widget(pitaco)
                self.choices(event)

    def event_card(self, event):
        card = Card(padding=dp(15), spacing=dp(8))
        head = row(51)
        name = event['remetente']
        head.add_widget(Portrait(name, diameter=50))
        names = stack(1)
        names.add_widget(Text(name, size=14, bold=True))
        names.add_widget(Text(PERFIS.get(name, {}).get('papel', 'Morador do condomínio'), size=10, color=MUTED))
        head.add_widget(names)
        card.add_widget(head)
        card.add_widget(Text(event.get('titulo', 'Mensagem no grupo'), size=21, bold=True))
        card.add_widget(Text(event['mensagem'], size=15))
        resident = self.game.moradores.get(name)
        if resident:
            mood = 'Ainda confio na gestão.' if resident['confianca'] >= 65 else (
                'Estou guardando os prints.' if resident['irritacao'] >= 40 else 'Vamos ver como você resolve.')
            card.add_widget(Text(mood, size=11, color=MINT if resident['confianca'] >= 65 else MUTED, italic=True))
            card.add_widget(Text(f"Confiança {resident['confianca']}% · irritação {resident['irritacao']}%", size=10, color=MUTED))
        category = CATEGORIAS.get(event['categoria'], event['categoria'].upper())
        card.add_widget(Text(category+' / '+('CRISE DO CONSELHO' if event.get('tipo_evento') == 'crise' else 'ZAP DA GESTÃO'), size=9, color=MINT, bold=True))
        self.content.add_widget(card)

    def choices(self, event):
        self.content.add_widget(Text('ESCOLHA SUA RESPOSTA', size=10, color=MUTED, bold=True))
        for index, option in enumerate(self.game.opcoes_evento(event)):
            kind = option.get('tipo', ('passiva', 'debochada', 'multa', 'conselho')[min(index, 3)])
            chaos = kind == 'conselho'
            card = TapCard(action=lambda e=event, i=index: self.responder(e, i), radius=16,
                           bg=(1, .94, .80, 1) if chaos else (PANEL2 if kind == 'melhoria' else PANEL),
                           stroke=(.88, .71, .39, 1) if chaos else EDGE, padding=dp(13), spacing=dp(5))
            card.add_widget(Text(f'{index+1:02d} / '+TIPOS.get(kind, kind.upper()), size=9,
                                 color=AMBER if chaos else MINT, bold=True))
            message = option['texto']
            for prefix in ('Passiva: ', 'Debochada: ', 'Multa: ', 'Conselho: '):
                if message.startswith(prefix):
                    message = message[len(prefix):]
            if chaos and event.get('tipo_evento') != 'crise':
                message = f"Seguir o plano de {event.get('conselheiro', 'Toninho')}."
            card.add_widget(Text(message, size=14))
            impact = self.game.impacto_opcao(event, option)
            card.add_widget(Text(f"R$ {impact['caixa']:+.0f}  /  paciência {impact['paciencia']:+d}  /  apoio {impact['aprovacao']:+d}", size=10, color=MUTED))
            if chaos:
                card.add_widget(Text('Pode abrir outra crise nos próximos dias.', size=10, color=AMBER))
            self.content.add_widget(card)

    def assembly_card(self):
        g = self.game
        crisis = g.assembleia['tipo'] == 'crise'
        self.section('MANDATO EM JOGO' if crisis else 'ASSEMBLEIA DO MÊS', g.assembleia['titulo'],
                     'A maioria precisa apoiar um plano. Rejeição na crise encerra o mandato.' if crisis else
                     'A confiança e a irritação dos moradores decidem o voto. Maioria: 5 de 8.')
        crowd = Card(orientation='horizontal', adaptive=False, height=dp(51), padding=dp(8), spacing=dp(5))
        for name in PERFIS:
            crowd.add_widget(Portrait(name, diameter=29))
        self.content.add_widget(crowd)
        for i, proposal in enumerate(g.propostas()):
            votes = g.prever_votos(proposal)
            support = sum(v['sim'] for v in votes)
            card = TapCard(action=lambda i=i: self.acao(lambda: self.game.votar(i)),
                           stroke=CORAL if crisis else EDGE, padding=dp(14))
            card.add_widget(Text(proposal['titulo'], size=18, bold=True))
            card.add_widget(Text(proposal['texto'], size=13, color=MUTED))
            card.add_widget(Text(f"Apoio: {support}/8 · custo R$ {proposal['custo']} · receita R$ {proposal['receita']}",
                                 size=11, color=MINT if support >= 5 else CORAL, bold=True))
            if proposal['custo'] > g.caixa:
                card.add_widget(Text('Caixa insuficiente para este plano.', size=11, color=CORAL))
            self.content.add_widget(card)

    def render_pending(self):
        g = self.game
        self.notice()
        if g.assembleia:
            self.assembly_card()
        else:
            self.section('PAUTAS DO CONDOMÍNIO', 'O grupo não esquece.',
                         'Pendências desgastam o mandato. Crises do conselho têm prazo e reparação emergencial se forem ignoradas.')
        for event in g.pendencias:
            crisis = event.get('tipo_evento') == 'crise'
            selected = self.ticket_selecionado == event['ticket']
            card = TapCard(action=lambda t=event['ticket']: self.selecionar(t), stroke=CORAL if crisis else EDGE)
            card.add_widget(Text(f"CRISE · PRAZO DIA {event['prazo']}" if crisis else f"ABERTO NO DIA {event['abertura']}",
                                 size=10, color=CORAL if crisis else AMBER, bold=True))
            card.add_widget(Text(event.get('titulo', event['remetente']), size=17, bold=True))
            card.add_widget(Text(event['remetente']+' · toque para resolver', size=11, color=MUTED))
            self.content.add_widget(card)
            if selected and not g.assembleia:
                self.event_card(event)
                self.choices(event)
        if not g.pendencias and not g.assembleia:
            self.content.add_widget(Text('Fila zerada. Aproveite este raro momento.', size=16, color=MINT))
        if g.consequencias:
            self.content.add_widget(Text(f'{len(g.consequencias)} plano(s) do conselho ainda podem trazer consequências.', size=12, color=AMBER))
        if g.ultima_votacao:
            vote = g.ultima_votacao
            self.section('ATA MAIS RECENTE', f"{vote['sim']}/{vote['total']} votos a favor", vote['titulo'])
            for item in vote['votos']:
                card = Card(orientation='horizontal', adaptive=False, height=dp(55), padding=dp(8))
                card.add_widget(Portrait(item['nome'], diameter=36))
                card.add_widget(Text(item['nome']+' · '+('SIM' if item['sim'] else 'NÃO'), size=12, color=MINT if item['sim'] else CORAL))
                self.content.add_widget(card)

    def render_people(self):
        self.section('QUEM MORA AO LADO', 'Cada vizinho tem memória.',
                     'Confiança ajuda nas votações. Deboche e multas acumulam irritação. Uma conversa de mediação por dia.')
        self.notice()
        for name, profile in PERFIS.items():
            state = self.game.moradores[name]
            card = Card(spacing=dp(8))
            head = row(58)
            head.add_widget(Portrait(name, diameter=58))
            names = stack(2)
            names.add_widget(Text(name, size=17, bold=True))
            names.add_widget(Text(profile['papel'], size=11, color=MUTED))
            head.add_widget(names)
            card.add_widget(head)
            card.add_widget(Text(f"Confiança {state['confianca']}% / irritação {state['irritacao']}%", size=12, color=MUTED))
            card.add_widget(Meter(value=state['confianca']))
            card.add_widget(Text(state['ultima'], size=12, color=MUTED))
            if not self.game.social_dia:
                card.add_widget(button('Conversar · R$ 120', lambda n=name: self.acao(lambda: self.game.reconciliar(n))))
            self.content.add_widget(card)

    def render_management(self):
        g = self.game
        self.section('NOSSO CONDOMÍNIO', 'Invista em menos caos.',
                     'Melhorias desbloqueiam soluções nos chamados e têm custos mensais visíveis.')
        self.notice()
        actions = Card(bg=PANEL2)
        actions.add_widget(Text('CUIDE DA GESTÃO', size=11, color=MINT, bold=True))
        actions.add_widget(Text('Pausa ou ajuda profissional. Uma utilização de cada por dia.', size=13, color=MUTED))
        actions.add_widget(button('Descansar · R$ 180 · +14 paciência' if not g.descanso_dia else 'Descanso já usado hoje',
                                  lambda: self.acao(g.descansar)))
        actions.add_widget(button(f"Delegar chamado · R$ {160 if g.melhorias['portaria'] else 240}" if not g.delegacao_dia else 'Delegação já usada hoje',
                                  lambda: self.acao(g.delegar)))
        self.content.add_widget(actions)
        for key, spec in MELHORIAS.items():
            card = Card(stroke=MINT if g.melhorias[key] else EDGE)
            card.add_widget(Text('INSTALADO' if g.melhorias[key] else 'MELHORIA DISPONÍVEL', size=9, color=MINT, bold=True))
            card.add_widget(Text(spec['nome'], size=21, bold=True))
            card.add_widget(Text(spec['resumo'], size=13, color=MUTED))
            card.add_widget(Text(f"Compra R$ {spec['custo']} / mensal R$ {spec['mensal']}", size=11, color=MUTED))
            if not g.melhorias[key]:
                card.add_widget(button('Instalar melhoria', lambda key=key: self.comprar(key), primary=True))
            self.content.add_widget(card)
        budget = Card()
        budget.add_widget(Text('FECHAMENTO A CADA 30 DIAS', size=10, color=MINT, bold=True))
        budget.add_widget(Text(f'Despesas R$ {money(g.custo_mensal)} / mês', size=20, bold=True))
        budget.add_widget(Text('Taxas previstas: R$ 12.000. A inadimplência cresce quando o apoio cai.', size=13, color=MUTED))
        self.content.add_widget(budget)
        self.content.add_widget(Text('LIVRO DE OCORRÊNCIAS', size=10, color=MINT, bold=True))
        for item in reversed(g.historico[-12:]):
            entry = Card(radius=13, padding=dp(12), spacing=dp(4))
            entry.add_widget(Text(f"DIA {item['dia']:03d}", size=9, color=MINT, bold=True))
            entry.add_widget(Text(item['texto'], size=13))
            self.content.add_widget(entry)

    def render_result(self):
        g = self.game
        self.content.add_widget(Cover(size_hint_y=None, height=dp(175)))
        self.section('MANDATO CONCLUÍDO' if g.vitoria else 'FIM DO MANDATO', g.titulo_final,
                     'Você sobreviveu aos 365 dias do grupo.' if g.vitoria else
                     {'destituicao': 'A assembleia votou pelo fim da sua gestão.',
                      'caixa': 'O caixa ficou negativo.', 'paciencia': 'A paciência acabou.'}.get(g.fim_motivo, 'O mandato terminou.'))
        card = Card()
        card.add_widget(Text(f'Dia {g.dia} / R$ {money(g.caixa)}', size=21, bold=True))
        card.add_widget(Text(f'Apoio {g.aprovacao}% · {len(g.pendencias)} pauta(s) abertas', size=13, color=MUTED))
        self.content.add_widget(card)
        self.content.add_widget(button('Outro mandato, outra história', self.confirmar_reinicio, primary=True))

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

    def acao(self, callback):
        self.aviso = callback()
        self.salvar()
        self.render()

    def responder(self, evento, indice):
        self.ticket_selecionado = None
        self.acao(lambda: self.game.responder_evento(evento, indice))

    def avancar(self):
        self.aba, self.ticket_selecionado = 'chat', None
        self.acao(self.game.avancar_dia)

    def comprar(self, key='cameras'):
        self.aviso = (MELHORIAS[key]['nome']+' instalado.') if self.game.comprar_melhoria(key) else 'Melhoria já instalada ou caixa insuficiente.'
        self.salvar()
        self.render()

    def confirmar_reinicio(self):
        box = stack(12, dp(16))
        box.add_widget(Text('Novo mandato substitui o save e sorteia novas histórias. Continuar preserva sua partida.', size=14))
        popup = Popup(title='Começar outro mandato?', content=box, size_hint=(.92, None), height=dp(300),
                      background='', background_color=BG, title_color=INK, separator_color=MINT)
        def reiniciar():
            popup.dismiss()
            first = self.game.vistos[0] if self.game.vistos else self.game.evento_atual['id']
            self.game = SindicoGame(evitar_inicio=first)
            self.aba, self.aviso, self.ticket_selecionado, self.no_menu = 'chat', '', None, False
            self.salvar()
            self.render()
        box.add_widget(button('Novo mandato aleatório', reiniciar, primary=True))
        box.add_widget(button('Manter minha partida', popup.dismiss))
        popup.open()

    def on_pause(self):
        self.salvar()
        return True

    def on_stop(self):
        if hasattr(self, 'game') and hasattr(self, 'save_path'):
            self.salvar()


if __name__ == '__main__':
    ZapCondominioApp().run()
