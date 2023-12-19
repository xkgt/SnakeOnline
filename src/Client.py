import logging
import time
from typing import Optional, Callable

from pygame.time import Clock

from GameSide import GameSide
from Ticker import Ticker
from game import IGame, Game
from gui import Window, Renderer
from gui.screens import InfoScreen, TitleScreen, GameScreen
from network import Connection
from resouces import ResourceManager


class Client(Ticker, GameSide):
    instance: "Client"

    def __init__(self, resourcemanager: ResourceManager):
        self.instance = self
        self.resourcemanager = resourcemanager
        self.config = resourcemanager.config
        GameSide.__init__(self)
        Ticker.__init__(self, self.config.fps)
        # 日志
        self.logger = logging.getLogger(Client.__name__)
        self.logger.setLevel(logging.INFO)

        self.window = Window(self)
        self.renderer: Optional[Renderer] = None  # 进游戏时存在

        self.connection: Optional[Connection] = None  # 进游戏时存在

        self.tpsdetector = Clock()
        self.currenttps = 0

    @property
    def player(self):
        if self.connection and self.connection.player and not self.connection.player.killed:
            return self.connection.player
        return None

    def tick(self, frame):
        self.window.tick(frame)
        if self.game:
            if frame % (self.framerate // self.game.framerate) == 0:  # 模拟tps
                self.game.tick(frame // self.game.framerate)
                self.tpsdetector.tick(0)
                self.currenttps = self.tpsdetector.get_fps()
        if self.networksystem:
            self.networksystem.tick()
        if self.connection and not self.connection.is_local():
            try:
                self.connection.recv_data()
            except BlockingIOError:
                ...
            except Exception as e:
                self.logger.exception(e)
                self.disconnect()
                self.window.setscreen(InfoScreen(TitleScreen(), str(e)))
        if self.renderer:
            self.renderer.tick(frame)
        self.window.update()

    def connect(self, address, lastscreen):
        self.disconnect()
        run = True

        def stop():
            nonlocal run
            run = False

        def connect():
            try:
                self.connection = self.create_connection()
                self.connection.connect_to(address)
                self.connection.socket.setblocking(False)
                if run:
                    sc = InfoScreen(lastscreen, "正在登录", None, False)
                    self.window.setscreen(sc)
                    # 登录
                    self.connection.login(self.resourcemanager.config.name)
                    time.sleep(5)
                    if self.window.screen == sc:  # 还是登录屏幕，代表连接出问题
                        self.disconnect()
                        self.window.setscreen(InfoScreen(lastscreen, "服务器未响应"))
                else:
                    self.disconnect()
            except Exception as e:
                if run:
                    self.disconnect()
                    self.window.setscreen(InfoScreen(lastscreen, f"连接失败：{e}", None))

        self.window.setscreen(InfoScreen(lastscreen, "正在连接", stop))
        self.backgroundexecutor.submit(connect)

    def create_connection(self) -> Connection:
        connection = Connection(client=self)
        # 启用处理器
        connection.set_playerinfo.enable()  # 允许设置玩家信息
        connection.set_game.enable()  # 游戏
        connection.login_success.enable()  # 登录回复
        connection.server_disconnect.enable()  # 服务器关闭
        return connection

    def disconnect(self):
        """断开连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
        if self.game:
            self.game.end()
            self.game: Optional[IGame] = None
        if self.networksystem:
            self.networksystem.close("服务器关闭")
            self.networksystem = None
        self.renderer = None

    def start_game(self):
        self.game = Game()
        self.game.start()
        self.connection = self.create_connection()
        self.game.handle_join(self.connection, self.config.name)
        if self.config.playsound:
            self.resourcemanager.play_single_music()

    def join_game(self, game: IGame):
        """加入游戏"""
        self.game = game
        self.renderer = Renderer(self, self.resourcemanager, game)
        if not self.connection.is_local():
            self.window.setscreen(GameScreen())

    def start(self, callback: Callable[["Client"], None] = None):
        if callback:
            self.resourcemanager.load(self, None, lambda: callback(self))
        else:
            self.resourcemanager.load(self, TitleScreen(), self.start_game)
        self.run()

    def end(self):
        self.disconnect()
        self.backgroundexecutor.shutdown()
        self.window.close()
