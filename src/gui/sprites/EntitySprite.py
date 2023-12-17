from typing import Generic, TypeVar

from .Sprite import Sprite
from game.entities import Entity

_T = TypeVar("_T", bound=Entity)


class EntitySprite(Sprite, Generic[_T]):
    ENTITY_SPRITE_MAP: dict[type[Entity], type["EntitySprite"]] = {}

    def __init__(self, renderer, entity: _T):
        super().__init__(renderer)
        self.entity = entity

    def __init_subclass__(cls, **kwargs):
        cls.ENTITY_SPRITE_MAP[cls.__orig_bases__[0].__args__[0]] = cls


del Entity
