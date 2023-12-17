from moretypes import Vector2
from game import IGame


class Moveable:
    def __init__(self, pos: Vector2, game: IGame):
        self.displaypos = pos.copy()
        self.game = game

    def approach(self, fps, pos, motion: Vector2 = None):
        """靠近坐标"""
        for i in (0, 1):
            a = pos[i] - self.displaypos[i]  # 计算差值
            if a > self.game.size[i] * 0.9:  # 如果实际坐标在地图另一端
                self.displaypos[i] += self.game.size[i]  # 直接加或者减(这样切换会更流畅)
            elif a < -self.game.size[i] * 0.9:
                self.displaypos[i] -= self.game.size[i]
            elif abs(a) > 200:  # 否则如果距离直接过远
                self.displaypos[i] = pos[i]
            else:
                if motion:  # 否则就慢慢移过去
                    self.displaypos[i] += (a + motion.xy[i]) * 6 / fps
                else:
                    self.displaypos[i] += a * 6 / fps
