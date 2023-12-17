from typing import TYPE_CHECKING
from .Connection import Connection
import logging
import selectors
import socket
if TYPE_CHECKING:
    from game import IGame


class NetworkSystem:

    def __init__(self, game: "IGame", port=0):
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
                self.newconnect()
            else:
                self.read(key.data)

    def read(self, connecthandler: Connection):
        try:
            connecthandler.recv()
        except Exception as e:
            if isinstance(e, (AssertionError, IOError)):
                self.logger.info("断开连接 %s", connecthandler.conn.getpeername())
            else:
                self.logger.exception("断开连接 %s 原因:%s", connecthandler.conn.getpeername(), e)
            self.selector.unregister(connecthandler.conn)
            connecthandler.close()

    def newconnect(self):
        """处理新的连接"""
        conn, addr = self.serversocket.accept()
        self.logger.info("新的连接 %s", addr)
        conn.setblocking(False)
        connect = Connection(self.game, None, conn)
        self.selector.register(conn, selectors.EVENT_READ, data=connect)

    def close(self):
        self.serversocket.close()
        self.selector.close()
        self.serversocket = None
        self.selector = None
