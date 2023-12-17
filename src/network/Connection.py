import socket
import logging
import struct
from typing import Optional, TYPE_CHECKING
from uuid import UUID
from moretypes import *

from .DataStream import DataStream
from game.entities import Player, Entity
from game import Game, IGame, PlayerInfo, PlayerList
if TYPE_CHECKING:
    from Client import Client
from .package import *


# noinspection PyUnusedLocal
class Connection(Handler):
    def __init__(self, sock: Optional[socket.socket] = None, client: Optional["Client"] = None,
                 game: Optional[Game] = None):
        super().__init__()
        self.logger = logging.getLogger(Connection.__name__)
        self.logger.setLevel(logging.INFO)
        self.socket = sock  # 如果是客户端本地模式，则没有
        self.client = client  # 如果是服务端，则没有
        self.game = game  # 如果是服务端，那一开始就有，如果是客户端，在handle_set_game后有，类型为IGame
        self._cache = bytearray()
        # 游戏
        self.playerinfo: Optional[PlayerInfo] = None
        self.player: Optional[Player] = None
        self.player_num = 0  # 玩家数量

    def connect_to(self, address):
        self.socket = socket.create_connection(address)

    def send_data(self, pkg_name, *args):
        if self.is_local():
            package = self.handlers.get(pkg_name, None)
            if not package:
                raise KeyError(f"未知包:{pkg_name} {args}")
            package.handle(*args)
        else:
            stream = DataStream()
            stream << pkg_name
            for arg in args:
                if isinstance(arg, Entity):  # 如果是实体类
                    stream << arg.uuid  # 就发送uuid
                else:
                    stream << arg
            size = len(stream.getvalue())
            self.socket.send(struct.pack("i", size))
            self.socket.sendall(stream.getvalue())

    def recv_data(self):
        assert not self.is_local()
        self._cache += self.socket.recv(10000)
        while len(self._cache) > 4:
            size = struct.unpack("i", self._cache)[0]
            if len(self._cache) >= size + 4:
                stream = DataStream(memoryview(self._cache)[4:size])
                pkg_name = stream >> str
                package = self.handlers.get(pkg_name, None)
                if not package:
                    raise KeyError(f"未知包:{pkg_name}")
                args = []
                for parameter in package.parameters:
                    if issubclass(parameter, Entity):  # 如果参数继承实体
                        uuid = stream >> UUID  # 就读取uuid
                        arg = self.game.entitymanager[uuid]  # 获取实体
                    else:
                        arg = stream >> parameter
                    args.append(arg)
                del self._cache[:size + 4]
                package.handle(*args)
            else:
                break

    def is_local(self):
        return self.socket is None

    def close(self):
        if self.socket:
            self.socket.close()

    @in_client
    def login(self, name: str):
        """登录"""
        remote_call()

    @login.set_handler
    def handle_login(self, name: str):
        try:
            self.game.handle_join(self, name)
        except Exception as e:
            self.login_reply(False, str(e))
        else:
            self.login_reply(True)

    @in_server
    def set_playerinfo(self, playerinfo: PlayerInfo):
        """设置客户端信息"""
        self.playerinfo = playerinfo
        remote_call()

    @set_playerinfo.set_handler
    def handle_set_playerinfo(self, playerinfo: PlayerInfo):
        self.playerinfo = playerinfo

    @in_server
    def login_reply(self, success: bool, message: str = None):
        """登录回复"""
        remote_call(success, message or "")

    @login_reply.set_handler
    def handle_login_reply(self, success: bool, message: str):
        from gui.screens import InfoScreen, TitleScreen, GameScreen
        if not success:  # 如果没成功
            self.client.disconnect()
            self.client.window.setscreen(InfoScreen(TitleScreen(), "登录失败:" + message))
        else:
            self.login_reply.disable()  # 登录完成，禁止登录回复
            self.logger.info("已连接至服务器")
            self.client.window.setscreen(GameScreen())

    @in_client
    def request_create_player(self, pos: Vector2):
        """请求创建玩家"""
        remote_call()

    @request_create_player.set_handler
    def handle_request_create_player(self, pos: Vector2):
        # 如果不希望客户端可以随便重设玩家，可以修改逻辑
        if self.player:
            self.player.kill()
        self.game.create_player(pos, self)

    @in_server
    def set_game(self, game: IGame):
        """设置游戏"""
        remote_call()

    @set_game.set_handler
    def handle_set_game(self, game: IGame):
        self.game = game
        self.create_entity.enable()
        self.remove_entity.enable()
        self.update_playerlist.enable()
        self.set_player.enable()
        self.client.join_game(game)

    @in_server
    def update_playerlist(self, playerlist: PlayerList):
        remote_call()

    @update_playerlist.set_handler
    def handle_update_playerlist(self, playerlist: PlayerList):
        self.game.playerlist = playerlist

    @in_server
    def create_entity(self, entity: Entity):
        """创建实体"""
        if not self.is_local():  # 如果是本地模组，则不发送
            id_ = Entity.sub_classes.index(entity.__class__)
            stream = DataStream()
            stream << entity
            remote_call(id_, stream.getvalue())  # 绕过uuid发送

    @create_entity.set_handler
    def handle_create_entity(self, id_: int, data: bytes):
        stream = DataStream(data)
        type_ = Entity.sub_classes[id_]
        entity = stream >> type_
        self.game.entitymanager.add(entity)

    @in_server
    def update_entity(self, entity: Entity):
        if not self.is_local():
            stream = DataStream()
            entity.write(stream, False)
            remote_call(entity, stream.getvalue())  # 发送时entity会转为uuid

    @update_entity.set_handler
    def handle_update_entity(self, entity: Entity, data: bytes):
        # 接收时uuid会转为entity
        entity.load(DataStream(data))

    @in_server
    def remove_entity(self, entity: Entity):
        if not self.is_local():
            remote_call()

    @remove_entity.set_handler
    def handle_remove_entity(self, entity: Entity):
        self.game.entitymanager.remove(entity)

    @in_server
    def set_player(self, player: Player):
        """设置客户端玩家"""
        self.player = player
        remote_call()

    @set_player.set_handler
    def handle_set_player(self, player: Player):
        self.player = player

    @in_client
    def set_angle(self, angle: float):
        remote_call()

    @set_angle.set_handler
    def handle_set_angle(self, angle: float):
        self.player.set_angle(angle)

    @in_server
    def server_close(self, message: str):
        remote_call()

    @server_close.set_handler
    def handle_server_close(self, message: str):
        from gui.screens import InfoScreen, TitleScreen
        self.client.disconnect()
        self.client.window.setscreen(InfoScreen(TitleScreen(), message))
