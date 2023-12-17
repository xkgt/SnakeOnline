from functools import lru_cache
from .Widget import Widget
from .Label import Label
from gui.Listener import Listener
import pygame


class Button(Widget, Listener):
    def __init__(self, w, h, label: Label, bgcolor, callback):
        super().__init__(w=w, h=h)
        Listener.__init__(self)
        self.bgcolor = bgcolor
        self.label = label
        self.callback = callback
        self.clicked = False

    def mousebuttondown(self, pos, button, **kwargs):
        if self.rect.collidepoint(pos):
            self.clicked = True

    def mousemotion(self, pos, rel, buttons, **kwargs):
        if self.clicked and not self.rect.collidepoint(pos):
            self.clicked = False

    def mousebuttonup(self, pos, button, **kwargs):
        if self.rect.collidepoint(pos):
            self.clicked = False
            self.callback()
            raise StopIteration

    def render(self, surface, mousex: int, mousey: int):
        # 按钮
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        a = self.rect.inflate(-6, -6)
        pygame.draw.rect(surface, self.bgcolor, a)
        # 鼠标对着按钮
        if self.rect.collidepoint(mousex, mousey):
            surface.blit(get_alpha_surface(a.size), a)
            # 按着
            if self.clicked:
                surface.blit(get_alpha_surface(a.size), a)
        # 反复修改坐标，防止按钮位置改版
        self.label.rect.center = self.rect.center
        self.label.render(surface, mousex, mousey)

    @classmethod
    def build(cls, w, h, text, font, callback, fgcolor=(0, 0, 255), bgcolor=(186, 229, 249), size=30):
        return cls(w, h, Label(font, text, fgcolor=fgcolor, size=size), bgcolor, callback)


@lru_cache(10)
def get_alpha_surface(size):
    alpha_surface = pygame.Surface(size, pygame.SRCALPHA)
    alpha_surface.fill((255, 255, 255, 127))
    return alpha_surface
