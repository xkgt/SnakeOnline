from gui import layouts
from .GameScreen import GameScreen
from .PromptScreen import PromptScreen
from .Screen import Screen
from gui.widgets import TextLine, Button, Widget, Label


class OnlineScreen(Screen):
    def __init__(self, lastscreen):
        super().__init__()
        self.lastscreen = lastscreen
        self.inputline = None

    def publish(self):
        try:
            if self.inputline.text:
                port = int(self.inputline.text)
            else:
                port = 5566
        except ValueError:
            self.window.setscreen(PromptScreen(self, "格式错误，输入值应为0~65536范围内的数字"))
        else:
            try:
                self.client.publish(port)
            except Exception as e:
                self.window.setscreen(PromptScreen(self.lastscreen, str(e)))
            else:
                self.window.topscreen.prompt(f"端口已开放{port}", 2)
                self.window.setscreen(GameScreen())

    def connect(self):
        try:
            ip, port = self.inputline.text.split(":")
            port = int(port)
        except ValueError:
            self.window.setscreen(PromptScreen(self, "格式错误，格式为：\"地址:端口\""))
        else:
            self.client.connect((ip, port), self)

    def init(self, width, height):
        # 输入行
        if self.inputline:
            self.addwidget(self.inputline)
        else:
            self.inputline = self.addwidget(TextLine(600, 60, self.font, placeholder_text="默认开放端口5566"))
        # 按钮
        join_button = self.addwidget(Button.build(290, 60, "加入房间", self.font, self.connect))
        create_button = self.addwidget(Button.build(290, 60, "创建房间", self.font, self.publish))
        rect = layouts.horizontal_layout(join_button, create_button, interval=10)
        self.inputline.rect.centery = self.window.rect.centery - self.inputline.rect.h / 2
        self.inputline.rect.centerx = self.window.rect.centerx
        title = self.addwidget(Label(self.font, "多人模式", size=40, fgcolor=(255, 255, 255)))
        title.rect.bottom = self.inputline.rect.top - self.inputline.rect.h
        title.rect.centerx = self.inputline.rect.centerx
        layouts.vertical_layout(
            c := Widget(w=rect.w, h=rect.h),
            self.addwidget(Button.build(600, 60, "返回", self.font, self.back)),
            top=self.window.rect.centery+self.inputline.rect.h, centerx=self.window.rect.centerx, interval=20
        )
        layouts.horizontal_layout(join_button, create_button, interval=20, center=c.rect.center)

    def back(self):
        self.window.setscreen(self.lastscreen)
