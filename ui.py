"""Componentes vetoriais do jogo, sem dependências de tema externas."""
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line, Ellipse
from kivy.metrics import dp, sp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

BG = (0.035, 0.063, 0.106, 1)
PANEL = (0.072, 0.115, 0.173, 1)
PANEL2 = (0.095, 0.148, 0.210, 1)
EDGE = (0.16, 0.22, 0.29, 1)
INK = (0.95, 0.95, 0.91, 1)
MUTED = (0.57, 0.65, 0.73, 1)
MINT = (0.46, 0.89, 0.71, 1)
AMBER = (0.97, 0.73, 0.40, 1)
CORAL = (1.0, 0.51, 0.46, 1)


class Text(Label):
    def __init__(self, text='', size=14, color=INK, bold=False, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        super().__init__(text=text, font_size=sp(size), color=color, bold=bold, halign='left', valign='middle', **kwargs)
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
    label = Label(text=title, color=BG if primary else INK, bold=True, font_size=sp(font))
    label.bind(size=lambda w, s: setattr(w, 'text_size', (s[0], s[1])))
    card.add_widget(label)
    return card
