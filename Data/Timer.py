
class Timer(object):

    # Call Constructor:
    def __init__(self, length, secondsElapsed):
        self.secondsAtStart = secondsElapsed
        self.seconds = 0
        self.length = length
        self.alert = False

    # Update the timer:
    def update(self, secondsElapsed):
        self.seconds = secondsElapsed - self.secondsAtStart
        if self.seconds >= self.length: # check if the timer has reached it's asked length
            self.alert = True # set alert (completion) to true

    # Get Alert method: (Alert --> If the timer has completed)
    def getAlert(self):
        return self.alert
        
