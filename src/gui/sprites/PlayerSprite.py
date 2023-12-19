import pygame
from pygame import Surface, Rect
from game.entities import Player, Body
from .EntitySprite import EntitySprite


class PlayerSprite(EntitySprite[Player]):
    def __init__(self, renderer, entity: Player):
        super().__init__(renderer, entity)
        self.render_num = 0
        self.time = 0

    def tick(self, fps):
        if self.entity.dead:
            if self.entity.dead_time <= self.renderer.game.framerate:  # 一秒内
                self.time += 1
                if self.time > fps // self.entity.length - 1:
                    self.render_num -= 1
                    self.time = 0
        else:
            self.render_num = self.entity.length

    def render(self, surface: Surface):
        self.render_body(surface, self.entity, self.render_num)

    def render_body(self, surface: Surface, body: Body, count):
        if body.body:
            count -= 1
            if count > 0:
                self.render_body(surface, body.body, count)
        rect = Rect(body.pos*self.renderer.grid_size, (self.renderer.grid_size, self.renderer.grid_size))
        pygame.draw.rect(surface, self.entity.playerinfo.color if not self.entity.dead else (255, 0, 0), rect)
