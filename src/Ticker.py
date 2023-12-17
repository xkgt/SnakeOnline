from pygame.time import Clock


class Ticker:
    def __init__(self, framerate):
        self.framerate = framerate
        self.running = True
        self.clock = Clock()

    def run(self):
        frame = 0
        try:
            while self.running:
                self.tick(frame)
                if frame == self.framerate:
                    self.second()
                frame += 1
                if frame == self.framerate:
                    frame = 0
                self.clock.tick(self.framerate)
        except KeyboardInterrupt:
            ...
        self.end()

    def tick(self, frame):
        ...

    def second(self):
        ...

    def end(self):
        ...

    def stop(self):
        self.running = False
