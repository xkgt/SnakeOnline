import pygame.draw

from .Widget import Widget


class ProgressBar(Widget):
    def __init__(self, w, h, maxvalue, value=0):
        super().__init__(0, 0, w, h)
        self.maxvalue = maxvalue
        self.value = value

    def render(self, surface, mousex: int, mousey: int):
        rect = self.rect.copy()
        rect.w = self.rect.w * (self.value / self.maxvalue)
        # 绘制进度条
        pygame.draw.rect(surface, (0, 255, 0), rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 3)
