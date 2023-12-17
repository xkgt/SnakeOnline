import random

import pygame
from pygame import Surface, Rect

from game.entities import Player
from moretypes import Vector2, Color
from .Screen import Screen
from gui import layouts
from gui.widgets import Label
from game import PlayerInfo


class GameScreen(Screen):
    #     def __init__(self):
    #         super().__init__()
    #     self.playerinfomap: dict[Player, PlayerInfo] = {}
    #

    def init(self, width, height):
        widgets = [
            self.addwidget(Label(self.font, "按e设置音乐", size=20, fgcolor=(255, 255, 255))),
        ]
        if self.client.connection.is_local():
            widgets.insert(1, self.addwidget(Label(self.font, "按o添加人机", size=20, fgcolor=(255, 255, 255))))
            self.addwidget(Label(self.font, "按z增加长度", size=20, fgcolor=(255, 255, 255))),

        layouts.vertical_layout(
            *widgets,
            bottomleft=(5, height - 5)
        )

    def tick(self, frame):
        # for player in self.client.game.entitymanager.all_of_type(Player):
        #     if player not in self.playerinfomap:
        #         self.playerinfomap[player] = PlayerInfo(player, self.resourcemanager)
        # for player, playerinfo in tuple(self.playerinfomap.items()):
        #     if player.killed:
        #         self.playerinfomap.pop(player)
        if self.client.player:
            if self.mouse_in_game():
                x, y = self.get_game_mouse_pos()
                angle = Vector2(x - self.client.player.pos[0], y - self.client.player.pos[1]).as_polar()[1]
                self.client.connection.set_angle(angle)

    def keydown(self, unicode, key, mod, **kwargs):
        if key == pygame.K_o:
            if self.client.connection.is_local():
                player = self.client.game.entitymanager.add(Player(
                    Vector2(
                        random.randint(Player.radius, self.client.game.size[0] - Player.radius),
                        random.randint(Player.radius, self.client.game.size[1] - Player.radius)
                    ),
                    PlayerInfo("AI", Color(0, 0, 0)), ai=True
                ))
                for i in range(5):
                    player.addbody()
            else:
                self.window.topscreen.tip("你不是房主", 0.3)
        elif key == pygame.K_z:
            if self.client.game:
                if self.client.player and not self.client.player.death:
                    self.client.player.add_body()
            else:
                self.window.topscreen.tip("你不是房主", 0.3)

    def render(self, surface: Surface, mousex: int, mousey: int):
        super().render(surface, mousex, mousey)
        # 绘制游戏屏幕
        rect = self.get_game_screen_rect()
        x, y = self.get_game_mouse_pos()
        self.client.renderer.render(self.mouse_in_game(), x, y)
        surface.blit(self.client.renderer.screen, rect)
        # 绘制玩家信息
        # widgets = self.playerinfomap.values()
        # x = (self.window.rect.width - rect.width) / 5
        # if widgets:
        #     layouts.vertical_layout(*widgets, y=x, centerx=x * 2)
        # for widget in widgets:
        #     widget.render(surface, mousex, mousey)

    def mousebuttondown(self, pos, button, **kwargs):
        if button == 1:
            if not self.client.player:
                if self.mouse_in_game():
                    x, y = self.get_game_mouse_pos()
                    self.client.connection.request_create_player(Vector2(x, y))
                    raise StopIteration

    def get_game_screen_rect(self):
        rect = Rect((0, 0), self.client.game.size)
        rect.centery = self.window.rect.centery
        x = 250 + 20 + 20
        rect.centerx = x + (self.width - x) / 2
        return rect

    def mouse_in_game(self):
        return self.get_game_screen_rect().collidepoint(*self.getmousepos())

    def get_game_mouse_pos(self):
        """获得游戏内鼠标坐标"""
        rect = self.get_game_screen_rect()
        x, y = self.getmousepos()
        return x - rect.x, y - rect.y

    def back(self):
        from .TitleScreen import TitleScreen
        self.window.setscreen(TitleScreen())
