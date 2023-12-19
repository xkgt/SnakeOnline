from typing import TYPE_CHECKING

import pygame.transform
from pygame import Surface

from game import IGame
from resouces import ResourceManager

if TYPE_CHECKING:
    from Client import Client
from game.entities import *
from gui.sprites import *


class Renderer:
    """负责游戏窗口绘制"""
    def __init__(self, client: "Client", resourcemanager: ResourceManager, game: IGame):
        self.client = client
        self.resourcemanager = resourcemanager
        self.game = game
        self.grid_size = 30
        # 地图虽然很小，但像素得高点
        self.screen = Surface((game.size.w*self.grid_size, game.size.h*self.grid_size), pygame.SRCALPHA)

    def tick(self, frame):
        for entity in self.game.entitymanager:
            if not hasattr(entity, "sprite"):
                sprite_cls = EntitySprite.ENTITY_SPRITE_MAP.get(entity.__class__, None)
                if sprite_cls:
                    setattr(entity, "sprite", sprite_cls(self, entity))
            sprite: Sprite = getattr(entity, "sprite", None)
            if sprite:
                sprite.tick(self.client.framerate)

    def render(self, focus: bool, mousex: int, mousey: int):
        self.screen.fill((0, 0, 0))
        for entity in self.game.entitymanager:
            sprite: Sprite = getattr(entity, "sprite", None)
            if sprite:
                sprite.render(self.screen)
        if focus:  # 如果鼠标在屏幕类
            if not self.client.player:
                mousex = mousex // self.grid_size * self.grid_size
                mousey = mousey // self.grid_size * self.grid_size

                text, rect = self.resourcemanager.font.render("点击放置新蛇", fgcolor=(255, 0, 0), size=self.grid_size)
                rect.centerx = mousex
                rect.top = mousey + self.grid_size
                self.screen.blit(text, rect)
                pygame.draw.rect(
                    self.screen,
                    self.client.connection.playerinfo.color,
                    (mousex, mousey, self.grid_size, self.grid_size),
                    width=4)
