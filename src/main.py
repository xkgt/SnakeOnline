import pygame
from resouces import Config, ResourceManager
from Client import Client

pygame.init()

config = Config.load("config.json")
client = Client(ResourceManager(config))
try:
    client.start()
finally:
    config.save()
