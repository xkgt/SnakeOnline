from network import Connection
from functools import wraps
from .entities import Entity
from .PlayerList import PlayerList


def broadcast(package):
    def a(func):
        @wraps(func)
        def b(self, *args):
            for connection in self:
                package(connection, *args)
        return b
    return a


class ConnectionList(list[Connection]):
    @broadcast(Connection.create_entity)
    def broadcast_create_entity(self, entity: Entity):
        ...

    @broadcast(Connection.remove_entity)
    def broadcast_remove_entity(self, entity: Entity):
        ...

    @broadcast(Connection.server_close)
    def broadcast_server_close(self, message: str):
        ...

    @broadcast(Connection.update_playerlist)
    def broadcast_update_playerlist(self, playerlist: PlayerList):
        ...

    @broadcast(Connection.update_entity)
    def broadcast_update_entity(self, entity: Entity):
        ...
