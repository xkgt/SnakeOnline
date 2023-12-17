from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.screens import Screen

from gui.Paintable import Paintable
from pygame import Rect


class Widget(Paintable):
    rect: Rect
    screen: "Screen"

    def __init__(self, x=0, y=0, w=0, h=0):
        self.rect = Rect(x, y, w, h)

    def tick(self, frame):
        ...
    #
    # def __delattr__(self, item):
    #     object.__delattr__(self, item)
    #
    # def __setattr__(self, key, value):
    #     object.__setattr__(self, key, value)
