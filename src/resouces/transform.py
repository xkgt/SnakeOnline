from functools import lru_cache

import pygame


__all__ = [
    "replacecolor",
    "scale",
    "rotate"
]
rotate = pygame.transform.rotate


@lru_cache(maxsize=15)
def replacecolor(surface, color, repcolor):
    with pygame.PixelArray(surface.copy()) as p:
        p.replace(color, repcolor)
        return p.surface


@lru_cache(maxsize=15)
def scale(surface, w=None, h=None, maintainratio=False):
    """高级缩放"""
    if maintainratio:
        assert not (w and h)
        rect = surface.get_rect()
        if w:
            rect.h = w / rect.w * rect.h
            rect.w = w
        else:
            rect.h = h
            rect.w = h / rect.h * rect.w
        return pygame.transform.scale(surface, rect.size)
    else:
        assert w and h
        return pygame.transform.scale(surface, (w, h))
