from typing import TypeVar, Union
from uuid import UUID
from typing import TYPE_CHECKING
from functools import cache

if TYPE_CHECKING:
    from game import IGame

from .entities import Entity

_T = TypeVar("_T", bound=Entity)


class EntityManager:
    """实体管理器"""

    def __init__(self, game: "IGame"):
        self.entities: dict[UUID, Entity] = {}
        self.game = game
        self.all_of_type = cache(self.all_of_type)  # 缓存

    def update(self):
        for entity in set(self.entities.values()):
            entity.update()

    def add(self, entity: _T) -> _T:
        self.entities[entity.uuid] = entity
        entity.game = self.game
        self.all_of_type.cache_clear()
        self.game.connectionlist.broadcast_create_entity(entity)
        return entity

    def all_of_type(self, type_: type[_T]) -> set[_T]:
        a = set()
        for i in self.entities.values():
            if isinstance(i, type_):
                a.add(i)
        return a

    def get_by_uuid(self, uuid: UUID, default=None):
        return self.entities.get(uuid, default)

    def remove(self, uuid_or_entity: Union[Entity, UUID]):
        if isinstance(uuid_or_entity, Entity):
            entity = self.entities.pop(uuid_or_entity.uuid)
        else:
            entity = self.entities.pop(uuid_or_entity)
        entity.kill()
        self.game.connectionlist.broadcast_remove_entity(entity)
        self.all_of_type.cache_clear()

    def __iter__(self):
        return self.entities.values().__iter__()

    def __getitem__(self, item: UUID):
        return self.get_by_uuid(item)
