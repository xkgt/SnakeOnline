from .IGame import IGame
from .PlayerInfo import PlayerInfo
from .entities import Player, Food
from network import Connection
from moretypes import Size, Color


class Game(IGame):
    """贪吃蛇游戏"""

    def __init__(self):
        IGame.__init__(self, Size(1000, 800), 6)
        # 玩家颜色列表，也是最大玩家数
        self.colors: list[Color] = [Color(30, 233, 30), Color(0, 0, 255), Color(255, 0, 255), ]

    def tick(self, frame):
        self.entitymanager.update()

    def start(self):
        """启动游戏"""
        self.entitymanager.add(Food.random_pos_food(self.size))

    def handle_join(self, connection: Connection, name):
        """添加新的连接"""
        if not self.colors:  # 是否还有多余的颜色
            raise RuntimeError("人数已满")
        for c in self.connectionlist:  # 是否名字一样
            if c.playerinfo.name == name:
                name = f"Player_{name}"
                break
        playerinfo = PlayerInfo(name, self.colors.pop(0))
        # 成功加入，设置客户端信息
        connection.set_playerinfo(playerinfo)
        connection.set_game(self)
        for entity in self.entitymanager:
            connection.create_entity(entity)
        # 启用和禁用请求
        connection.request_create_player.enable()
        connection.set_angle.enable()
        connection.login.disable()
        # 添加
        self.connectionlist.append(connection)
        self.playerlist.append(playerinfo)
        self.connectionlist.broadcast_update_playerlist(self.playerlist)

    def handle_exit(self, connection: Connection):
        """处理退出"""
        self.colors.append(connection.playerinfo.color)
        self.connectionlist.remove(connection)
        self.playerlist.remove(connection.playerinfo)
        self.connectionlist.broadcast_update_playerlist(self.playerlist)

    def create_player(self, pos, connection: Connection) -> Player:
        """创建新蛇(玩家)"""
        player = Player(pos, connection.playerinfo)
        connection.playerinfo.uuid = player.uuid
        self.entitymanager.add(player)
        for i in range(4):
            player.add_body()
        connection.set_player(player)
        # 更新玩家列表
        self.connectionlist.broadcast_update_playerlist(self.playerlist)
        return player
