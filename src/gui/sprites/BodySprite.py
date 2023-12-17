from typing import Generic, TypeVar
from resouces import transform

from game.entities import Body
from .EntitySprite import EntitySprite
from .Moveable import Moveable

_T = TypeVar("_T", bound=Body)


class BodySprite(EntitySprite[Body], Moveable, Generic[_T]):
    def __init__(self, renderer, entity: Body):
        super().__init__(renderer, entity)
        Moveable.__init__(self, entity.pos, self.renderer.level)
        self.color = entity.color
        self.alpha = 127  # 透明度
        self.alpha_add = True
        self.radius = entity.radius + 2
        self.surface = self.resourcemanager.snake

    def tick(self, fps):
        if self.entity.hand.death:  # 如果实体已死
            self.approach(fps, self.entity.pos)  # 只靠近坐标，不加速
        else:
            self.approach(fps, self.entity.pos, self.entity.motion)

        # 如果实体处于无敌状态
        if self.entity.hand.invincible_time:
            if self.alpha_add:
                self.alpha += 128 / fps * 1.7
            else:
                self.alpha -= 128 / fps * 1.7
            if self.alpha > 255 or self.alpha < 127:
                self.alpha_add = not self.alpha_add
        else:
            self.alpha = 255

    def render(self, surface):
        # 改颜色
        s = self.handleimage()
        rect = s.get_rect(center=self.displaypos)
        rect2 = rect.copy()
        surface.blit(s, rect)
        # 在四周也画球
        rect.centerx -= self.renderer.screen.get_width()
        surface.blit(s, rect)
        rect.centerx += self.renderer.screen.get_width() * 2
        surface.blit(s, rect)
        rect2.centery -= self.renderer.screen.get_height()
        surface.blit(s, rect2)
        rect2.centery += self.renderer.screen.get_height() * 2
        surface.blit(s, rect2)

    def handleimage(self):
        surface = transform.scale(self.surface, self.radius * 2, self.radius * 2)
        surface = transform.replacecolor(surface, (0, 0, 0), self.color)
        surface.set_alpha(self.alpha)
        return surface

    # def getimage(self):
    #     with pygame.PixelArray(self.resourcemanager.snake.copy()) as p:
    #         p.replace((0, 0, 0), self.color)
    #         s = p.surface
    #     s = pygame.transform.scale(s, (self.radius * 2, self.radius * 2))
    #     return s


del Body
