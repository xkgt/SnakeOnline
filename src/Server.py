from game import IGame
from network import NetworkSystem
from Ticker import Ticker
from krpc import rpc, Side


class Server(Ticker):
    def __init__(self):
        rpc.side = Side.SERVER
        self.game = IGame()
        super().__init__(self.game.framerate)
        self.networksystem = NetworkSystem(self.game, port=18389)

    def tick(self, frame):
        self.networksystem.tick()
        self.game.tick(frame)

    def end(self):
        self.networksystem.close()
        self.game.end()


if __name__ == '__main__':
    import logging
    logging.basicConfig(handlers=[logging.StreamHandler()])
    server = Server()
    server.run()
