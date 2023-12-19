import argparse
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

parser = argparse.ArgumentParser(description='设置启动方法')
parser.add_argument('-s', '--server', action='store_true', help='是否启动服务器')
parser.add_argument('-p', '--port', type=int, default=5566, help='服务器端口号')
parser.add_argument('-c', '--connect', help='客户端连接地址')
args = parser.parse_args()

import pygame
import logging
logging.basicConfig(level=logging.INFO)
pygame.init()

if args.server:
    from Server import Server
    server = Server(args.port)
    server.run()
else:
    from Client import Client
    from resouces import Config, ResourceManager
    config = Config.load()
    client = Client(ResourceManager(config))
    try:
        if args.connect:
            from gui.screens import TitleScreen
            ip, port = args.connect.split(":")
            port = int(port)
            client.start(lambda _: client.connect((ip, port), TitleScreen()))
        else:
            client.start()
    finally:
        config.save()
