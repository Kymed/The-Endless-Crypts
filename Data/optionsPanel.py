import pygame
from Data.Button import Button

class OptionPanel(object):

    # Call constructor
    def __init__(self, x, y, screenWidth, width, height, scaleWidth, scaleHeight, font, font2):
        # CREATE PANEL #
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scaleWidth = scaleWidth
        self.scaleHeight = scaleHeight
        self.screenWidth = screenWidth
        self.font2 = font2
        self.arrowImage = pygame.image.load("Data/images/arrow.png")
        self.hoverarrow = pygame.image.load("Data/images/hoverarrow.png")
        self.arrowImage = pygame.transform.scale(self.arrowImage, (int(self.arrowImage.get_width() * 0.75), int(self.arrowImage.get_height() * 0.75))) # scale down the arrow
        self.hoverarrow = pygame.transform.scale(self.hoverarrow, (int(self.hoverarrow.get_width() * 0.75), int(self.hoverarrow.get_height() * 0.75))) # scale down the hover arrow
        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.arrowImage = pygame.transform.scale(self.arrowImage, (int(self.arrowImage.get_width() * self.scaleWidth), int(self.arrowImage.get_height() * self.scaleHeight)))
            self.hoverarrow = pygame.transform.scale(self.hoverarrow, (int(self.hoverarrow.get_width() * self.scaleWidth), int(self.hoverarrow.get_height() * self.scaleHeight)))

        self.isMousePressed = False
        self.mousex = self.mousey = 0
        # CREATE PANEL #

        # RESOLUTION PANEL #
        self.panelWidth = int(self.width * 0.33)
        self.panelHeight = int(self.height * 0.33)
        self.resolutionPanelRect = pygame.Rect((self.x, self.y),(self.panelWidth, self.panelHeight))

        self.resolutionText = font.render("Resolution:", True, (0,0,0))
        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.resolutionText = pygame.transform.scale(self.resolutionText, (int(self.resolutionText.get_width() * self.scaleWidth), int(self.resolutionText.get_height() * self.scaleHeight))) # scale
        self.resolutionTextX = self.x + int(self.width * 0.15) - int(self.resolutionText.get_width() / 2) # center in the middle of the 30% start X
        self.resolutionTextY = self.y + int(self.height * 0.15) - int(self.resolutionText.get_height() / 2) # center in the middle of the 30% start Y

        self.leftArrow = pygame.transform.rotate(self.arrowImage, 180) # rotate to point left
        self.leftArrowX = self.x + int(self.width * 0.33)
        self.leftArrowY = self.y + int(self.panelHeight * 0.33)
        self.leftArrowRect = pygame.Rect((self.leftArrowX, self.leftArrowY),(self.arrowImage.get_width(), self.arrowImage.get_height()))

        self.rightArrow = self.arrowImage
        self.rightArrowX = self.width - ((self.width * 0.70) * 0.20)
        self.rightArrowY = self.y + int(self.panelHeight * 0.33)
        self.rightArrowRect = pygame.Rect((self.rightArrowX, self.rightArrowY),(self.arrowImage.get_width(), self.arrowImage.get_height()))

        self.resolutions = ["800x600","1024x720", "1280x768", "1600x900", "1920x1080"]
        self.currentResNum = 2
        if self.screenWidth == 800:
            self.currentResNum = 0
        elif self.screenWidth == 1024:
            self.currentResNum = 1
        elif self.screenWidth == 1280:
            self.currentResNum = 2
        elif self.screenWidth == 1600:
            self.currentResNum = 3
        elif self.screenWidth == 1920:
            self.currentResNum = 4
        self.currentResolution = self.resolutions[self.currentResNum]

        self.currentResolutionText = self.font2.render(self.currentResolution, True, (0, 0, 0))
        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.currentResolutionText = pygame.transform.scale(self.currentResolutionText, (int(self.currentResolutionText.get_width() * self.scaleWidth), int(self.currentResolutionText.get_height() * self.scaleHeight)))
        self.currentResolutionTextX = self.leftArrowX + self.arrowImage.get_width() + int(int(self.rightArrowX - int(self.leftArrowX + self.arrowImage.get_width())) / 2) - int(self.currentResolutionText.get_width() / 2)
        self.currentResolutionTextY = self.leftArrowY + int(self.arrowImage.get_height() / 2) - int(self.currentResolutionText.get_height() / 2)
        # RESOLUTION PANEL #

        # DIFFICULTY PANEL #
        self.difficultyPanelY = self.y + self.panelHeight
        self.difficultyPanelRect = pygame.Rect((self.x, self.difficultyPanelY),(self.panelWidth, self.panelHeight))

        self.difficultyText = font.render("Difficulty:", True, (0,0,0))
        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.difficultyText = pygame.transform.scale(self.difficultyText, (int(self.difficultyText.get_width() * self.scaleWidth), int(self.difficultyText.get_height() * self.scaleHeight)))
        self.difficultyTextX = self.x + int(self.width * 0.15) - int(self.difficultyText.get_width() / 2)
        self.difficultyTextY = self.resolutionTextY + int(self.height * 0.15) - int(self.difficultyText.get_height() / 2)

        self.buttonColor = (255, 0 ,0)
        self.buttonHoverColor = (175, 0, 0)
        self.buttonWidth = self.arrowImage.get_width()
        self.buttonHeight = self.arrowImage.get_height()
        self.buttonSpacing = int((self.rightArrowX - int(self.leftArrowX + self.arrowImage.get_width())) / 3)
        self.easyButtonX = self.leftArrowX + self.buttonSpacing - self.arrowImage.get_width()
        self.mediumButtonX = self.leftArrowX + self.arrowImage.get_width() + int(int(self.rightArrowX - int(self.leftArrowX + self.arrowImage.get_width())) / 2) - int(self.buttonWidth / 2)
        self.hardButtonX = self.rightArrowX
        self.easyDifficultyButton = Button(self.easyButtonX, self.leftArrowY + self.arrowImage.get_height(), self.buttonWidth, self.buttonHeight + 1, self.buttonColor, self.buttonHoverColor, self.font2, "Easy")
        self.mediumDifficultyButton = Button(self.mediumButtonX, self.leftArrowY + self.arrowImage.get_height() + 1, self.buttonWidth, self.buttonHeight, self.buttonColor, self.buttonHoverColor, self.font2, "Medium")
        self.hardDifficultyButton = Button(self.hardButtonX, self.leftArrowY + self.arrowImage.get_height() + 1, self.buttonWidth, self.buttonHeight, self.buttonColor, self.buttonHoverColor, self.font2, "Hard")
        # DIFFICULTY PANEL #

        # SOUND PANEL #
        self.soundPanelY = self.y + (self.panelHeight * 2)
        self.soundPanelRect = pygame.Rect((self.x, self.soundPanelY),(self.panelWidth, self.panelHeight))

        self.soundText = font.render("Sound:", True, (0,0,0))
        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.soundText = pygame.transform.scale(self.soundText, (int(self.soundText.get_width() * self.scaleWidth), int(self.soundText.get_height() * self.scaleHeight)))
        self.soundTextX = self.x + int(self.width * 0.15) - (self.soundText.get_width() / 2)
        self.soundTextY = self.difficultyTextY + int(self.height * 0.15) - (self.soundText.get_height() / 2)

        self.soundOnButton = Button((self.easyButtonX + self.buttonWidth + int(self.mediumButtonX - int(self.easyButtonX + self.buttonWidth)) / 2) - int(self.buttonWidth / 2), self.soundTextY - int(self.buttonHeight / 2), self.buttonWidth, self.buttonHeight + 1, self.buttonColor, self.buttonHoverColor, self.font2, "On")
        self.soundOffButton = Button((self.mediumButtonX + self.buttonWidth + int(self.hardButtonX - int(self.mediumButtonX + self.buttonWidth)) / 2) - int(self.buttonWidth / 2), self.soundTextY - int(self.buttonHeight / 2), self.buttonWidth, self.buttonHeight + 1, self.buttonColor, self.buttonHoverColor, self.font2, "Off")
        self.oldSoundText = self.soundText
        # SOUND PANEL #

    # Count characters in a string
    def countCharacters(self, word):
        charCount = 0
        wordToCheck = word

        while (wordToCheck !=""):
            charCount+= 1
            wordToCheck = wordToCheck[1:]

        return charCount

    # Write resolution
    def writeResolution(self):
        xindex = 0
        for char in self.currentResolution:
            if char == "x":
                 break
            xindex += 1
        w = self.currentResolution[0:xindex]
        h = self.currentResolution[xindex + 1:self.countCharacters(self.currentResolution)]
        resfile = open("Data/saveddata/resolution.txt", "w") # opens resolution file to write
        resfile.write(w)
        resfile.write("\n")
        resfile.write(h)
        resfile.close()
    # Pass events
    def passEvent(self, event):
        # Update buttons
        self.easyDifficultyButton.passEvent(event)
        self.mediumDifficultyButton.passEvent(event)
        self.hardDifficultyButton.passEvent(event)
        self.soundOnButton.passEvent(event)
        self.soundOffButton.passEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isMousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.isMousePressed = False
        if event.type == pygame.MOUSEMOTION:
            self.mousex, self.mousey = event.pos

    # Get if a button was clicked or not
    def getButtonClicked(self, button):
        if button == "soundon": # if the button was sound on
            if self.soundOnButton.getClicked() == True: # if the button was clicked
                return True # return true
            return False # return false if not
        elif button == "soundoff": # if the button was sound off
            if self.soundOffButton.getClicked() == True: # if the button was clicked
                return True # return True
            return False  # return false if not
        elif button == "easy":
            if self.easyDifficultyButton.getClicked() == True: # if the easy difficulty button was clicked
                return True # return true
            return False # return false if not
        elif button == "medium":
            if self.mediumDifficultyButton.getClicked() == True: # if the medium difficulty button was clicked
                return True # return true
            return False # return false if not
        elif button == "hard":
            if self.hardDifficultyButton.getClicked() == True: # if the hard difficulty button was clicked
                return True # return true
            return False
        # Why didn't I just return get clicked instead of making it logic? Click this ad now to figure out..

    # Update
    def update(self):
        # Update resolution text
        self.currentResolutionText = self.font2.render(self.currentResolution, True, (0, 0, 0))
        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.soundText = pygame.transform.scale(self.oldSoundText, (int(self.oldSoundText.get_width() * self.scaleWidth), int(self.oldSoundText.get_height() * self.scaleHeight)))
        self.currentResolutionTextX = self.leftArrowX + self.arrowImage.get_width() + int(int(self.rightArrowX - int(self.leftArrowX + self.arrowImage.get_width())) / 2) - int(self.currentResolutionText.get_width() / 2)
        self.currentResolutionTextY = self.leftArrowY + int(self.arrowImage.get_height() / 2) - int(self.currentResolutionText.get_height() / 2)

        # Check if the player is hovering the arrow and if the player clicked
        if self.leftArrowRect.collidepoint(self.mousex, self.mousey) == True: # if the player hovered the left arrow
            self.leftArrow = pygame.transform.rotate(self.hoverarrow, 180)
            if self.isMousePressed == True: # if the player clicked yeet
                self.isMousePressed = False # turn off to reduce spam
                self.currentResNum -= 1
                if self.currentResNum < 0: self.currentResNum = 0
                self.currentResolution = self.resolutions[self.currentResNum]
                self.writeResolution()
        else: self.leftArrow = pygame.transform.rotate(self.arrowImage, 180)
        if self.rightArrowRect.collidepoint(self.mousex, self.mousey) == True: # if the player hovered the right arrow
            self.rightArrow = self.hoverarrow
            if self.isMousePressed == True: # if the player clicked yeet
                self.isMousePressed = False # turn off to reduce spam
                self.currentResNum += 1
                self.writeResolution()
                if self.currentResNum > len(self.resolutions) - 1: self.currentResNum = len(self.resolutions) - 1
                self.currentResolution = self.resolutions[self.currentResNum]
                self.writeResolution()
        else: self.rightArrow = self.arrowImage

        # Update buttons
        self.easyDifficultyButton.update()
        self.mediumDifficultyButton.update()
        self.hardDifficultyButton.update()
        self.soundOnButton.update()
        self.soundOffButton.update()

    # Draw option panel
    def draw(self, canvas):
        # Draw text
        canvas.blit(self.resolutionText, (self.resolutionTextX, self.resolutionTextY)) # draw resolution text
        canvas.blit(self.difficultyText, (self.difficultyTextX, self.difficultyTextY)) # draw difficulty text
        canvas.blit(self.soundText, (self.soundTextX, self.soundTextY)) # draw sound text

        # Draw resolution panel
        canvas.blit(self.leftArrow, (self.leftArrowX, self.leftArrowY)) # draw left resolution arrow
        canvas.blit(self.rightArrow, (self.rightArrowX, self.rightArrowY)) # draw right resolution arrow
        canvas.blit(self.currentResolutionText, (self.currentResolutionTextX, self.currentResolutionTextY)) # draw current resolution

        # Draw buttons
        self.easyDifficultyButton.draw(canvas)
        self.mediumDifficultyButton.draw(canvas)
        self.hardDifficultyButton.draw(canvas)
        self.soundOnButton.draw(canvas)
        self.soundOffButton.draw(canvas)
