from Ticker import Ticker
from network import DataStream
from .EntityManager import EntityManager
from .PlayerList import PlayerList
from moretypes import Size, Serializable


class IGame(Ticker, Serializable):
    """基础游戏属性"""
    def __init__(self, size: Size, framerate):
        from .ConnectionList import ConnectionList
        super().__init__(framerate)
        self.size = size
        self.entitymanager = EntityManager(self)
        self.connectionlist = ConnectionList()  # 连接列表
        self.playerlist = PlayerList()  # 玩家列表

    def write(self, stream: DataStream):
        stream << self.size
        stream << self.framerate

    @classmethod
    def read(cls, stream: DataStream):
        size = stream >> Size
        framerate = stream >> int
        return cls(size, framerate)
