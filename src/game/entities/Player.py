import random

from moretypes import Vector2

from .Food import Food
from .Body import Body
from ..PlayerInfo import PlayerInfo


class Player(Body):
    """玩家，就是蛇"""
    def __init__(self, pos, playerinfo: PlayerInfo, ai=False):
        super().__init__(pos, Vector2(0, 0))
        self.playerinfo = playerinfo
        self.death_time = 0
        self.speed = 21
        self.death = False
        self.ai = ai
        self.angle = 0
        self.invincible_time = 18
        self.length = 1

    def set_angle(self, angle):
        self.angle = angle

    def update(self):
        if not self.death:
            if self.ai:  # ai操作
                if random.randint(0, 14):
                    self.set_angle(random.randint(0, 360))
            # 移动
            pos: Vector2 = Vector2(self.pos.x + self.motion.x, self.pos.y + self.motion.y)
            size = self.game.size
            pos.x = pos.x % size.w  # 确保坐标在地图内
            pos.y = pos.y % size.h
            a = Vector2(self.speed, 0).rotate(self.angle)
            motion = self.motion + a
            motion.scale_to_length(self.speed)
            self.update_chain(pos, motion)
            # 吃食物
            for food in self.entitymanager.all_of_type(Food):
                if food.collision(self):
                    food.kill()
                    self.add_body()
            # 碰撞
            if self.invincible_time == 0:
                for player in self.entitymanager.all_of_type(Player):
                    if player != self:
                        if player.invincible_time == 0 and not player.death:
                            if player.collision(self):
                                self.die()
            else:
                self.invincible_time -= 1
        else:  # 慢性死亡
            self.death_time += 1
            if self.death_time >= 6 * 1.7:
                self.kill()

    def die(self):
        self.death = True

    def add_body(self):
        body = Body(self.pos, self.motion)
        body.body = self.body
        self.body = body
        self.length += 1

    # def write(self, stream: DataStream, complete=True):
    #     super().write(stream, complete)
    #
    # def write(self, data, complete: bool):
    #     super().write(data, complete)
    #     data.write_short(self.invincible_time)
    #     data.write_short(self.length)
    #     data.write_short(self.angle)
    #     data << self.death
    #     if self.death:
    #         data.write_short(self.death_time)
    #
    # def load(self, data, complete: bool):
    #     super().load(data, complete)
    #     self.invincible_time = data.read_short()
    #     self.length = data.read_short()
    #     self.angle = data.read_short()
    #     self.death = data >> bool
    #     self.hand = self
    #     if self.death:
    #         self.death_time = data.read_short()
