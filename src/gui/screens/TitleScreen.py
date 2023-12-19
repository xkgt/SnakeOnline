import random
from typing import Optional

import pygame.transform
from pygame import Rect

from gui import layouts
from gui.widgets import Button, Widget, Label
from game import Direction
from .GameScreen import GameScreen
from .OnlineScreen import OnlineScreen
from .Screen import Screen


class TitleScreen(Screen):
    def __init__(self):
        super().__init__()
        self.icon = None
        self.title_rect = None
        self.icon_rect = None
        self.menu_rect: Optional[Rect] = None

        self.rotational_speed = 0  # 旋转速度
        self.direction = 0.1  # 旋转方向
        self.icon_angle = 0  # 图标角度
        self.title_color_index = 0  # 标题颜色索引
        self.game_render_rect = None

    def init(self, width, height):
        icon = self.resourcemanager.icon
        self.icon = pygame.transform.scale(icon, (icon.get_width() * 2.5, icon.get_height() * 2.5))
        icon_widget = Widget(*self.icon.get_rect())
        title_rect = self.font.get_rect("贪 吃 蛇", size=50)
        title_widget = Widget(*title_rect)  # 文字站位

        if self.client.connection and not self.client.connection.is_local() or self.client.networksystem:
            online_button = Button.build(220, 70, "断开连接", self.font, self.quit_game)
        else:
            online_button = Button.build(220, 70, "多人游戏", self.font, self.online_game)
        # 菜单
        self.menu_rect = layouts.vertical_layout(
            icon_widget,
            title_widget,
            self.addwidget(Button.build(220, 70, "开始游戏", self.font, self.single_game)),
            self.addwidget(online_button),
            self.addwidget(Button.build(220, 70, "退出", self.font, self.exit)),
            interval=40, centerx=width // 6, centery=height // 1.8
        )
        self.icon_rect = icon_widget.rect
        self.title_rect = title_widget.rect
        # 作者
        layouts.vertical_layout(
            self.addwidget(Label(self.font, "作者：KGG_Xing_Kong", size=15, fgcolor=(255, 255, 255))),
            self.addwidget(Label(self.font, "哔哩哔哩：233星空xt", size=15, fgcolor=(255, 255, 255))),
            bottom=height - 4, x=4, align=layouts.LEFT_TOP
        )
        # 获得绘画区域大小
        self.game_render_rect = Rect(0, 0, self.width - self.menu_rect.right - self.menu_rect.x * 3, self.menu_rect.h)
        self.game_render_rect.bottom = self.menu_rect.bottom
        self.game_render_rect.x = self.menu_rect.right + self.menu_rect.x

    def single_game(self):
        if not self.client.game:
            self.client.start_game()
        self.window.setscreen(GameScreen())

    def online_game(self):
        if not self.client.game:
            self.client.start_game()
        self.window.setscreen(OnlineScreen(self))

    def quit_game(self):
        self.client.disconnect()
        self.client.start_game()
        self.window.topscreen.tip("已退出游戏", 0.6)
        self.window.initscreen(self)  # 按理说当前屏幕还是自己

    def tick(self, frame):
        # 旋转图标
        self.rotational_speed += self.direction
        self.icon_angle += self.rotational_speed
        if abs(self.rotational_speed) > 20:
            self.direction = -self.direction
        # 标题颜色变换
        if frame % (self.client.framerate // 4) == 0:
            self.title_color_index += 1
            if self.title_color_index == 3:
                self.title_color_index = 0
        if self.client.connection:  # 有连接(有游戏)
            # 玩家不存在或已死
            if not self.client.player:
                self.client.connection.request_create_player(self.client.game.random_pos())
            else:
                if random.randint(0, self.client.framerate * 4) == 0:
                    self.client.connection.set_direction(Direction.random_direction())
        super().tick(frame)

    def render(self, surface, mousex: int, mousey: int):
        super().render(surface, mousex, mousey)
        # 绘制图标
        icon = pygame.transform.rotate(self.icon, self.icon_angle)
        surface.blit(icon, icon.get_rect(center=self.icon_rect.center))
        # 绘制标题
        text_color = [
            (self.title_color_index == 0) * 255,
            (self.title_color_index == 1) * 255,
            (self.title_color_index == 2) * 255
        ]
        text_topright = self.font.render_to(surface, self.title_rect.topleft, "贪 ", text_color, size=50).topright
        text_color.append(text_color.pop(0))
        text_topright = self.font.render_to(surface, text_topright, "吃", text_color, size=50).topright
        text_color.append(text_color.pop(0))
        self.font.render_to(surface, text_topright, " 蛇", text_color, size=50)
        # 左下角绘制音量
        if self.resourcemanager.config.playsound:
            volume_image = self.resourcemanager.mute
        else:
            volume_image = self.resourcemanager.volume
        volume_rect = volume_image.get_rect()
        volume_rect.centery = self.height - volume_rect.h // 2 - 15
        volume_rect.left = self.width - self.resourcemanager.volume.get_size()[0] - 15
        surface.blit(volume_image, volume_rect)
        # 绘制游戏
        if self.client.renderer:
            # 缩放游戏屏幕
            self.render_game(surface, mousex, mousey, self.game_render_rect, False)

    def exit(self):
        self.client.stop()
