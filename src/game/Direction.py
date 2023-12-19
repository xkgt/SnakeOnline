from enum import Enum
from moretypes import Serializable
import random

from DataStream import DataStream


class Direction(Serializable, Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def new_random_direction(self):
        values = {self.UP, self.DOWN, self.RIGHT, self.LEFT}
        values.remove(self)
        return random.choice(list(values))

    @classmethod
    def random_direction(cls):
        values = {cls.UP, cls.DOWN, cls.RIGHT, cls.LEFT}
        return random.choice(list(values))

    def reverse(self):
        reverse_mapping = {
            self.UP: self.DOWN,
            self.DOWN: self.UP,
            self.LEFT: self.RIGHT,
            self.RIGHT: self.LEFT
        }
        return reverse_mapping[self]

    def write(self, stream: DataStream):
        stream.write_byte([self.UP, self.DOWN, self.RIGHT, self.LEFT].index(self))

    @classmethod
    def read(cls, stream: DataStream):
        return [cls.UP, cls.DOWN, cls.RIGHT, cls.LEFT][stream.read_byte()]
