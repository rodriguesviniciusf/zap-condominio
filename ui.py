"""Componentes vetoriais do jogo, sem dependências de tema externas."""
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line, Ellipse, StencilPush, StencilUse, StencilUnUse, StencilPop
from kivy.core.image import Image as CoreImage
from pathlib import Path
from lore import PERFIS, CONSELHEIROS
from kivy.metrics import dp, sp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

BG = (.955, .946, .908, 1)
PANEL = (.998, .993, .972, 1)
PANEL2 = (.89, .95, .90, 1)
EDGE = (.77, .83, .78, 1)
INK = (.09, .19, .19, 1)
MUTED = (.36, .46, .43, 1)
MINT = (.08, .48, .35, 1)
AMBER = (.76, .40, .09, 1)
CORAL = (.80, .24, .20, 1)


TEXT_SCALE = 1.0

def set_text_scale(value):
    global TEXT_SCALE
    TEXT_SCALE = value


class Text(Label):
    def __init__(self, text='', size=14, color=INK, bold=False, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        super().__init__(text=text, font_size=sp(size * TEXT_SCALE if size >= 12 else size), color=color, bold=bold, halign='left', valign='middle', **kwargs)
        self.bind(width=self._wrap, texture_size=self._fit)
        self._wrap()

    def _wrap(self, *_):
        self.text_size = (max(1, self.width), None)

    def _fit(self, *_):
        self.height = self.texture_size[1] + dp(3)


class Card(BoxLayout):
    bg = ListProperty(PANEL)
    stroke = ListProperty(EDGE)

    def __init__(self, radius=18, adaptive=True, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('padding', dp(14))
        kwargs.setdefault('spacing', dp(8))
        if adaptive:
            kwargs.setdefault('size_hint_y', None)
        elif 'height' in kwargs:
            kwargs.setdefault('size_hint_y', None)
        super().__init__(**kwargs)
        self.radius = dp(radius)
        with self.canvas.before:
            self._border_color = Color(*self.stroke)
            self._border = RoundedRectangle(radius=[self.radius])
            self._fill_color = Color(*self.bg)
            self._fill = RoundedRectangle(radius=[max(0, self.radius-dp(1))])
        self.bind(pos=self._paint, size=self._paint, bg=self._paint, stroke=self._paint)
        if adaptive:
            self.bind(minimum_height=self.setter('height'))
        self._paint()

    def _paint(self, *_):
        self._border_color.rgba = self.stroke
        self._border.pos, self._border.size = self.pos, self.size
        self._fill_color.rgba = self.bg
        self._fill.pos = (self.x+dp(1), self.y+dp(1))
        self._fill.size = (max(0, self.width-dp(2)), max(0, self.height-dp(2)))


class TapCard(ButtonBehavior, Card):
    def __init__(self, action=None, **kwargs):
        super().__init__(**kwargs)
        self.action = action
        self.rest = list(self.bg)
        self.bind(on_press=self._press, on_release=self._release)

    def _press(self, *_):
        Animation.cancel_all(self, 'bg')
        self.bg = [min(1, v+0.045) for v in self.rest[:3]]+[1]

    def _release(self, *_):
        Animation(bg=self.rest, duration=.12).start(self)
        if self.action:
            self.action()


class Avatar(Label):
    def __init__(self, initials, accent=MINT, diameter=38, **kwargs):
        super().__init__(text=initials, color=BG, bold=True, font_size=sp(13), size_hint=(None, None), size=(dp(diameter), dp(diameter)), **kwargs)
        with self.canvas.before:
            Color(*accent)
            self._circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._paint, size=self._paint)

    def _paint(self, *_):
        self._circle.pos, self._circle.size = self.pos, self.size


class Meter(Widget):
    value = NumericProperty(0)

    def __init__(self, value=0, accent=MINT, **kwargs):
        super().__init__(size_hint_y=None, height=dp(4), **kwargs)
        self.accent = accent
        self.value = value
        self.bind(pos=self._paint, size=self._paint, value=self._paint)

    def _paint(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*EDGE)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(2)])
            Color(*self.accent)
            RoundedRectangle(pos=self.pos, size=(self.width*max(0, min(100, self.value))/100, self.height), radius=[dp(2)])


class CondoArt(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._paint, size=self._paint)

    def _paint(self, *_):
        self.canvas.clear()
        x, y, w, h = self.x, self.y, self.width, self.height
        with self.canvas:
            Color(.08, .17, .20, 1)
            Ellipse(pos=(x+w*.16, y+h*.04), size=(w*.7, h*.94))
            Color(*AMBER)
            Ellipse(pos=(x+w*.78, y+h*.69), size=(h*.17, h*.17))
            Color(*EDGE)
            Line(points=[x+w*.04, y+h*.12, x+w*.96, y+h*.12], width=dp(1))
            buildings = [(.15, .15, .23, .55, PANEL2), (.40, .15, .26, .78, (.15, .27, .31, 1)), (.68, .15, .18, .43, PANEL2)]
            for b, (bx, by, bw, bh, color) in enumerate(buildings):
                Color(*color)
                RoundedRectangle(pos=(x+w*bx, y+h*by), size=(w*bw, h*bh), radius=[dp(7)])
                for r in range(5 if b == 1 else 3):
                    for c in range(3 if b != 2 else 2):
                        Color(*(AMBER if (r+c+b) % 3 != 1 else (.07, .13, .18, 1)))
                        Rectangle(pos=(x+w*(bx+.025+c*.065), y+h*(by+.09+r*.115)), size=(w*.034, h*.055))
            Color(*MINT)
            RoundedRectangle(pos=(x+w*.48, y+h*.15), size=(w*.07, h*.085), radius=[dp(3)])
            Line(circle=(x+w*.13, y+h*.72, dp(4)), width=dp(1.2))
            Line(points=[x+w*.89, y+h*.45, x+w*.93, y+h*.45], width=dp(1))
            Line(points=[x+w*.91, y+h*.42, x+w*.91, y+h*.48], width=dp(1))


def stack(spacing=10, padding=0):
    box = BoxLayout(orientation='vertical', spacing=dp(spacing), padding=padding, size_hint_y=None)
    box.bind(minimum_height=box.setter('height'))
    return box


def row(height=38, spacing=8):
    return BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(height), spacing=dp(spacing))


def button(title, action, primary=False, accent=MINT, font=14):
    card = TapCard(action=action, adaptive=False, size_hint_y=None, height=dp(50), bg=accent if primary else PANEL,
                   stroke=accent if primary else EDGE, padding=(dp(15), dp(10)), radius=14)
    if font >= 12:
        label = Text(title, size=font, color=(1, 1, .96, 1) if primary else INK, bold=True)
        label.halign = 'center'
        label.bind(height=lambda w, h: setattr(card, 'height', max(dp(50), h+dp(20))))
    else:
        label = Label(text=title, color=(1, 1, .96, 1) if primary else INK, bold=True, font_size=sp(font))
        label.bind(size=lambda w, s: setattr(w, 'text_size', (s[0], s[1])))
    card.add_widget(label)
    return card

_TEXTURES = {}


def texture(name):
    if name not in _TEXTURES:
        _TEXTURES[name] = CoreImage(str(Path(__file__).parent/'assets'/name)).texture
    return _TEXTURES[name]


class Portrait(Widget):
    def __init__(self, name='', diameter=48, index=None, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(diameter), dp(diameter)), **kwargs)
        info = PERFIS.get(name, CONSELHEIROS.get(name, dict(retrato=11)))
        tile = info['retrato'] if index is None else index
        source = texture('elenco.jpg')
        w, h = source.width//3, source.height//4
        side = min(w, h)
        self.face = source.get_region((tile % 3)*w+(w-side)//2, (3-tile//3)*h, side, side)
        self.bind(pos=self._draw, size=self._draw)
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(.1, .2, .15, .12)
            Ellipse(pos=(self.x, self.y-dp(2)), size=self.size)
            StencilPush()
            Ellipse(pos=self.pos, size=self.size)
            StencilUse()
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size, texture=self.face)
            StencilUnUse()
            Ellipse(pos=self.pos, size=self.size)
            StencilPop()
            Color(*EDGE)
            Line(circle=(self.center_x, self.center_y, self.width/2), width=dp(1))


class Cover(Widget):
    def __init__(self, radius=20, **kwargs):
        super().__init__(**kwargs)
        self.radius = dp(radius)
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        if self.width < 1 or self.height < 1:
            return
        source = texture('capa.jpg')
        target = self.width/self.height
        if source.width/source.height > target:
            crop_h, crop_w = source.height, int(source.height*target)
        else:
            crop_w, crop_h = source.width, int(source.width/target)
        crop_w, crop_h = max(1, crop_w), max(1, crop_h)
        region = source.get_region((source.width-crop_w)//2, (source.height-crop_h)//2, crop_w, crop_h)
        self.canvas.clear()
        with self.canvas:
            StencilPush()
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            StencilUse()
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size, texture=region)
            StencilUnUse()
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            StencilPop()


class Icon(Widget):
    def __init__(self, kind='chat', accent=MINT, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(22), dp(22)), **kwargs)
        self.kind, self.accent = kind, accent
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        x, y, s = self.x, self.y, self.width
        self.canvas.clear()
        with self.canvas:
            Color(*self.accent)
            if self.kind == 'building':
                Line(rectangle=(x+s*.16, y+s*.1, s*.68, s*.8), width=dp(1.3))
                for a in (.32, .6):
                    for b in (.32, .57, .77):
                        Rectangle(pos=(x+s*a, y+s*b), size=(s*.09, s*.07))
            elif self.kind == 'people':
                for a in (.28, .72):
                    Line(circle=(x+s*a, y+s*.7, s*.12), width=dp(1.2))
                    Line(points=[x+s*(a-.19), y+s*.18, x+s*(a-.14), y+s*.4,
                                 x+s*(a+.14), y+s*.4, x+s*(a+.19), y+s*.18], width=dp(1.2))
            elif self.kind == 'board':
                Line(rounded_rectangle=(x+s*.2, y+s*.08, s*.6, s*.78, dp(2)), width=dp(1.2))
                for a in (.3, .5, .7):
                    Line(points=[x+s*.34, y+s*a, x+s*.66, y+s*a], width=dp(1.2))
            else:
                Line(rounded_rectangle=(x+s*.1, y+s*.28, s*.8, s*.61, dp(4)), width=dp(1.3))
                Line(points=[x+s*.2, y+s*.28, x+s*.2, y+s*.08, x+s*.43, y+s*.28], width=dp(1.3))

