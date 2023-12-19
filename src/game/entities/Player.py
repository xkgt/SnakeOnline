import random

from DataStream import DataStream
from .Entity import Entity
from .Food import Food
from .Body import Body
from ..PlayerInfo import PlayerInfo
from ..Direction import Direction


class Player(Entity, Body):
    """玩家，就是蛇"""
    def __init__(self, pos, playerinfo: PlayerInfo, ai=False):
        super().__init__(pos)
        Body.__init__(self, pos)
        self.playerinfo = playerinfo
        self.death_time = 0
        self.death = False
        self.invincible_time = 8
        self.direction = Direction.RIGHT
        self.ai = ai
        self.length = 1

    def set_direction(self, direction: Direction):
        if self.body:
            if self.pos + direction.value == self.body.pos:
                return
        self.direction = direction
        if not self.death:
            self.move()
        self.synchronize()

    def move(self):
        pos = self.pos + self.direction.value
        size = self.game.size
        pos.x = pos.x % size.w  # 确保坐标在地图内
        pos.y = pos.y % size.h
        self.update_chain(pos)
        # 吃食物
        for food in self.entitymanager.all_of_type(Food):
            if food.collision(self):
                food.kill()
                self.add_body()
        if self.invincible_time == 0:
            # 碰撞
            for player in self.entitymanager.all_of_type(Player):
                if player.invincible_time == 0 and not player.death:
                    if player != self:
                        if player.collision(self):
                            self.die()
                            if Entity.collision(self, player):
                                player.die()
                    else:
                        if self.body and self.body.body:
                            if self.body.body.collision(self):
                                self.die()

    def collision(self, entity: "Body") -> bool:
        return Body.collision(self, entity)

    def update(self):
        if not self.death:
            if self.ai:  # ai操作
                if random.randint(0, 7) == 0:
                    self.set_direction(Direction.random_direction())
            # 移动
            self.move()
            # 无敌时间
            if self.invincible_time != 0:
                self.invincible_time -= 1
        else:  # 慢性死亡
            self.death_time -= 1
            if self.death_time == 0:
                self.kill()
        self.synchronize()

    def die(self):
        self.death = True
        self.death_time = 6

    def add_body(self):
        body = Body(self.pos)
        body.body = self.body
        self.body = body
        self.length += 1

    def write(self, stream: DataStream, complete=True):
        super().write(stream, complete)
        stream << self.playerinfo
        stream << self.invincible_time
        stream << self.length
        stream << self.direction
        stream << self.death
        if self.death:
            stream << self.death_time
        Body.write(self, stream)

    def load(self, stream: DataStream, complete=False):
        super().load(stream, complete)
        if complete:
            self.body = None
        self.playerinfo = stream >> PlayerInfo
        self.invincible_time = stream >> int
        self.length = stream >> int
        self.direction = stream >> Direction
        self.death = stream >> bool
        if self.death:
            self.death_time = stream >> int
        Body.load(self, stream)
