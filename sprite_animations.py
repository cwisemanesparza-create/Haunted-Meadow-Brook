class Animation:

    def __init__(self, frames, speed=0.1):
        self.frames = frames
        self.speed = speed
        self.index = 0

    def update(self):

        self.index += self.speed

        if self.index >= len(self.frames):
            self.index = 0

    def get_frame(self):
        return self.frames[int(self.index)]