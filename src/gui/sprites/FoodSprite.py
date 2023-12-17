from .EntitySprite import EntitySprite
from resouces import transform
from game.entities import Food


class FoodSprite(EntitySprite[Food]):

    def __init__(self, renderer, entity: Food):
        super().__init__(renderer, entity)

    def render(self, surface):
        img = transform.scale(
            self.resourcemanager.food,
            self.entity.radius * 2.5,
            self.entity.radius * 2.5
        )
        surface.blit(img, img.get_rect(center=self.entity.pos))
