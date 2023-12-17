from pygame import Surface


class Paintable:
    """可绘画"""
    def render(self, surface: Surface, mousex: int, mousey: int):
        ...
