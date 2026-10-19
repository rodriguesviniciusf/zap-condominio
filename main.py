"""Zap do Condomínio: interface mobile e persistência do mandato."""
from pathlib import Path
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from game import SindicoGame

Window.clearcolor = (0.055, 0.09, 0.10, 1)


class ZapCondominioApp(App):
    def build(self):
        self.title = 'Zap do Condomínio'
        self.game = SindicoGame()
        self.save_path = Path(self.user_data_dir) / 'mandato.json'
        self.aviso = 'Bem-vindo ao Zap da Gestão. O mandato dura 365 dias.'
        if self.save_path.exists():
            try:
                self.game.carregar(self.save_path)
                self.aviso = 'Mandato retomado.'
            except (OSError, ValueError, TypeError, KeyError):
                self.aviso = 'Não foi possível ler o save. Novo mandato iniciado.'
        self.aba = 'chat'
        self.root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))
        self.status = Label(size_hint_y=None, height=dp(92), font_size='14sp')
        self.root.add_widget(self.status)
        barra = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        for titulo, aba in [('Chat', 'chat'), ('Chamados', 'pendencias'), ('Gestão', 'gestao')]:
            botao = Button(text=titulo)
            botao.bind(on_release=lambda _, a=aba: self.mudar_aba(a))
            barra.add_widget(botao)
        self.root.add_widget(barra)
        self.scroll = ScrollView()
        self.conteudo = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        self.conteudo.bind(minimum_height=self.conteudo.setter('height'))
        self.scroll.add_widget(self.conteudo)
        self.root.add_widget(self.scroll)
        self.atualizar_interface()
        return self.root

    def texto(self, mensagem, cor=(0.9, 0.95, 0.94, 1)):
        rotulo = Label(text=mensagem, color=cor, size_hint_y=None, font_size='15sp', halign='left', valign='top')
        rotulo.bind(width=lambda w, v: setattr(w, 'text_size', (max(1, v-dp(8)), None)))
        rotulo.bind(texture_size=lambda w, v: setattr(w, 'height', v[1]+dp(18)))
        self.conteudo.add_widget(rotulo)

    def botao(self, titulo, acao):
        btn = Button(text=titulo, size_hint_y=None, height=dp(64), font_size='14sp', background_normal='', background_color=(0.08, 0.38, 0.31, 1))
        btn.bind(size=lambda w, v: setattr(w, 'text_size', (v[0]-dp(20), v[1]-dp(8))))
        btn.bind(on_release=lambda _: acao())
        self.conteudo.add_widget(btn)

    def mudar_aba(self, aba):
        self.aba = aba
        self.atualizar_interface()

    def atualizar_interface(self):
        g = self.game
        self.status.text = f'ZAP DA GESTÃO | Dia {g.dia}/365\nCaixa: R$ {g.caixa:,.0f}\nPaciência: {g.paciencia}% | Aprovação: {g.aprovacao}%\nChamados: {len(g.pendencias)} | Crises futuras: {len(g.consequencias)}'
        self.conteudo.clear_widgets()
        self.texto(self.aviso, (0.55, 0.9, 0.75, 1))
        if not g.jogo_ativo:
            self.texto('VITÓRIA! Você sobreviveu ao mandato.' if g.vitoria else 'FIM DO MANDATO: ' + ('paciência esgotada.' if g.paciencia <= 0 else 'o caixa ficou negativo.'))
            self.botao('Começar outro mandato', self.reiniciar)
        elif self.aba == 'chat':
            if g.encerrado:
                self.texto('Chamado de hoje encerrado. Você ainda pode resolver chamados antigos ou investir.')
            else:
                self.exibir_evento(g.evento_atual)
            self.botao('Encerrar o dia' if g.encerrado else 'Adiar chamado e encerrar o dia', self.avancar)
        elif self.aba == 'pendencias':
            self.texto('Cada chamado aberto reduz paciência e aprovação ao encerrar o dia (máximo de 12 pontos).')
            if not g.pendencias:
                self.texto('Tudo em dia. Desconfie desse silêncio.')
            for evento in g.pendencias:
                self.texto(f"Chamado aberto no dia {evento['abertura']}")
                self.exibir_evento(evento)
        else:
            self.texto('A cada 30 dias: R$ 12.000 em taxas, menos inadimplência conforme a aprovação, e R$ 9.000 em despesas. Câmeras reduzem pela metade o custo das decisões em segurança.')
            if not g.tem_cameras:
                self.botao('Instalar câmeras — R$ 1.500', self.comprar)
            else:
                self.texto('Câmeras instaladas.')
            self.texto('Últimas mensagens da gestão:')
            for item in g.historico[-8:]:
                self.texto(f"Dia {item['dia']}: {item['texto']}")
        self.scroll.scroll_y = 1
        g.salvar(self.save_path)

    def exibir_evento(self, evento):
        self.texto(f"{evento['remetente']}\n{evento['mensagem']}")
        self.texto(evento['conselheiro_pitaco'], (1, 0.78, 0.35, 1))
        for indice, opcao in enumerate(evento['opcoes']):
            self.botao(opcao['texto'], lambda e=evento, i=indice: self.responder(e, i))

    def responder(self, evento, indice):
        self.aviso = self.game.responder_evento(evento, indice)
        self.atualizar_interface()

    def avancar(self):
        self.game.avancar_dia()
        self.aviso = 'Novo dia, novas notificações. Veja o histórico na Gestão.'
        self.atualizar_interface()

    def comprar(self):
        self.aviso = 'Câmeras instaladas!' if self.game.comprar_cameras() else 'Saldo insuficiente.'
        self.atualizar_interface()

    def reiniciar(self):
        self.game = SindicoGame()
        self.aviso = 'Novo mandato. Boa sorte com o grupo.'
        self.aba = 'chat'
        self.atualizar_interface()

    def on_pause(self):
        self.game.salvar(self.save_path)
        return True

    def on_stop(self):
        if hasattr(self, 'game') and hasattr(self, 'save_path'):
            self.game.salvar(self.save_path)


if __name__ == '__main__':
    ZapCondominioApp().run()
