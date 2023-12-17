from gui.widgets import Widget
from pygame import Rect

CENTER = 0
LEFT_TOP = 1
RIGHT_BOTTOM = 2


def get_width(*widgets: Widget, interval=0):
    w = 0
    for widget in widgets:
        w += widget.rect.w + interval
    return w - interval


def get_height(*widgets: Widget, interval=0):
    h = 0
    for widget in widgets:
        h += widget.rect.h + interval
    return h - interval


def horizontal_layout(*widgets: Widget, interval=5, align=CENTER, **kwargs):
    """横向布局"""
    rect = Rect(0, 0, get_width(*widgets, interval=interval), max(i.rect.h for i in widgets))
    for i in kwargs.items():
        setattr(rect, *i)
    x = rect.x
    for widget in widgets:
        if align == CENTER:
            widget.rect.centery = rect.centery
        elif align == LEFT_TOP:
            widget.rect.top = rect.top
        else:
            widget.rect.bottom = rect.bottom
        widget.rect.x = x
        x += widget.rect.w + interval
    return rect


def vertical_layout(*widgets: Widget, interval=5, align=CENTER, **kwargs):
    """纵向布局"""
    rect = Rect(0, 0, max(i.rect.w for i in widgets), get_height(*widgets, interval=interval))
    for i in kwargs.items():
        setattr(rect, *i)
    y = rect.y
    for widget in widgets:
        if align == CENTER:
            widget.rect.centerx = rect.centerx
        elif align == LEFT_TOP:
            widget.rect.left = rect.left
        else:
            widget.rect.right = rect.right
        widget.rect.y = y
        y += widget.rect.h + interval
    return rect


def grid_layout(*row_widgets: tuple[Widget], intervalx=5, intervaly=5, **kwargs):
    """格子布局(AI写的)"""
    row_num = len(row_widgets)  # 行数
    col_num = max(len(row) for row in row_widgets)  # 列数

    # 计算每一列的最大宽度和每一行的最大高度
    col_widths = [max(row[i].rect.w for row in row_widgets if i < len(row)) for i in range(col_num)]
    row_heights = [max(widget.rect.h for widget in row) for row in row_widgets]

    # 计算整个布局的宽度和高度
    w = sum(col_widths) + intervalx * (col_num - 1)
    h = sum(row_heights) + intervaly * (row_num - 1)
    rect = Rect(0, 0, w, h)

    # 设置布局矩形的位置和其他属性
    for i in kwargs.items():
        setattr(rect, *i)

    # 依次设置每个 widget 的位置和大小
    x = rect.x
    y = rect.y
    for i, row in enumerate(row_widgets):
        for j, widget in enumerate(row):
            # 设置 widget 的位置和大小
            widget.rect = Rect(x, y, col_widths[j], row_heights[i])
            # 更新 x 值
            x += col_widths[j] + intervalx
        # 更新 y 值
        y += row_heights[i] + intervaly
        # 重置 x 值
        x = rect.x
    return rect
