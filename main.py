import json
import os
import random
from kivy.config import Config

# Força o tamanho da janela do PC para o formato exato de tela de smartphone (360x640)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Define a cor de fundo da janela (Estilo escuro/WhatsApp)
Window.clearcolor = (0.1, 0.12, 0.15, 1)


class SindicoGame:
    def __init__(self):
        self.dia = 1
        self.caixa = 5000.00          # Saldo inicial em R$
        self.paciencia = 100          # Sanidade (0 a 100%)
        self.aprovacao = 50           # Popularidade (0 a 100%)
        self.tem_cameras = False      # Upgrade de segurança
        self.pendencias = []          # Chamados acumulados não resolvidos
        self.jogo_ativo = True
        self.todos_eventos = []
        self.carregar_eventos()

    def carregar_eventos(self):
        # Carrega o banco de dados do arquivo eventos.json se ele existir na pasta
        if os.path.exists("eventos.json"):
            try:
                with open("eventos.json", "r", encoding="utf-8") as f:
                    self.todos_eventos = json.load(f)
            except Exception:
                self.todos_eventos = []
        
        # Se o arquivo estiver vazio ou não existir, usa um evento de segurança padrão
        if not self.todos_eventos:
            self.todos_eventos = [{
                "dia": 1,
                "remetente": "Dona Cida (101)",
                "mensagem": "Síndico, o cachorro do 401 rasgou o lixo do corredor de novo!",
                "conselheiro_pitaco": "Seu Valdir (Conselho): 'Joga a sacola rasgada dentro da varanda dele!'",
                "recursos_necessarios": {"cameras": False},
                "opcoes": [
                    {"texto": "Notificar o dono educadamente.", "paciencia_sindico": -2, "caixa_condominio": 0, "aprovacao": 2, "resposta_morador": "Vou prender o cachorro!"},
                    {"texto": "Seguir o conselho do Seu Valdir.", "paciencia_sindico": 10, "caixa_condominio": -100, "aprovacao": -15, "resposta_morador": "O 401 chamou a polícia!"},
                    {"texto": "Aplicar multa de R$ 150.", "paciencia_sindico": 0, "caixa_condominio": 150, "aprovacao": -5, "resposta_morador": "Vou recorrer!"}
                ]
            }]

    def obter_evento_do_dia(self):
        # 1. Procura se há um evento específico cadastrado para este dia exato no JSON
        evento_fixo = next((ev for ev in self.todos_eventos if ev.get("dia") == self.dia), None)
        if evento_fixo:
            return evento_fixo
        
        # 2. Se não houver evento fixo para o dia, sorteia um aleatoriamente para o jogo nunca acabar
        if self.todos_eventos:
            evento_sorteado = random.choice(self.todos_eventos).copy()
            evento_sorteado["dia"] = self.dia
            evento_sorteado["mensagem"] = f"[TRETA REPETIDA] {evento_sorteado['mensagem']}"
            return evento_sorteado
        
        return None

    def avancar_dia(self):
        if not self.jogo_ativo:
            return

        # 1. Cobrança de taxa de condomínio no início de cada mês (a cada 30 dias)
        if self.dia > 1 and self.dia % 30 == 1:
            self.caixa += 12000.00

        # 2. Penalidade por acúmulo de pendências no Zap
        if len(self.pendencias) > 0:
            penalidade = len(self.pendencias) * 2
            self.paciencia -= penalidade
            self.aprovacao -= penalidade

        # Limites lógicos (0 a 100)
        self.paciencia = max(0, min(100, self.paciencia))
        self.aprovacao = max(0, min(100, self.aprovacao))

        # Adiciona o evento do dia atual às pendências
        evento_atual = self.obter_evento_do_dia()
        if evento_atual and evento_atual not in self.pendencias:
            self.pendencias.append(evento_atual)

        self.dia += 1
        self.verificar_status_jogo()

    def responder_evento(self, evento, indice_opcao):
        opcao = evento["opcoes"][indice_opcao]

        # Aplica impactos
        self.paciencia += opcao.get("paciencia_sindico", 0)
        self.caixa += opcao.get("caixa_condominio", 0)
        self.aprovacao += opcao.get("aprovacao", 0)

        # Limites
        self.paciencia = max(0, min(100, self.paciencia))
        self.aprovacao = max(0, min(100, self.aprovacao))

        # Remove das pendências
        if evento in self.pendencias:
            self.pendencias.remove(evento)

        self.verificar_status_jogo()
        return opcao.get("resposta_morador", "O morador leu a mensagem.")

    def comprar_cameras(self):
        custo = 1500.00
        if self.caixa >= custo and not self.tem_cameras:
            self.caixa -= custo
            self.tem_cameras = True
            self.aprovacao += 10
            return True
        return False

    def verificar_status_jogo(self):
        if self.paciencia <= 0 or self.caixa < 0:
            self.jogo_ativo = False


class ZapCondominioApp(App):
    def build(self):
        self.game = SindicoGame()
        self.title = "Zap do Condomínio"

        # Layout Principal Retrato
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=8)

        # 1. PAINEL DE STATUS (Topo)
        self.lbl_status = Label(
            text="",
            size_hint_y=None,
            height=65,
            color=(1, 1, 1, 1),
            font_size=12,
            bold=True
        )
        self.root.add_widget(self.lbl_status)

        # 2. TELA DE CHAT (Centro / Scroll)
        self.chat_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))

        self.scroll = ScrollView(size_hint_y=0.53)
        self.scroll.add_widget(self.chat_layout)
        self.root.add_widget(self.scroll)

        # 3. BOTÕES DE RESPOSTA E AÇÕES (Rodapé)
        self.botoes_layout = BoxLayout(orientation='vertical', spacing=4, size_hint_y=0.37)
        self.root.add_widget(self.botoes_layout)

        self.atualizar_interface()
        return self.root

    def atualizar_interface(self):
        cam_status = "📷 Câmeras: SIM" if self.game.tem_cameras else "📷 Câmeras: NÃO"
        self.lbl_status.text = (
            f"🗓️ Dia: {self.game.dia}/365  |  💰 Caixa: R$ {self.game.caixa:.2f}\n"
            f"🧠 Paciência: {self.game.paciencia}%  |  ⭐ Aprovação: {self.game.aprovacao}%\n"
            f"📋 Pendências: {len(self.game.pendencias)}  |  {cam_status}"
        )

        self.chat_layout.clear_widgets()
        self.botoes_layout.clear_widgets()

        # Condição de Fim de Jogo
        if not self.game.jogo_ativo:
            motivo = "Surto de estresse total!" if self.game.paciencia <= 0 else "Falência do condomínio!"
            lbl_end = Label(
                text=f"🚨 GAME OVER! 🚨\n\n{motivo}\nVocê não sobreviveu ao mandato.",
                size_hint_y=None, height=120, color=(1, 0.3, 0.3, 1), bold=True
            )
            self.chat_layout.add_widget(lbl_end)
            return

        if self.game.dia > 365:
            lbl_win = Label(
                text="🏆 VITÓRIA! 🏆\n\nVocê sobreviveu aos 365 dias do Zap do Condomínio!",
                size_hint_y=None, height=120, color=(0.3, 1, 0.3, 1), bold=True
            )
            self.chat_layout.add_widget(lbl_win)
            return

        evento_hoje = self.game.obter_evento_do_dia()

        # Exibe o problema no Chat
        if evento_hoje:
            msg = f"📱 [GRUPO DO ZAP]\nDe: {evento_hoje['remetente']}\n\n\"{evento_hoje['mensagem']}\""
            self.chat_layout.add_widget(Label(text=msg, size_hint_y=None, height=100, color=(0.9, 0.9, 0.9, 1), font_size=13))

            # Exibe o Pitaco do Conselheiro
            if "conselheiro_pitaco" in evento_hoje:
                pitaco = f"🤡 [PITACA DA CONSELHO]\n{evento_hoje['conselheiro_pitaco']}"
                self.chat_layout.add_widget(Label(text=pitaco, size_hint_y=None, height=75, color=(1, 0.8, 0.2, 1), font_size=12))

            # Gera os botões de resposta
            for idx, opcao in enumerate(evento_hoje["opcoes"]):
                btn = Button(
                    text=opcao["texto"],
                    size_hint_y=None,
                    height=42,
                    background_color=(0.2, 0.5, 0.8, 1),
                    font_size=12
                )
                btn.bind(on_press=lambda inst, i=idx: self.responder(evento_hoje, i))
                self.botoes_layout.add_widget(btn)

        # Botão de Comprar Câmeras se não tiver
        if not self.game.tem_cameras and self.game.caixa >= 1500:
            btn_cam = Button(
                text="🛒 Comprar Câmeras HD (R$ 1.500)",
                size_hint_y=None,
                height=38,
                background_color=(0.8, 0.5, 0.2, 1),
                font_size=12
            )
            btn_cam.bind(on_press=self.comprar_cameras_acao)
            self.botoes_layout.add_widget(btn_cam)

    def responder(self, evento, indice_opcao):
        self.game.responder_evento(evento, indice_opcao)
        self.game.avancar_dia()
        self.atualizar_interface()

    def comprar_cameras_acao(self, instance):
        if self.game.comprar_cameras():
            self.atualizar_interface()


if __name__ == '__main__':
    ZapCondominioApp().run()