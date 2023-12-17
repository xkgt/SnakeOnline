from typing import Optional

from moretypes import Vector2
from .Ball import Ball


class Body(Ball):
    radius = 20

    def __init__(self, pos, motion):
        super().__init__(pos, motion)
        self.body: Optional[Body] = None

    def update_chain(self, pos: Vector2, motion: Vector2):
        if self.body:
            if self.pos.calc_distance(self.body.pos) > self.radius * 1.5:  # 如果间距大于1.5倍半径
                self.body.update_chain(self.pos, self.motion)  # 更新
        self.pos = pos
        self.motion = motion

    def collision(self, ball: "Ball") -> bool:
        if super().collision(ball):
            return True
        if self.body:
            return self.body.collision(ball)
