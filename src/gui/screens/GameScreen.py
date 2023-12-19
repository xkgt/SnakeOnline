import pygame
from functools import lru_cache
from pygame import Surface, Rect

from game.entities import Player
from moretypes import Vector2, Color
from resouces import transform
from .Screen import Screen
from gui import layouts
from gui.widgets import Label
from game import PlayerInfo, Direction


class GameScreen(Screen):
    def __init__(self):
        super().__init__()
        self.game_render_rect = None
        self.lru_replacecolor = lru_cache(10)(transform.replacecolor)
        self.lru_scale = lru_cache(10)(transform.scale)

    def init(self, width, height):
        widgets = [
            self.addwidget(Label(self.font, "按e设置音乐", size=20, fgcolor=(255, 255, 255))),
        ]
        if self.client.connection.is_local():
            widgets.insert(1, self.addwidget(Label(self.font, "按o添加人机", size=20, fgcolor=(255, 255, 255))))
            widgets.insert(1, self.addwidget(Label(self.font, "按z增加长度", size=20, fgcolor=(255, 255, 255))))

        layouts.vertical_layout(
            *widgets,
            bottomleft=(5, height - 5)
        )
        # 设置游戏绘制区域
        x = 250  # 游戏区域x
        w = self.width - x - 30
        self.game_render_rect = Rect((x, 0), (max(w, 10), self.height - 60))
        self.game_render_rect.centery = self.window.rect.centery

    def render(self, surface: Surface, mousex: int, mousey: int):
        super().render(surface, mousex, mousey)
        # 绘制游戏屏幕
        self.render_game(surface, mousex, mousey, self.game_render_rect, True)
        # 绘制玩家信息
        x = y = 30
        for playerinfo in self.client.game.playerlist:
            self.render_playerinfo(surface, playerinfo, x, y)
            y += 130

    def render_playerinfo(self, surface: Surface, playerinfo: PlayerInfo, x, y):
        """绘制玩家信息，占250*100大小"""
        player = self.client.game.entitymanager.get_by_uuid(playerinfo.uuid, None)

        avatar_rect = Rect(x, y, 100, 100)
        surface.fill((255, 255, 255), avatar_rect)  # 填充白色背景

        if player:  # 如果有玩家就画头像
            avatar = self.lru_replacecolor(
                self.lru_scale(self.resourcemanager.snake, avatar_rect.h - 10, avatar_rect.h - 10), (0, 0, 0),
                playerinfo.color)
            surface.blit(avatar, avatar.get_rect(center=avatar_rect.center))
        pygame.draw.rect(surface, (0, 0, 0), avatar_rect, width=3)  # 画边框
        # 名字
        name_surface, name_rect = self.resourcemanager.font.render(playerinfo.name, (0, 0, 0), size=20)
        name_rect.left = avatar_rect.right + 5
        name_rect.top = avatar_rect.top + 5
        surface.blit(name_surface, name_rect)
        # 如果有玩家就画长度
        if player:
            len_text, len_rect = self.resourcemanager.font.render("长度：" + str(player.length), (0, 0, 0), size=20)
            len_rect.left = name_rect.left
            len_rect.top = name_rect.bottom + 5
            surface.blit(len_text, len_rect)

    def keydown(self, unicode, key, mod, **kwargs):
        if key == pygame.K_o:
            # 新建ai玩家
            if self.client.connection.is_local():
                player = Player(self.client.game.random_pos(), PlayerInfo("AI", Color(255, 255, 0)), ai=True)
                self.client.game.entitymanager.add(player)
                for i in range(5):
                    player.add_body()
            else:
                self.window.topscreen.tip("你不是房主", 0.3)
        elif key == pygame.K_z:
            # 添加长度
            if self.client.connection.is_local():
                if self.client.player and not self.client.player.death:
                    self.client.player.add_body()
            else:
                self.window.topscreen.tip("你不是房主", 0.3)
        else:
            key_map = {
                pygame.K_w: Direction.UP,
                pygame.K_s: Direction.DOWN,
                pygame.K_a: Direction.LEFT,
                pygame.K_d: Direction.RIGHT
            }
            direction = key_map.get(key, None)
            if direction:
                self.client.connection.set_direction(direction)

    def mousebuttondown(self, pos, button, **kwargs):
        if button == 1:
            if not self.client.player:
                if self.mouse_in_game():
                    x, y = self.get_game_display_rect_mouse_pos(
                        self.get_game_display_rect(self.game_render_rect),
                        *self.getmousepos())
                    pos = Vector2(x//self.client.renderer.grid_size, y//self.client.renderer.grid_size)
                    self.client.connection.request_create_player(pos)
                    raise StopIteration

    # def get_game_display_rect(self):
    #     x = 30 + 250 + 30  # 游戏区域x
    #     rect = Rect((0, 0), (self.width - x - 30, self.height))
    #     rect.centery = self.window.rect.centery
    #     rect.centerx = x + (self.width - x) / 2
    #     return rect

    def mouse_in_game(self):
        return self.get_game_display_rect(self.game_render_rect).collidepoint(*self.getmousepos())

    # def get_in_game_mouse_pos(self):
    #     """获得游戏内鼠标坐标"""
    #     rect = self.get_game_display_rect(self.game_render_rect)
    #     x, y = self.getmousepos()
    #     return x - rect.x, y - rect.y

    def back(self):
        from .TitleScreen import TitleScreen
        self.window.setscreen(TitleScreen())
