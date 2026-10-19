"""Executa as telas reais em Xvfb e verifica layout e ações essenciais."""
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['ZAP_SAVE_DIR'] = tempfile.mkdtemp(prefix='zap-ui-')
os.environ['KIVY_NO_ARGS'] = '1'
from kivy.config import Config
Config.set('graphics', 'width', os.environ.get('ZAP_WIDTH', '390'))
Config.set('graphics', 'height', os.environ.get('ZAP_HEIGHT', '844'))
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from PIL import Image
from main import ZapCondominioApp

OUT = Path('screenshots')
OUT.mkdir(exist_ok=True)
app = ZapCondominioApp()
errors = []
width = os.environ.get('ZAP_WIDTH', '390')


def check(name):
    assert app.shell.height >= Window.height-4, (name, app.shell.size, Window.size)
    assert app.shell.width >= Window.width-4, (name, app.shell.size, Window.size)
    for widget in app.root.walk():
        if isinstance(widget, Label) and widget.text:
            widget.texture_update()
            assert widget.height+4 >= widget.texture_size[1], (name, widget.text, widget.height, widget.texture_size)
    path = OUT/f'{width}-{name}.png'
    app.root.export_to_png(str(path))
    image = Image.open(path).convert('RGB')
    # Uma captura só com fundo ou com a primeira composição incompleta não passa.
    assert len(image.getcolors(image.width*image.height)) > 100, name
    print('Tela:', name, 'janela:', Window.size, 'layout:', app.shell.size, flush=True)


def menu(_):
    check('inicio')
    app.iniciar()
    Clock.schedule_once(chat, .6)


def chat(_):
    check('chat')
    app.scroll.scroll_y = 0
    Clock.schedule_once(choices, .4)


def choices(_):
    check('escolhas')
    app.responder(app.game.evento_atual, 0)
    assert app.game.encerrado
    app.avancar()
    app.avancar()
    app.mudar_aba('pendencias')
    Clock.schedule_once(pending, .5)


def pending(_):
    check('chamados')
    app.selecionar(app.game.pendencias[0]['ticket'])
    Clock.schedule_once(detail, .5)


def detail(_):
    check('detalhe')
    app.responder(app.game.pendencias[0], 0)
    assert not app.game.pendencias
    app.mudar_aba('gestao')
    Clock.schedule_once(management, .5)


def management(_):
    check('gestao')
    app.comprar()
    assert app.game.tem_cameras
    app.game.dia = 365
    app.game.evento_atual = app.game._sortear_evento()
    app.game.encerrado = True
    app.game.avancar_dia()
    app.mudar_aba('chat')
    Clock.schedule_once(result, .5)


def result(_):
    check('resultado')
    app.confirmar_reinicio()
    Clock.schedule_once(finish, .5)


def finish(_):
    Window.screenshot(name=str(OUT/f'{width}-reinicio.png'))
    app.stop()


Clock.schedule_once(menu, 3)
app.run()
print('UI verificada:', width)
