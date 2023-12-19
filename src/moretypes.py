import math
from collections import namedtuple
from uuid import UUID
from DataStream import DataStream
from pygame import Color as _Color, Vector2 as _Vector2

__all__ = [
    "Color",
    "Size",
    "Vector2",
    "Serializable",
    "UUID_NULL"
]


class Serializable:
    @classmethod
    def read(cls, stream: DataStream):
        args = []
        for type_ in cls.__annotations__.values():
            args.append(stream >> type_)
        return cls(*args)

    def write(self, stream: DataStream):
        for key in self.__annotations__.keys():
            value = getattr(self, key)
            stream << value


class Color(_Color, Serializable):
    def __hash__(self):
        return hash((self[0], self[1], self[2], self[3]))

    @classmethod
    def read(cls, stream: DataStream):
        return cls(*stream.read(4))

    def write(self, stream: DataStream):
        stream.write(self)


class Vector2(_Vector2, Serializable):
    def __hash__(self):
        return hash((self[0], self[1]))

    def calc_distance(self, vector2: "Vector2") -> float:
        return math.hypot(self[0] - vector2[0], self[1] - vector2[1])

    @classmethod
    def read(cls, stream: DataStream):
        return cls(stream >> float, stream >> float)

    def write(self, stream: DataStream):
        stream << self.x << self.y


class Size(namedtuple("Size", ["w", "h"]), Serializable):
    def __new__(cls, w, h):
        return super().__new__(cls, w, h)

    @classmethod
    def read(cls, stream: DataStream):
        return cls(stream >> int, stream >> int)

    def write(self, stream: DataStream):
        stream << self.w << self.h


UUID_NULL = UUID(int=0)
