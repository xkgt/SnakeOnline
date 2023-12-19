from .Config import Config
from pygame.freetype import Font
from pygame.mixer import Sound
from pygame import Surface
import pygame


# noinspection PyTypeChecker
class ResourceManager:
    def __init__(self, config: Config):
        self.__futures: dict[str, Future] = {}
        self.config = config
        self.icon = pygame.image.load("img/icon.png")  # 图标
        self.font = Font("font/biliw.otf")  # 字体

        # 不卡的资源可以直接加载
        self.food = pygame.image.load("img/apple.png")
        self.volume = pygame.image.load("img/volume.png")
        self.mute = pygame.image.load("img/mute.png")

        # 需要预处理的资源
        def aa(surface: Surface):
            """透明背景"""
            x = surface.convert_alpha()  # 需要有窗口才能用
            with pygame.PixelArray(x) as p:
                p.replace((255, 255, 255), (0, 0, 0, 0))
            return x

        self.snake: Surface = Future(pygame.image.load, "img/snake.bmp", callback=aa)

        def a(sound: Sound):
            """降低声响"""
            sound.set_volume(0.3)
        self.single_music: Sound = Future(Sound, "sound/single.mp3", callback=a)
        self.online_music: Sound = Future(Sound, "sound/online.mp3", callback=a)

    def load(self, client, screen, callback):
        from gui.screens import InitScreen
        screen = InitScreen(len(self.__futures), screen, callback)
        client.window.setscreen(screen)

        def a():
            for k, v in self.__futures.items():
                setattr(self, k, v.get_value())
                screen.add()
        client.backgroundexecutor.submit(a)

    def __setattr__(self, key, value):
        if isinstance(value, Future):
            self.__futures[key] = value
        super().__setattr__(key, value)

    def play_single_music(self):
        self.online_music.stop()
        if not self.single_music.get_num_channels():
            self.single_music.play(-1)

    def play_online_music(self):
        self.single_music.stop()
        if not self.online_music.get_num_channels():
            self.online_music.play(-1)

    def stop_music(self):
        self.single_music.stop()
        self.online_music.stop()


class Future:
    def __init__(self, cls, *args, callback=None, **kwargs):
        self.cls = cls
        self.args = args
        self.kwargs = kwargs
        self.callback = callback

    def get_value(self):
        a = self.cls(*self.args, **self.kwargs)
        if self.callback:
            b = self.callback(a)
            if b:
                return b
        return a

    def __getattr__(self, item):
        return lambda *args, **kwargs: ...
