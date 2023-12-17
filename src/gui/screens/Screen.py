from typing import TYPE_CHECKING, TypeVar

import pygame.mouse
from pygame import Surface

from gui.Listener import Listener
from gui.widgets import Widget
from gui.Paintable import Paintable
if TYPE_CHECKING:
    from Client import Client
_T = TypeVar("_T", bound=Widget)


class Screen(Paintable, Listener):
    """负责绘制，gui"""
    width: int
    height: int
    client: "Client"

    def __init__(self):
        super().__init__()
        self.widgets: list[Widget] = []

    def init(self, width, height):
        """用于初始化组件"""

    def tick(self, frame):
        """一帧只有一个tick，但是render可能多次绘制"""
        for widget in self.widgets:
            widget.tick(frame)

    def addwidget(self, widget: _T) -> _T:
        """添加自动绘画组件"""
        self.widgets.append(widget)
        self.initwidget(widget)
        if isinstance(widget, Listener):
            self.sub_listeners.add(widget)
        return widget

    def render(self, surface: Surface, mousex: int, mousey: int):
        for widget in self.widgets:
            widget.render(surface, mousex, mousey)

    @property
    def resourcemanager(self):
        return self.client.resourcemanager

    @property
    def font(self):
        return self.resourcemanager.font

    @property
    def window(self):
        return self.client.window

    def __setattr__(self, key, value):
        if isinstance(value, Widget):
            self.initwidget(value)
        super().__setattr__(key, value)

    def initwidget(self, widget):
        widget.screen = self
        return widget

    def getmousepos(self):
        return pygame.mouse.get_pos()

    def back(self):
        ...

    @Listener.event
    def close(self):
        ...
