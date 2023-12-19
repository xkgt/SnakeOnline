from typing import TYPE_CHECKING

from .Entity import Entity
if TYPE_CHECKING:
    from ..IGame import IGame


class Food(Entity):

    def kill(self):
        if super().kill():
            if self.game.is_run_in_server:
                self.entitymanager.add(self.random_pos_food(self.game))

    @classmethod
    def random_pos_food(cls, game: "IGame"):
        return cls(game.random_pos())
