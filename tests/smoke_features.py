"""Testa os novos fluxos, inclusive texto ampliado e popups."""
import copy
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['ZAP_SAVE_DIR'] = tempfile.mkdtemp(prefix='zap-features-')
os.environ['ZAP_QA_SEED'] = '19'
os.environ['KIVY_NO_ARGS'] = '1'
from kivy.config import Config
Config.set('graphics', 'width', os.environ.get('ZAP_WIDTH', '390'))
Config.set('graphics', 'height', os.environ.get('ZAP_HEIGHT', '844'))
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.opengl import glPixelStorei, GL_PACK_ALIGNMENT
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from main import ZapCondominioApp
from community import CASOS
from ui import set_text_scale

app = ZapCondominioApp()
Path('screenshots').mkdir(exist_ok=True)
width = os.environ.get('ZAP_WIDTH', '390')


def dismiss():
    for child in list(Window.children):
        if isinstance(child, Popup):
            child.dismiss(animation=False)


def check(nome):
    for top in Window.children:
        for widget in top.walk():
            if isinstance(widget, Label) and widget.text:
                widget.texture_update()
                assert widget.height+4 >= widget.texture_size[1], (nome, widget.text, widget.height, widget.texture_size)
    glPixelStorei(GL_PACK_ALIGNMENT, 1)  # RGB: 390*3 não é múltiplo de quatro.
    Window.screenshot(name=str(Path('screenshots')/f'{width}-novo-{nome}.png'))
    print('Nova tela:', nome, flush=True)


def caso():
    dismiss()
    app.no_menu = False
    app.game.assembleia = None
    app.game.encerrado = False
    e = app.game.evento_atual
    e['investigacao'] = copy.deepcopy(CASOS[0])
    e['investigacao']['consultadas'] = []
    e['mensagem'] = CASOS[0]['mensagem']
    e['titulo'] = CASOS[0]['titulo']
    app.mudar_aba('chat')
    app.scroll.scroll_y = .48


def pistas():
    e = app.game.evento_atual
    app.acao(lambda: app.game.investigar(e, 0))
    app.acao(lambda: app.game.investigar(e, 1))
    app.scroll.scroll_y = .4


def texto_grande():
    dismiss()
    set_text_scale(1.3)
    app.preferencias.valores['texto'] = 1.3
    app.mudar_aba('chat')
    app.scroll.scroll_y = .4


def resolver():
    dismiss()
    app.acao(lambda: app.game.concluir_caso(app.game.evento_atual, 0))
    assert app.game.casos_resolvidos == 1
    app.mudar_aba('moradores')


def transicao():
    dismiss()
    del os.environ['ZAP_QA_SEED']
    app.avancar()
    assert app.transitando


steps = [
 ('tutorial-1', lambda: app.tutorial(0)),
 ('tutorial-2', lambda: (dismiss(), app.tutorial(1))),
 ('tutorial-3', lambda: (dismiss(), app.tutorial(2))),
 ('tutorial-4', lambda: (dismiss(), app.tutorial(3))),
 ('investigacao', caso),
 ('pistas', pistas),
 ('confirmacao', lambda: app.confirmar_acusacao(app.game.evento_atual, 0)),
 ('texto-grande', texto_grande),
 ('panelinhas', resolver),
 ('preferencias', app.ajustes),
 ('transicao', transicao),
]


def run(index=0):
    if index == len(steps):
        assert app.game.dia == 2
        Clock.schedule_once(lambda _: app.stop(), 1)
        return
    nome, acao = steps[index]
    acao()
    def capture(_):
        check(nome)
        Clock.schedule_once(lambda _: run(index+1), .15)
    Clock.schedule_once(capture, .45)


app.bind(on_start=lambda *_: Clock.schedule_once(lambda _: run(), .7))
app.run()
