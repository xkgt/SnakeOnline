from typing import TYPE_CHECKING, Optional

from pygame import Surface
import pygame

from gui.Listener import Listener
from gui.screens import TopScreen

if TYPE_CHECKING:
    from Client import Client
from gui.screens import Screen


# noinspection PyMethodMayBeStatic
class Window(Listener):
    """窗口，管理输入事件"""

    def __init__(self, client: "Client"):
        super().__init__()
        self.client = client
        pygame.display.set_caption("多人对战")
        pygame.display.set_icon(client.resourcemanager.icon)
        # 创建屏幕
        self.surface: Surface = pygame.display.set_mode((1200, 750), pygame.SRCALPHA | pygame.RESIZABLE)
        self.screen: Optional[Screen] = None  # 当前屏幕，可能不存在
        self.topscreen = TopScreen()
        self.addlistener(self.topscreen)
        self.initscreen(self.topscreen)

    def tick(self, frame):
        self.handle_event()
        if self.screen:
            self.screen.tick(frame)
        self.topscreen.tick(frame)

    def update(self):
        self.surface.fill((168, 152, 231))
        if self.screen:
            self.renderscreen(self.screen)
        self.renderscreen(self.topscreen)
        pygame.display.flip()

    def setscreen(self, screen: Optional[Screen]):
        """设置显示屏幕"""
        if self.screen:
            self.sub_listeners.remove(self.screen)
            self.screen.close()
        self.screen = screen
        if screen:
            self.sub_listeners.add(screen)
            self.initscreen(screen)

    def initscreen(self, screen: Screen):
        screen.client = self.client
        screen.width, screen.height = self.rect.size
        screen.widgets.clear()
        screen.sub_listeners.clear()
        screen.init(*self.rect.size)

    def renderscreen(self, screen: Screen):
        screen.render(self.surface, *screen.getmousepos())

    @property
    def rect(self):
        return self.surface.get_rect()

    def close(self):
        pygame.quit()

    def quit(self, **kwargs):
        self.client.stop()

    def getmousepos(self):
        return pygame.mouse.get_pos()

    def windowsizechanged(self, **kwargs):
        if self.screen:
            self.initscreen(self.screen)
        self.initscreen(self.topscreen)
