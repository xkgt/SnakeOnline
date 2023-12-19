import pygame


__all__ = [
    "replacecolor",
    "scale",
    "rotate"
]
rotate = pygame.transform.rotate


def replacecolor(surface, color, repcolor):
    with pygame.PixelArray(surface.copy()) as p:
        p.replace(color, repcolor)
        return p.surface


def scale(surface, w=None, h=None, maintain_ratio=False):
    """高级缩放"""
    if maintain_ratio:
        assert not (w and h)
        rect = surface.get_rect()
        if w:
            rect.h = w / rect.w * rect.h
            rect.w = w
        else:
            rect.w = h / rect.h * rect.w
            rect.h = h
        return pygame.transform.scale(surface, rect.size)
    else:
        assert w and h
        return pygame.transform.scale(surface, (w, h))
