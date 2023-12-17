from pygame import Surface
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui import Renderer


class Sprite:
    """精灵"""
    def __init__(self, renderer: "Renderer"):
        self.renderer = renderer

    def tick(self, fps):
        ...

    def render(self, surface: Surface):
        ...

    @property
    def resourcemanager(self):
        return self.renderer.resourcemanager
