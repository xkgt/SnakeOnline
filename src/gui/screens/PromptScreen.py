from typing import Union

from gui import layouts
from .Screen import Screen
from gui.widgets import Label, Button, Widget


class PromptScreen(Screen):
    def __init__(self, lastscreen: Screen, label_or_text: Union[Label, str], back_callback=None, has_back_button=True):
        super().__init__()
        self.lastscreen = lastscreen
        self.label_or_text = label_or_text
        self.back_func = back_callback
        self.has_back_button = has_back_button

    def init(self, width, height):
        if isinstance(self.label_or_text, str):
            label = Label(self.font, self.label_or_text, fgcolor=(255, 0, 0), size=40)
        else:
            label = self.label_or_text
        a = self.addwidget(Button.build(350, 80, "返回", self.font, self.back, size=40)
                           if self.has_back_button else Widget(w=350, h=80))
        layouts.vertical_layout(
            self.addwidget(label),
            a,
            centerx=width//2, top=(height-label.rect.h)//2-60, interval=140
        )

    def back(self):
        if self.back_func:
            self.back_func()
        if self.has_back_button:
            self.window.setscreen(self.lastscreen)
