from typing import TYPE_CHECKING, TypeVar

import pygame.mouse
from pygame import Surface, Rect

from gui.Listener import Listener
from gui.widgets import Widget
from gui.Paintable import Paintable
from resouces import transform

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

    def render_game(self, surface: Surface, mousex: int, mousey: int, render_rect: Rect, focus: bool):
        """绘制游戏到屏幕上"""
        game_display_rect = self.get_game_display_rect(render_rect)
        # 鼠标
        if focus:
            if game_display_rect.collidepoint(mousex, mousey):
                # 鼠标也需要缩放
                mousex, mousey = self.get_game_display_rect_mouse_pos(game_display_rect, mousex, mousey)
            else:
                focus = False
        self.client.renderer.render(focus, mousex, mousey)
        game_screen = transform.scale(self.client.renderer.screen, w=game_display_rect.w, h=game_display_rect.h)
        surface.blit(game_screen, game_display_rect)

    def get_game_display_rect_mouse_pos(self, game_display_rect: Rect, mousex, mousey):
        mousex -= game_display_rect.x
        mousey -= game_display_rect.y
        game_screen_rect = self.client.renderer.screen.get_rect()
        mousex = game_screen_rect.w / game_display_rect.w * mousex
        mousey = game_screen_rect.h / game_display_rect.h * mousey
        return mousex, mousey

    def get_game_display_rect(self, render_rect: Rect) -> Rect:
        """已指定区域为范围获取绘制的区域"""
        game_screen_rect = self.client.renderer.screen.get_rect()
        # 缩放
        if render_rect.h >= render_rect.w:
            game_screen_rect.h = render_rect.w / game_screen_rect.w * game_screen_rect.h
            game_screen_rect.w = render_rect.w
        else:
            game_screen_rect.w = render_rect.h / game_screen_rect.h * game_screen_rect.w
            game_screen_rect.h = render_rect.h
        game_screen_rect.center = render_rect.center
        return game_screen_rect

    @property
    def resourcemanager(self):
        return self.client.resourcemanager

    @property
    def font(self):
        return self.resourcemanager.font

    @property
    def window(self):
        return self.client.window

    def initwidget(self, widget):
        widget.screen = self
        return widget

    def getmousepos(self):
        return self.window.getmousepos()

    def back(self):
        ...

    @Listener.event
    def close(self):
        pygame.key.stop_text_input()
