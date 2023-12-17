from uuid import UUID

from moretypes import Color, Serializable, UUID_NULL
from dataclasses import dataclass


@dataclass
class PlayerInfo(Serializable):
    name: str
    color: Color
    uuid: UUID = UUID_NULL
