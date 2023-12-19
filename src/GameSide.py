from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from network import NetworkSystem
from game import IGame


class GameSide:
    def __init__(self):
        self.backgroundexecutor = ThreadPoolExecutor()
        self.networksystem: Optional[NetworkSystem] = None
        self.game: Optional[IGame] = None
