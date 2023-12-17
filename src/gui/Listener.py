from functools import wraps
from types import FunctionType

import pygame.event


class Listener:
    """事件监听器"""

    def __init__(self):
        self.sub_listeners: set[Listener] = set()

    @staticmethod
    def event(func: FunctionType):
        name = func.__name__

        @wraps(func)
        def a(self: "Listener", *args, **kwargs):
            # 子类调用super函数将继续遍历子监听器
            for sub_listener in self.sub_listeners.copy():
                if hasattr(sub_listener, name):  # 比如Button可能没有Window.close的子监听器
                    getattr(sub_listener, name)(*args, **kwargs)
        return a

    def handle_event(self):
        """处理事件"""
        for event in pygame.event.get():
            name = pygame.event.event_name(event.type).lower()
            if hasattr(self, name):
                try:
                    getattr(self, name)(**event.dict)
                except StopIteration:
                    ...

    def addlistener(self, listener: "Listener"):
        self.sub_listeners.add(listener)

    def removelistener(self, listener: "Listener"):
        self.sub_listeners.remove(listener)

    # def __delattr__(self, item):
    #     """用del删除监听器"""
    #     if isinstance(item, Listener) and item in self.sub_listeners:
    #         self.sub_listeners.remove(item)
    #     super().__delattr__(item)
    #
    # def __setattr__(self, key, value):
    #     """设置监听器"""
    #     if hasattr(self, key):  # 替代之前的监听器
    #         item = getattr(self, key)
    #         if isinstance(item, Listener) and item in self.sub_listeners:
    #             self.sub_listeners.remove(item)
    #     if isinstance(value, Listener):
    #         self.sub_listeners.add(value)
    #     super().__setattr__(key, value)

    @event
    def textinput(self, text, **kwargs):
        """输入"""

    @event
    def textediting(self, text, start, length, **kwargs):
        """文本编辑"""

    @event
    def quit(self, **kwargs):
        """退出"""

    @event
    def userevent(self, code, **kwargs):
        """用户事件"""

    @event
    def mousemotion(self, pos, rel, buttons, **kwargs):
        """鼠标移动"""

    @event
    def mousebuttondown(self, pos, button, **kwargs):
        """鼠标按钮按下"""

    @event
    def mousebuttonup(self, pos, button, **kwargs):
        """鼠标按钮按松开"""

    @event
    def keydown(self, unicode, key, mod, **kwargs):
        """键盘按下"""

    @event
    def keyup(self, key, mod, **kwargs):
        """键盘松开"""

    @event
    def windowsizechanged(self, **kwargs):
        """窗口大小改变"""
