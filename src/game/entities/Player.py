import random
from typing import Optional

from DataStream import DataStream
from moretypes import Vector2
from .Entity import Entity
from .Food import Food
from ..Direction import Direction
from ..PlayerInfo import PlayerInfo


class Body:
    def __init__(self, pos):
        self.pos = pos
        self.body: Optional[Body] = None

    def update_chain(self, pos: Vector2):
        if self.body:
            if self.pos != self.body.pos:
                self.body.update_chain(self.pos)  # 更新
        self.pos = pos

    def collision(self, ball: "Body") -> bool:
        if self.pos == ball.pos:
            return True
        if self.body:
            return self.body.collision(ball)

    def write(self, stream: DataStream):
        stream << self.pos
        stream << (self.body is not None)
        if self.body:
            self.body.write(stream)

    def load(self, stream: DataStream):
        self.pos = stream >> Vector2
        has_body = stream >> bool
        if has_body:
            if not self.body:
                self.body = Body(None)
            self.body.load(stream)


class Player(Entity, Body):
    """玩家，就是蛇"""
    def __init__(self, pos, playerinfo: PlayerInfo, ai=False):
        super().__init__(pos)
        Body.__init__(self, pos)
        self.playerinfo = playerinfo
        self.dead = False  # 已死
        self.dead_time = 0  # 已死倒计时
        self.invincible_time = 8
        self.direction = Direction.RIGHT
        self.ai = ai
        self.length = 1

    def set_direction(self, direction: Direction):
        if self.body:
            if self.pos + direction.value == self.body.pos:
                return
        self.direction = direction
        if not self.dead:
            self.move()
        self.synchronize()

    def move(self):
        if not self.dead:
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
                    if player.invincible_time == 0 and not player.dead:
                        if player != self:
                            if player.collision(self):
                                self.die()
                                if Entity.collision(self, player):
                                    player.die()
                        else:  # 与自己碰撞
                            if self.body and self.body.body:
                                if self.body.body.collision(self):
                                    self.die()

    def collision(self, entity: "Body") -> bool:
        return Body.collision(self, entity)

    def update(self):
        if not self.dead:
            if self.ai:  # ai操作
                if random.randint(0, 3) == 0:
                    self.set_direction(self.direction.new_random_direction())
            # 移动
            self.move()
            # 无敌时间
            if self.invincible_time != 0:
                self.invincible_time -= 1
        else:  # 慢性死亡
            self.dead_time -= 1
            if self.dead_time == 0:
                self.kill()
        self.synchronize()

    def die(self):
        self.dead = True
        self.dead_time = 6

    def add_body(self):
        body = Body(self.pos)
        body.body = self.body
        self.body = body
        self.length += 1

    def write(self, stream: DataStream, complete=True):
        super().write(stream, complete)
        stream << self.playerinfo
        stream.write_short(self.invincible_time)
        stream << self.length
        stream << self.direction
        stream << self.dead
        if self.dead:
            stream << self.dead_time
        Body.write(self, stream)

    def load(self, stream: DataStream, complete=False):
        super().load(stream, complete)
        if complete:
            self.body = None
        self.playerinfo = stream >> PlayerInfo
        self.invincible_time = stream.read_short()
        self.length = stream >> int
        self.direction = stream >> Direction
        self.dead = stream >> bool
        if self.dead:
            self.dead_time = stream >> int
        Body.load(self, stream)
