from typing import TYPE_CHECKING
from .Connection import Connection
import logging
import selectors
import socket
if TYPE_CHECKING:
    from game import Game


class NetworkSystem:

    def __init__(self, game: "Game", port=0):
        self.game = game
        self.logger = logging.getLogger(NetworkSystem.__name__)
        self.logger.setLevel(logging.INFO)
        self.selector = selectors.DefaultSelector()
        self.serversocket = socket.create_server(("", port))
        self.logger.info("绑定端口 %d", self.serversocket.getsockname()[1])
        self.serversocket.setblocking(False)
        self.selector.register(self.serversocket, selectors.EVENT_READ, data=self)

    def tick(self):
        for key, mask in self.selector.select(timeout=0):
            if key.data == self:
                self.new_connect()
            else:
                self.read(key.data)

    def read(self, connection: Connection):
        try:
            connection.recv_data()
        except Exception as e:
            if isinstance(e, (AssertionError, IOError)):
                self.logger.info("断开连接 %s", connection.socket.getpeername())
            else:
                self.logger.exception("断开连接 %s 原因:%s", connection.socket.getpeername(), e)
            # raise e
            # self.selector.unregister(connection.socket)
            connection.close()

    def new_connect(self):
        """处理新的连接"""
        conn, addr = self.serversocket.accept()
        self.logger.info("新的连接 %s", addr)
        conn.setblocking(False)
        connection = Connection(sock=conn, game=self.game, networksystem=self)
        connection.login.enable()
        self.selector.register(conn, selectors.EVENT_READ, data=connection)

    def close(self, reason: str):
        self.logger.info(f"close: {reason}")
        self.game.connectionlist.broadcast_server_disconnect(reason)
        self.serversocket.close()
        for key in set(self.selector.get_map().values()):
            if key.data != self:
                key.data.close()
        self.selector.close()
        self.serversocket = None
        self.selector = None
