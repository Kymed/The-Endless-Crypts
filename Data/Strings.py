import pygame
from Clock import Clock
from Timer import Timer

class StringManager(object):

    # Call Constructor:
    def __init__(self):
        self.strings = []
        self.stringposx = []
        self.stringposy = []
        self.stringActive = []
        self.stringVel = []
        self.stringTimer = []

    # Spawn a new string:
    def addText(self, string, color, font, pos, timeLength, vel, game_Clock):
        self.strings.append(font.render(string, True, color)) # create the text
        self.stringposx.append(pos[0]) # create the text's x position
        self.stringposy.append(pos[1]) # create the text's y position
        self.stringVel.append(vel) # create the text's velocity
        self.stringActive.append(True) # set the texts's activity true

        self.stringTimer.append(Timer(timeLength, game_Clock.getElapsedSeconds()))
        

    # Update string:
    def update(self, game_Clock):
        if len(self.strings) > 0: # if any texts exist
            for text in range(len(self.strings)): # run a for loop for all texts
                if self.stringTimer[text].getAlert() == True: # check if it made over as many translations as planned
                    self.stringActive[text] = False # stop the strings activity

                if self.stringActive[text] == True: # if the string is still active
                    self.stringTimer[text].update(game_Clock.getElapsedSeconds()) # update the text's timer
                    self.stringposy[text] += self.stringVel[text]

    # Draw string:
    def draw(self, canvas):
        if len(self.strings) > 0: # if any texts exist
            for text in range(len(self.strings)): # run a for loop for all texts
                if self.stringActive[text] == True: # if the text is active
                    canvas.blit(self.strings[text],(self.stringposx[text], self.stringposy[text])) # draw the text ( was gonna use tuples but they don't support item assignment )
    
    # Dispose strings:
    def dispose(self):
        self.strings = []
        self.stringposx = []
        self.stringposy = []
        self.stringActive = []
        self.stringVel = []
        self.stringTimer = []
