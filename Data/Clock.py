
class Clock(object):

    # Call Constructor:
    def __init__(self):
        self.secondsElapsed = 0
        self.framesElapsed = 0

    # Get elapsed seconds:
    def getElapsedSeconds(self):
        return self.secondsElapsed

    # Get elapsed frames:
    def getElapsedFrames(self):
        return self.framesElapsed

    # Update clock:
    def update(self, fps):
        self.framesElapsed += 1
        self.secondsElapsed = self.framesElapsed / fps

