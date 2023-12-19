from GameSide import GameSide
from game import Game
from network import NetworkSystem
from Ticker import Ticker


class Server(Ticker, GameSide):
    def __init__(self, port):
        super().__init__(20)
        GameSide.__init__(self)
        self.game = Game()
        self.game.start()
        self.networksystem = NetworkSystem(self.game, port)

    def tick(self, frame):
        self.networksystem.tick()
        if frame % (self.framerate // self.game.framerate) == 0:
            self.game.tick(frame)

    def end(self):
        self.networksystem.close("服务器关闭")
        self.game.end()
