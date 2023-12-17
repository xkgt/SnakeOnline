from network import DataStream
from .PlayerInfo import PlayerInfo
from moretypes import Serializable


class PlayerList(list[PlayerInfo], Serializable):
    def write(self, stream: DataStream):
        stream << len(self)
        for playerinfo in self:
            stream << playerinfo

    @classmethod
    def read(cls, stream: DataStream):
        player_list = PlayerList()
        size = stream >> int
        for i in range(size):
            playerinfo = stream >> PlayerInfo
            player_list.append(playerinfo)
        return player_list
