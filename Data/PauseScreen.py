from __future__ import division
import pygame
from Data.Button import Button

class PauseScreen(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight, scaleWidth, scaleHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.scaleWidth = scaleWidth
        self.scaleHeight = scaleHeight
        self.finish = False
        self.mainmenu = False
        self.exit = False

        # CREATE PAUSE HUD #
        self.width = int(self.screenWidth * 0.25)
        self.height = int(self.screenHeight * 0.25)
        self.x = int(self.screenWidth / 2) - int(self.width / 2)
        self.y = int(self.screenHeight / 2) - int(self.height / 2)
        self.hud = pygame.Rect((self.x, self.y),(self.width, self.height))
        # CREATE PAUSE HUD #

        # CREATE PAUSE TITLE #
        titleFont = pygame.font.SysFont("Impact", 72)
        self.title = titleFont.render("Paused", True, (0, 0, 0))
        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.title = pygame.transform.scale(self.title, (int(self.title.get_width() * self.scaleWidth), int(self.title.get_height() * self.scaleHeight))) # stretch to viewport

        topHalf = pygame.Rect((self.x, self.y),(self.width, int(self.height / 2)))
        self.titleX = topHalf.center[0] - (self.title.get_width() / 2)
        self.titleY = topHalf.center[1] - (self.title.get_height() / 2)
        # CREATE PAUSE TITLE #

        # BUTTONS #
        buttonWidth = int(self.width * 0.20)
        buttonHeight = int(self.height * 0.20)
        bottomHalf = pygame.Rect((self.x, self.y + int(self.height / 2)),(self.width, int(self.height / 2)))
        buttonFont = pygame.font.SysFont("Droid Sans", 16)
        self.finishButton = Button(bottomHalf.center[0] - int(self.width / 4) - int(buttonWidth / 2), bottomHalf.center[1] - int(buttonHeight / 2), buttonWidth, buttonHeight, (0, 255, 50), (0, 200, 25), buttonFont, "Finish")

        self.mainMenuButton = Button(bottomHalf.center[0] + int(self.width / 4) - int(buttonWidth / 2), bottomHalf.center[1] - int(buttonHeight / 2), buttonWidth, buttonHeight, (0, 255, 50), (0, 200, 25), buttonFont, "Main Menu")
        
        # BUTTONS #
    # Get finished
    def getFinished(self):
        return self.finish

    # Get whether or not to go to the main menu
    def gotoMainMenu(self):
        return self.mainmenu
    
    # Pass event
    def passEvent(self, event):
        self.finishButton.passEvent(event)
        self.mainMenuButton.passEvent(event)
    # Update
    def update(self):
        self.finishButton.update()
        self.mainMenuButton.update()
        if self.finishButton.getClicked() == True:
            self.finish = True
        if self.mainMenuButton.getClicked() == True:
            self.mainmenu = True

    # Draw
    def draw(self, canvas):
        pygame.draw.rect(canvas, (0, 0, 200), self.hud, 0)
        pygame.draw.rect(canvas, (0, 0, 0), self.hud, 3)
        canvas.blit(self.title, (self.titleX, self.titleY))
        self.finishButton.draw(canvas)
        self.mainMenuButton.draw(canvas)
