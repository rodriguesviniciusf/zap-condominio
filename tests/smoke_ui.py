"""Percorre a interface real em celular, com cenários controlados para cada mecânica."""
import copy
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['ZAP_SAVE_DIR'] = tempfile.mkdtemp(prefix='zap-ui-')
os.environ['ZAP_QA_SEED'] = '7'
os.environ['KIVY_NO_ARGS'] = '1'
from kivy.config import Config
Config.set('graphics', 'width', os.environ.get('ZAP_WIDTH', '390'))
Config.set('graphics', 'height', os.environ.get('ZAP_HEIGHT', '844'))
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from PIL import Image
from main import ZapCondominioApp

OUT = Path('screenshots')
OUT.mkdir(exist_ok=True)
width = os.environ.get('ZAP_WIDTH', '390')
app = ZapCondominioApp()


def check(name):
    assert app.shell.height >= Window.height-4
    assert app.shell.width >= Window.width-4
    for widget in app.root.walk():
        if isinstance(widget, Label) and widget.text:
            widget.texture_update()
            assert widget.height+4 >= widget.texture_size[1], (name, widget.text, widget.height, widget.texture_size)
        if isinstance(widget, BoxLayout) and widget.orientation == 'vertical':
            children = sorted(widget.children, key=lambda child: child.y)
            for child in children:
                assert child.height > 0, (name, 'altura vazia', type(child).__name__)
            for lower, upper in zip(children, children[1:]):
                assert lower.top <= upper.y+2, (name, 'sobreposição', type(lower).__name__, type(upper).__name__)
    path = OUT/f'{width}-{name}.png'
    app.root.export_to_png(str(path))
    img = Image.open(path).convert('RGB')
    assert len(img.getcolors(img.width*img.height)) > 100, name
    print('Tela:', name, 'janela:', Window.size, flush=True)


def later(fn):
    Clock.schedule_once(fn, .6)


def menu(_):
    check('inicio')
    app.iniciar()
    later(chat)


def chat(_):
    check('chat')
    app.scroll.scroll_y = 0
    later(choices)


def choices(_):
    check('escolhas')
    app.responder(app.game.evento_atual, 0)
    app.avancar()
    app.avancar()
    app.mudar_aba('pendencias')
    later(pending)


def pending(_):
    check('pautas')
    app.selecionar(app.game.pendencias[0]['ticket'])
    later(detail)


def detail(_):
    check('detalhe')
    app.responder(app.game.pendencias[0], 0)
    assert not app.game.pendencias
    app.mudar_aba('moradores')
    later(people)


def people(_):
    check('moradores')
    name = next(iter(app.game.moradores))
    app.acao(lambda: app.game.reconciliar(name))
    assert app.game.social_dia
    app.mudar_aba('gestao')
    later(management)


def management(_):
    check('predio')
    app.acao(app.game.descansar)
    app.acao(app.game.delegar)
    assert app.game.descanso_dia and app.game.delegacao_dia
    app.comprar('cameras')
    assert app.game.tem_cameras
    app.game.caixa = 5000  # Estado de QA para testar a votação sem depender da economia.
    for state in app.game.moradores.values():
        state.update(confianca=80, irritacao=0)
    app.game.aprovacao = 70
    app.game.assembleia = dict(tipo='ordinaria', dia=app.game.dia, titulo='Assembleia do mês')
    app.mudar_aba('pendencias')
    later(assembly)


def assembly(_):
    check('assembleia')
    app.acao(lambda: app.game.votar(0))
    assert app.game.ultima_votacao['aprovada']
    app.game.encerrado = False
    app.game.evento_atual = copy.deepcopy(next(e for e in app.game.todos_eventos if e['categoria'] == 'seguranca'))
    app.game.evento_atual.update(ticket='fixture-seguranca', abertura=app.game.dia, tipo_evento='normal')
    app.mudar_aba('chat')
    app.scroll.scroll_y = 0
    later(unlocked)


def unlocked(_):
    check('solucao-extra')
    assert len(app.game.opcoes_evento(app.game.evento_atual)) == 5
    app.responder(app.game.evento_atual, 3)
    for _ in range(3):
        app.avancar()
        if app.game.dia < 6:
            app.responder(app.game.evento_atual, 0)
    assert app.game.evento_foco.get('tipo_evento') == 'crise'
    later(crisis)


def crisis(_):
    check('crise')
    app.responder(app.game.evento_foco, 2)
    for _ in range(2):
        app.responder(app.game.evento_atual, 0)
        app.avancar()
    assert app.game.evento_foco['etapa'] == 2
    later(crisis_two)


def crisis_two(_):
    check('crise-2')
    app.game.caixa = 5000
    app.responder(app.game.evento_foco, 0)
    app.game.aprovacao = 5
    app.game.assembleia = dict(tipo='crise', dia=app.game.dia, titulo='Assembleia de destituição')
    for state in app.game.moradores.values():
        state.update(confianca=0, irritacao=90)
    app.mudar_aba('pendencias')
    later(emergency)


def emergency(_):
    check('destituicao')
    app.acao(lambda: app.game.votar(2))
    assert app.game.fim_motivo == 'destituicao'
    later(result)


def result(_):
    check('resultado')
    app.confirmar_reinicio()
    later(popup)


def popup(_):
    Window.screenshot(name=str(OUT/f'{width}-reinicio.png'))
    old = app.game.vistos[0]
    modal = next(w for w in Window.children if isinstance(w, Popup))
    label = next(w for w in modal.walk() if isinstance(w, Label) and w.text == 'Novo mandato aleatório')
    label.parent.dispatch('on_release')
    assert app.game.evento_atual['id'] != old
    assert app.game.jogo_ativo
    later(finish)


def finish(_):
    check('novo-mandato')
    app.stop()


Clock.schedule_once(menu, 3)
app.run()
print('UI e novas mecânicas verificadas:', width)
