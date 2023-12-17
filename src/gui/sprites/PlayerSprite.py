from pygame import Vector2, Surface
from resouces import transform
from game.entities import Player, Body
from .EntitySprite import EntitySprite
from .Moveable import Moveable


class PlayerSprite(EntitySprite[Player], Moveable):
    def __init__(self, renderer, entity: Player):
        super().__init__(renderer, entity)
        Moveable.__init__(self, self.entity.pos, self.renderer.game)
        self.alpha = 255
        self.angle = entity.angle
        self.alpha_add = False

    def tick(self, fps):
        self.angle = self.entity.angle
        if self.entity.invincible_time:  # 无敌时间，身体透明话
            if self.alpha_add:
                self.angle += 128 / fps * 1.7
            else:
                self.angle -= 128 / fps * 1.7
            if self.angle < 127 or self.angle > 255:
                self.alpha_add = not self.alpha_add
        # 运动
        # self.approach(fps, self.entity.pos, self.entity.motion)
        self.entity.body.update_chain(self.displaypos, self.entity.motion)

    def render(self, surface: Surface):
        if self.entity.body:
            self.render_body(surface, self.entity.body)
        img = self.handle_img(self.resourcemanager.hand, self.entity.radius)
        # 角度
        img = transform.rotate(img, -self.angle-90)
        self.render_img(surface, img, self.entity.pos, self.entity.radius)

    def render_body(self, surface: Surface, body: Body):
        if body.body:
            self.render_body(surface, body.body)
        img = self.handle_img(self.resourcemanager.snake, body.radius)
        self.render_img(surface, img, body.pos, body.radius)

    def render_img(self, surface: Surface, img: Surface, pos: Vector2, radius: int):
        """绘制贪吃蛇的图片"""
        pos = pos.copy()
        # 中心左上角
        pos.x -= radius
        pos.y -= radius
        surface.blit(img, pos)

    def handle_img(self, img: Surface, radius: int) -> Surface:
        """处理贪吃蛇的图片"""
        # 大小
        img = transform.scale(img, radius * 2, radius * 2)
        # 颜色
        if self.entity.death:  # 死了(红色)
            # 有缓存，所以不会卡顿
            img = transform.replacecolor(img, (0, 0, 0), (255, 0, 0))
        else:  # 正常颜色，包含透明
            img = transform.replacecolor(img, (0, 0, 0), self.entity.playerinfo.color)
            img.set_alpha(self.alpha)
        return img

        # self.color = entity.color  # 死后会变红
        # super().__init__(renderer, entity)
        # self.angle = entity.angle  # 显示的角度
        # self.time = 0  # 死亡时间
        # self.death = False
        # self.surface = self.resourcemanager.hand
        # super().tick(fps)
        # if self.entity.death:
        #     if not self.death:  # 获得红色图头
        #         self.color = (255, 0, 0)
        #     if self.entity.death_time > 6:  # 慢慢删除尾巴
        #         if fps / self.entity.length // 2 > 0:
        #             if self.time % (fps / self.entity.length // 2) == 0:
        #                 tail = self.entity
        #                 while tail.tail and tail.tail in self.renderer.entityspritemap and self.renderer.entityspritemap[tail.tail] in self.renderer.sprites:
        #                     tail = tail.tail
        #                 self.renderer.sprites.remove(self.renderer.entityspritemap[tail])
        #             self.time += 1
        # else:
        #     v = Vector2(self.entity.speed * 6 / fps, 0).rotate(self.entity.angle)
        #     v += self.entity.motion
        #     v = Vector2(self.entity.speed * 6 / fps, 0).rotate(v.as_polar()[1])
        #     self.displaypos[0] += v.x
        #     self.displaypos[1] += v.y

            # a = v.as_polar()[1] - self.angle
            # if a > 180:
            #     a = -a + 180
            # elif a < -180:
            #     a = -a - 180
            # print(a)
            # self.angle += a * self.client.tps / self.client.framerate
            #
            # if self.angle > 180:
            #     self.angle -= 180
            # elif self.angle <= -180:
            #     self.angle += 180

            # print(self.angle, v.as_polar()[1], a)
            # if abs(a) > 180:
            #     a = -a
            # self.angle += a * self.client.tps / self.client.framerate

            # self.angle += (v.as_polar()[1] - self.angle) * 6 / fps

    # def approach(self, fps, pos, motion: Vector2 = None):
    #     super().approach(fps, pos)

    # def handleimage(self):
    #     return pygame.transform.rotate(super().handleimage(), -self.angle-90)

    # def getimage(self):
    #     with pygame.PixelArray(self.resourcemanager.hand.copy()) as p:
    #         p.replace((0, 0, 0), self.color)
    #         s = p.surface
    #     s = pygame.transform.scale(s, (self.radius * 2, self.radius * 2))
    #     return s

    # def render(self, surface):
    #     s = self.scale(self.convert_color(self.resourcemanager.hand, (0, 0, 0), self.color),
    #                    self.radius * 2, self.radius * 2)
    #     s = pygame.transform.rotate(s, -self.angle-90)
    #     s.set_alpha(self.alpha + 128)
    #     rect = s.get_rect(center=self.displaypos)
    #     rect2 = rect.copy()
    #     surface.blit(s, rect)
    #     rect.centerx -= self.client.size[0]
    #     surface.blit(s, rect)
    #     rect.centerx += self.client.size[0] * 2
    #     surface.blit(s, rect)
    #     rect2.centery -= self.client.size[1]
    #     surface.blit(s, rect2)
    #     rect2.centery += self.client.size[1] * 2
    #     surface.blit(s, rect2)
