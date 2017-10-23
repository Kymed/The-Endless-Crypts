from __future__ import division
from Data.SoundManager import SoundManager
import pygame

class SplashScreen(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight, image, fps):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.image = image
        self.fps = fps
        self.isFinished = False
        self.startCounter = 0
        self.finishCounter = 0
        self.dankSoundPlayed = False

        font = pygame.font.SysFont("Aller sans", 72)
        self.text = font.render("Kyle Meade Productions", True, (0, 0, 0))

        self.imageScale = self.text.get_height() / self.image.get_height()

        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.imageScale), int(self.image.get_height() * self.imageScale))) # rescale image to fit height of text

        self.textX = (self.screenWidth / 2) - (self.text.get_width() / 2) + (self.image.get_width() / 2) # adjust perfectly in center with image -> X Axis
        self.textY = (self.screenHeight / 2) - (self.text.get_height() / 2) - (self.image.get_height() / 2) # adjust in the center but slightly higher -> Y Axis

        self.imageX = self.textX + self.text.get_width()
        self.imageY = self.textY

        self.textCover = pygame.Rect((self.textX, self.textY),(self.text.get_width(), self.text.get_height()))

        self.imageVel = int(self.text.get_width() / (fps * 3))

    # Get if the state is finished
    def getFinished(self):
        return self.isFinished

    # Set if the state is finished
    def setFinished(self, isFinished):
        self.isFinished = isFinished
    # Update
    def update(self, soundManager):
        self.startCounter += 1
        if self.startCounter >= 30: # if half a second passed
            self.imageX -= self.imageVel # translate image to the left
        if self.imageX < self.textX - self.image.get_width():
            self.imageX = self.textX - self.image.get_width()
            self.finishCounter += 1
            if self.dankSoundPlayed == False:
                soundManager.playSound("intro") # play the splash screen intro sound
                self.dankSoundPlayed = True
        self.textCover.right = self.imageX # adjust rectangle to be beside image

        if self.finishCounter >= self.fps * 2: # if a two second has passed since the picture has finished revealing the text, 60 being the fps
            self.setFinished(True) # say that the state is finished

    # Draw
    def draw(self, canvas):
        canvas.blit(self.text, (self.textX, self.textY)) # draw text
        pygame.draw.rect(canvas, (255, 255, 255), self.textCover, 0) # draw text cover
        canvas.blit(self.image, (self.imageX, self.imageY)) # draw kyle image
