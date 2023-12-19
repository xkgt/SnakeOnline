from pygame import Surface

from gui import layouts
from .Screen import Screen
from gui.widgets import ProgressBar, Label


class InitScreen(Screen):
    def __init__(self, maxvalue, screen=None, callback=None):
        super().__init__()
        self.maxvalue = maxvalue
        self.value = 0
        self.displayvalue = 0
        self.screen = screen
        self.callback = callback

        self.surface = None  # 用于与标题界面切换的屏幕
        self.progressbar = None
        self.labelcenter = None

        self.x = 0  # 显示坐标
        self.t = 0  # 加载完成后的停留时间

    def init(self, width, height):
        if self.screen:
            self.window.initscreen(self.screen)
        self.surface = Surface((width, height))
        self.progressbar = ProgressBar(700, 30, self.maxvalue * 100)
        layouts.vertical_layout(
            self.addwidget(label := Label(self.font, "正在初始化游戏", size=45, fgcolor=(255, 0, 0))),
            self.addwidget(self.progressbar),
            centerx=width // 2, top=(height - label.rect.h) // 2 - 60, interval=60
        )
        self.labelcenter = label.rect.center

    def add(self):
        self.value += 1
        if self.value >= self.maxvalue:
            self.widgets[0] = (a := Label(self.font, "初始化完毕", size=45, fgcolor=(50, 50, 255)))
            a.rect.center = self.labelcenter

    def tick(self, frame):
        self.progressbar.value = self.displayvalue
        if self.value >= self.maxvalue:
            if self.t == 0:  # 加载完成后启动游戏
                if self.callback:
                    self.callback()
            if self.screen:
                self.screen.tick(frame)

    def render(self, surface, mousex: int, mousey: int):
        self.surface.fill((255, 255, 255))
        super().render(self.surface, mousex, mousey)

        a = (self.value+1) * 100 - self.displayvalue
        if a > 0:
            self.displayvalue += a * 0.09
            self.displayvalue = min(self.displayvalue, self.maxvalue * 100)

        if self.value >= self.maxvalue:
            self.screen.render(surface, mousex, mousey)
            if self.t >= self.client.framerate // 2:
                self.x += self.width / self.client.framerate * 5
            else:
                self.t += 1
        if self.x >= self.width:
            self.window.setscreen(self.screen)
        else:
            rect = self.window.rect
            rect.x = self.x
            surface.blit(self.surface, rect)
