from .Widget import Widget
from pygame import Surface


class Image(Widget):
    def __init__(self, image: Surface):
        self.image = image
        super().__init__(0, 0, *image.get_size())

    def render(self, surface: Surface, mousex: int, mousey: int):
        surface.blit(self.image, self.rect)
