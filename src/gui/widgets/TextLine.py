import pygame.draw
from pygame.freetype import Font

from .Widget import Widget
from gui.Listener import Listener


class TextLine(Widget, Listener):
    """输入框"""
    def __init__(self, w, h, font: Font, text="", placeholder_text=""):
        Listener.__init__(self)
        super().__init__(w=w, h=h)
        self.text = text
        self.placeholder_text = placeholder_text
        self.focus = False
        self.font = font
        self.cursor = False
        self.input_text = ""
        self.cursor_time = 0

    def tick(self, frame):
        if self.focus:
            self.cursor_time += 1
            if self.cursor_time % (self.screen.client.framerate // 2) == 0:
                self.setcursor(not self.cursor)

    def textinput(self, text, **kwargs):
        if self.focus:
            self.text += text
            raise StopIteration

    def keydown(self, unicode, key, mod, **kwargs):
        if self.focus:
            if key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            self.setcursor(True)
            raise StopIteration

    def mousebuttondown(self, pos, button, **kwargs):
        if button == 1:
            if self.rect.collidepoint(*pos):
                self.setfocus(True)
                raise StopIteration
            else:
                self.setfocus(False)

    def render(self, surface, mousex: int, mousey: int):
        # 边框
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        pygame.draw.rect(surface, (0, 0, 0) if self.focus else (0, 120, 215), self.rect, width=3)
        # 文字
        color = (0, 0, 0) if self.text else (127, 127, 127)
        text = self.text or self.placeholder_text
        text_surface, text_rect = self.font.render(text, size=self.rect.h - 12, fgcolor=color)
        text_rect.x = self.rect.x + 3
        text_rect.centery = self.rect.centery
        surface.blit(text_surface, text_rect)
        # 光标
        if self.cursor:
            cursor_x = text_rect.right + 2 if self.text else 5
            pygame.draw.line(surface, (0, 0, 0),
                             (cursor_x, self.rect.top+6),
                             (cursor_x, self.rect.bottom-6), width=2)

    def setcursor(self, v):
        self.cursor = v
        self.cursor_time = 0

    def setfocus(self, v):
        self.focus = v
        self.setcursor(v)
        if v:
            pygame.key.start_text_input()
            pygame.key.set_repeat(500, 50)
            # pygame.key.set_text_input_rect(self.rect)
        else:
            pygame.key.stop_text_input()
