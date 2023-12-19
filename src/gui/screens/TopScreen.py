from typing import Union, Optional

import pygame
from .Screen import Screen
from .TitleScreen import TitleScreen
from ..widgets import Label


class TopScreen(Screen):
    """置顶屏幕，负责输入事件监听和简单绘制"""
    def __init__(self):
        super().__init__()
        # 提示
        self.prompt_label: Optional[Label] = None
        self.prompt_time = 0

    def render(self, surface, mousex: int, mousey: int):
        super().render(surface, mousex, mousey)
        if self.prompt_time:
            self.prompt_label.render(surface, mousex, mousey)

    def tick(self, frame):
        if self.prompt_time:
            self.prompt_time -= 1

    def prompt(self, label_or_text: Union[Label, str], time=1):
        """弹出提示"""
        if isinstance(label_or_text, str):
            label_or_text = Label(self.font, label_or_text, fgcolor=(255, 100, 0), size=40)
        self.prompt_label = label_or_text
        self.prompt_label.rect.center = self.window.rect.center
        self.prompt_time = int(time * self.client.framerate)

    def keydown(self, unicode, key, mod, **kwargs):
        if key == pygame.K_e:
            self.resourcemanager.config.playsound = not self.resourcemanager.config.playsound
            if not self.client.config.playsound:  # 如果禁止播放声音
                self.resourcemanager.stop_music()
            elif self.client.game and len(self.client.game.playerlist) > 1:  # 如果在联机
                self.resourcemanager.play_online_music()
            else:  # 否则就是单人游戏
                self.resourcemanager.play_single_music()
            raise StopIteration
        elif key == pygame.K_ESCAPE:
            if self.window.screen:
                self.window.screen.back()
            else:
                self.back()
            raise StopIteration

    def back(self):
        self.window.setscreen(TitleScreen())

    def __gt__(self, other):
        """确保顶层屏幕在window.sub_listeners的最后一位"""
        return False
