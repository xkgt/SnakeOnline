import pygame
from pygame.freetype import Font
from pygame import Surface

from gui import layouts
from .Widget import Widget


class Label(Widget):
    """文字"""
    def __init__(self, font: Font, text, *labels: "Label", fgcolor=(0, 0, 0), bgcolor=None, size=45, **kwargs):
        self.text = text  # 没用，只是用于区分

        self.surface, self.rect = font.render(text, fgcolor, bgcolor, size=size, **kwargs)  # 文字
        super().__init__(w=layouts.get_width(*(self, *labels)), h=layouts.get_height(*(self, *labels)))
        new_surface = Surface(self.rect.size, pygame.SRCALPHA)

        x = 0
        for label in (self, *labels):
            label.rect.x = x
            label.rect.centery = self.rect.centery
            label.render(new_surface, 0, 0)
            x = label.rect.right
        self.surface = new_surface

    def render(self, surface, mousex: int, mousey: int):
        surface.blit(self.surface, self.rect)
