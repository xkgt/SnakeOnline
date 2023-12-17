import pygame.draw

from resouces import ResourceManager
from .Widget import Widget
from resouces import transform
from game.entities import Player


class PlayerInfo(Widget):
    def __init__(self, player: Player, resourcemanager: ResourceManager):
        self.player = player
        self.resourcemanager = resourcemanager
        super().__init__(w=250, h=100)

    def render(self, surface, mousex: int, mousey: int):
        # 头像
        avatar_rect = self.rect.copy()
        avatar_rect.size = (self.rect.h, self.rect.h)  # 弄一个正方形
        surface.fill((255, 255, 255), avatar_rect)  # 填充白色背景
        avatar = transform.replacecolor(
            transform.scale(self.resourcemanager.hand, self.rect.h - 10, self.rect.h - 10), (0, 0, 0),
            self.player.color)
        surface.blit(avatar, avatar.get_rect(center=avatar_rect.center))  # 画头像
        pygame.draw.rect(surface, (0, 0, 0), avatar_rect, width=3)  # 画边框
        # 名字
        name_surface, name_rect = self.resourcemanager.font.render(self.player.name, (0, 0, 0), size=20)
        name_rect.left = self.rect.x + avatar_rect.width + 5
        name_rect.top = avatar_rect.top + 5
        surface.blit(name_surface, name_rect)
        # 长度
        len_text, len_rect = self.resourcemanager.font.render("长度：" + str(self.player.length), (0, 0, 0), size=20)
        len_rect.left = name_rect.left
        len_rect.top = name_rect.bottom + 5
        surface.blit(len_text, len_rect)
