from typing import Optional

from DataStream import DataStream
from moretypes import Vector2


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
