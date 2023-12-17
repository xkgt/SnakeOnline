import random
from moretypes import Vector2, Size
from .Ball import Ball


class Food(Ball):
    radius = 16

    def kill(self):
        if super().kill():
            self.entitymanager.add(self.random_pos_food(self.game.size))

    @classmethod
    def random_pos_food(cls, size: Size):
        return cls(Vector2(
            random.randint(cls.radius, size[0] - Food.radius),
            random.randint(cls.radius, size[1] - Food.radius)
        ))
