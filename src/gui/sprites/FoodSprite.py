from .EntitySprite import EntitySprite
from resouces import transform
from game.entities import Food


class FoodSprite(EntitySprite[Food]):

    def __init__(self, renderer, entity: Food):
        super().__init__(renderer, entity)

    def render(self, surface):
        img = transform.scale(
            self.resourcemanager.food,
            self.renderer.grid_size,
            self.renderer.grid_size
        )
        surface.blit(img, img.get_rect(topleft=self.entity.pos*self.renderer.grid_size))
