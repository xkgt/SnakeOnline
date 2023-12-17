from .Entity import Entity


class Ball(Entity):
    radius: int

    def collision(self, ball: "Ball") -> bool:
        """碰撞"""
        return self.pos.calc_distance(ball.pos) <= (self.radius + ball.radius)
