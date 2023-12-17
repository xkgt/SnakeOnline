from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional

from moretypes import Vector2, Serializable
from network import DataStream

if TYPE_CHECKING:
    from game import IGame


class Entity(Serializable):
    sub_classes: list[type["Entity"]] = []

    def __init__(self, pos: Vector2, motion: Vector2 = None):
        self.uuid = uuid4()
        self.pos = pos
        self.motion = motion or Vector2()
        self.killed = False
        self.game: Optional["IGame"] = None

    def update(self):
        ...

    def synchronize(self):
        """与客户端同步"""
        self.game.connectionlist.broadcast_update_entity(self)

    @property
    def entitymanager(self):
        return self.game.entitymanager

    def kill(self) -> bool:
        if not self.killed:
            self.killed = True
            self.entitymanager.remove(self)
            return True
        return False

    def collision(self, entity: "Entity") -> bool:
        ...

    def write(self, stream: DataStream, complete=True):
        """写入数据，complete:是否完整写入，用于创建实体"""
        if complete:
            stream << self.uuid
        stream << self.pos
        stream << self.motion

    def load(self, stream: DataStream, complete=False):
        """更新数据，complete:是否完整更新"""
        if complete:
            self.uuid = stream >> UUID
            self.killed = False  # 不写的话,新建时没有killed属性
        self.pos = stream >> Vector2
        self.motion = stream >> Vector2

    @classmethod
    def read(cls, stream: DataStream) -> "Entity":
        """读取数据，创建一个新的实体"""
        obj: Entity = object.__new__(cls)
        obj.load(stream, True)
        return obj

    def __init_subclass__(cls, **kwargs):
        cls.sub_classes.append(cls)
