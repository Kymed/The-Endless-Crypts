from __future__ import division
import pygame, random
from Data.InstructionScreen import InstructionScreen
from Data.HighscoreScreen import HighscoreScreen
from Data.optionsPanel import OptionPanel
from Data.Button import Button
from Data.Clock import Clock
from Data.Timer import Timer

class Mainmenu(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.scaleWidth = screenWidth / 1280
        self.scaleHeight = screenHeight / 768

        self.backgroundColor = (255, 255, 255)

        self.isMousePressed = False
        self.mousex = self.mousey = 0

        self.state = "growing" # growing = side and highscore panels are extending | finished = show everything at maximum size
        self.mainState = "home"# home,instruction,highscore,option

        self.background = pygame.image.load("Data/images/background.jpg").convert() # load background image
        self.background = pygame.transform.scale(self.background, (self.screenWidth, self.screenHeight)) # scale the background

        self.soundOn = True
        self.difficulty = "medium"

        # LOGO PANEL #
        self.logoMainColor = (175, 25, 25)
        self.logoHoverColor = (140, 20, 20)
        self.logoColor = self.logoMainColor
        self.logo = pygame.image.load("Data/images/logo.png")

        self.logoPanelWidth = self.screenWidth * 0.20
        self.logoPanelHeight = self.screenWidth * 0.20 # yes i know it says screenwidth
        self.logoPanelRect = pygame.Rect((0, 0),(self.logoPanelWidth, self.logoPanelHeight))

        #self.logo = pygame.transform.scale(self.logo, (int(self.logoPanelWidth * 0.75), int(self.logoPanelHeight * 0.75))) # scale logo to fit
        self.logo = pygame.transform.scale(self.logo, (int(self.logoPanelWidth), int(self.logoPanelHeight))) # scale logo to fit
        # LOGO PANEL #

        # SIDE PANEL #
        self.sidePanelColor = (200, 0, 0)
        self.sidePanelWidth = self.logoPanelWidth * 0.80
        self.sidePanelMaxHeight = self.screenHeight - self.logoPanelHeight
        self.sidePanelHeight = 0

        self.sidePanelX = 0
        self.sidePanelY = self.logoPanelHeight

        self.sidePanelRect = pygame.Rect((self.sidePanelX, self.sidePanelY),(self.sidePanelWidth, self.sidePanelHeight))
        # SIDE PANEL #

        # HIGH SCORE TEXT PANEL #
        self.highScoreTextPanelWidth = self.screenWidth - self.logoPanelWidth
        self.highScoreTextPanelHeight = self.logoPanelHeight * 0.15

        self.highScoreTextPanelX = self.logoPanelWidth
        self.highScoreTextPanelY = 0
        self.highScoreTextPanelRect = pygame.Rect((self.highScoreTextPanelX, self.highScoreTextPanelY),(self.highScoreTextPanelWidth, self.highScoreTextPanelHeight))
        # HIGH SCORE TEXT PANEL #

        # HIGH SCORE PANEL #
        self.highScorePanelColor = (150, 12, 12)
        self.highScorePanelWidth = 0
        self.highScorePanelMaxWidth = self.screenWidth - self.logoPanelWidth
        self.highScorePanelHeight = self.logoPanelHeight * (0.60 - 0.15) # 60% minus the difference in the text panel

        self.highScorePanelX = self.logoPanelWidth
        self.highScorePanelY = self.highScoreTextPanelHeight
        self.highScorePanelRect = pygame.Rect((self.highScorePanelX, self.highScorePanelY),(self.highScorePanelWidth, self.highScorePanelHeight))
        # HIGH SCORE PANEL #

        # KYMED GAMES LOGO PANEL #
        self.kymedGamesLogo = pygame.image.load("Data/images/kymedgames.png")
        self.kymedGamesLogo = pygame.transform.scale(self.kymedGamesLogo, (int(self.screenWidth * 0.15), int(self.screenHeight * 0.075)))

        self.kymedGamesLogoX = self.screenWidth - self.kymedGamesLogo.get_width() - int(self.kymedGamesLogo.get_width() / 3)
        self.kymedGamesLogoY = self.screenHeight - (self.kymedGamesLogo.get_height() * 2)
        # KYMED GAMES LOGO PANEL #

        # BUTTONS #
        buttonFont = pygame.font.SysFont("Vegur", 24)

        buttonWidth = self.sidePanelWidth * 0.80
        buttonHeight = int(self.sidePanelMaxHeight / 10)
        buttonSpacing = int(self.sidePanelMaxHeight / 20)
        buttonX = self.sidePanelRect.center[0] - (buttonWidth / 2)

        buttonColor = (150, 0, 0)
        buttonHoverColor = (115, 0, 0)

        self.playButton = Button(buttonX, self.sidePanelY + buttonSpacing, buttonWidth, buttonHeight, buttonColor, buttonHoverColor, buttonFont, "Play") # Button 1
        self.instructionButton = Button(buttonX, self.sidePanelY + buttonSpacing * 2 + buttonHeight, buttonWidth, buttonHeight, buttonColor, buttonHoverColor, buttonFont, "Instructions") # button 2
        self.highScoreButton = Button(buttonX, self.sidePanelY + buttonSpacing * 3 + buttonHeight * 2, buttonWidth, buttonHeight, buttonColor, buttonHoverColor, buttonFont, "High Scores") # button 3
        self.optionButton = Button(buttonX, self.sidePanelY + buttonSpacing * 4 + buttonHeight * 3, buttonWidth, buttonHeight, buttonColor, buttonHoverColor, buttonFont, "Options") # button 4
        self.exitButton = Button(buttonX, self.sidePanelY + buttonSpacing * 5 + buttonHeight * 4, buttonWidth, buttonHeight, buttonColor, buttonHoverColor, buttonFont, "Exit") # button 5
        # BUTTONS #

        # BACKGROUND ZOMBIES #
        self.zombieImage = pygame.image.load("Data/images/zombie.png")
        self.zombieImage = pygame.transform.scale(self.zombieImage, (int(self.screenWidth / 16), int(self.screenHeight / 9.6)))
        zombieSpawnMinX = self.logoPanelWidth + int(self.zombieImage.get_width() / 2)
        zombieSpawnMinY = self.logoPanelHeight + int(self.zombieImage.get_height() / 4)
        zombieSpawnMinWidth = self.screenWidth - self.logoPanelWidth - self.zombieImage.get_width()
        zombieSpawnMinHeight = self.screenHeight - self.logoPanelHeight - int(self.zombieImage.get_height() / 4)
        self.zombieSpawnRect = pygame.Rect((zombieSpawnMinX, zombieSpawnMinY),(zombieSpawnMinWidth, zombieSpawnMinHeight))
        self.zombies = []
        self.zombiesx = []
        self.zombiesy = []

        self.spawnClock = Clock()
        self.zombieSpawnTimeMin = 1
        self.zombieSpawnTimeMax = 3
        self.spawnTimer = Timer(random.randint(self.zombieSpawnTimeMin, self.zombieSpawnTimeMax),0)

        # OPTION SCREEN #
        self.panelX = self.logoPanelWidth
        self.panelY = self.logoPanelHeight
        self.optionScreenFont = pygame.font.SysFont("Aller sans", 28)
        self.optionScreenFont2 = pygame.font.SysFont("Aller sans", 26)
        self.optionScreen = OptionPanel(self.panelX, self.panelY, self.screenWidth, self.screenWidth - self.logoPanelWidth, self.screenHeight - self.logoPanelHeight, self.scaleWidth, self.scaleHeight, self.optionScreenFont, self.optionScreenFont2)
        # OPTION SCREEN #

        # INSTRUCTION SCREEN #
        self.instructionScreen = InstructionScreen(self.panelX, self.panelY, self.screenWidth - self.logoPanelWidth, self.screenHeight - self.logoPanelHeight, self.scaleWidth, self.scaleHeight)
        # INSTRUCTION SCREEN #

        # HIGH SCORE SCREEN #
        self.highScoreScreen = HighscoreScreen(self.panelX, self.panelY, self.screenWidth - self.logoPanelWidth, self.screenHeight - self.logoPanelHeight, self.scaleWidth, self.scaleHeight, self.optionScreenFont2)
        # HIGH SCORE SCREEN #

    # Get if sound is on or not
    def isSoundOn(self):
        return self.soundOn

    # Get the difficulty chosen by the player
    def getDifficulty(self):
        return self.difficulty

    # Get the scale width
    def getScaleWidth(self):
        return self.scaleWidth

    # Get the scale height
    def getScaleHeight(self):
        return self.scaleHeight

    # Pass events
    def passEvent(self, event):
        if self.state == "finished":
            # Pass events to buttons
            self.playButton.passEvent(event)
            self.instructionButton.passEvent(event)
            self.highScoreButton.passEvent(event)
            self.optionButton.passEvent(event)
            self.exitButton.passEvent(event)

            # Pass events to state
            if self.mainState == "options": self.optionScreen.passEvent(event) # pass event to option screen
            if self.mainState == "instructions": self.instructionScreen.passEvent(event) # pass event to instruction screen

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isMousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.isMousePressed = False
        if event.type == pygame.MOUSEMOTION:
            self.mousex, self.mousey = event.pos

    # Get button clicked
    def getButtonClicked(self, button):
        if button == "play":
            return self.playButton.getClicked()
        elif button == "instructions":
            return self.instructionButton.getClicked()
        elif button == "highscore":
            return self.highScoreButton.getClicked()
        elif button == "options":
            return self.optionButton.getClicked()
        elif button == "exit":
            return self.exitButton.getClicked()

    # Update the main menu
    def update(self, fps, soundManager):
        self.spawnClock.update(fps)# Update spawn clock

        # Check if the mouse is hovering the logo
        if self.logoPanelRect.collidepoint(self.mousex, self.mousey):
            self.logoColor = self.logoHoverColor
        else:
            self.logoColor = self.logoMainColor

        # Check if the bars are finished translating
        if self.sidePanelHeight >= self.sidePanelMaxHeight and self.highScorePanelWidth >= self.highScorePanelMaxWidth:
            self.state = "finished" # finish the growing state

        # Grow the bars
        if self.state == "growing": # if the current state is "growing"
            self.sidePanelHeight += int(self.sidePanelMaxHeight / (fps * 2)) # have it grow in max length over 2 seconds
            self.highScorePanelWidth += int(self.highScorePanelMaxWidth / (fps * 2)) # have it grow in max length over 2 seconds
            self.sidePanelRect.height = self.sidePanelHeight
            self.highScorePanelRect.width = self.highScorePanelWidth
        else: # if the growing has finished
            self.sidePanelHeight = self.sidePanelMaxHeight

        # Run all necessary code if the mainmenu is finished grow
        if self.state == "finished":
            # Update buttons
            self.playButton.update()
            self.instructionButton.update()
            self.highScoreButton.update()
            self.optionButton.update()
            self.exitButton.update()

            # Spawn zombies
            if len(self.zombies) < 100 and self.mainState == "home":
                if self.spawnTimer.getAlert() == True: # if the spawn timer finished
                    rotation = random.randint(0, 360)
                    zombiex = random.randint(self.zombieSpawnRect.x, self.zombieSpawnRect.width)
                    zombiey = random.randint(self.zombieSpawnRect.y, self.zombieSpawnRect.height)
                    timerLength = random.randint(self.zombieSpawnTimeMin, self.zombieSpawnTimeMax)
                    self.zombies.append(pygame.transform.rotate(self.zombieImage, rotation)) # create a new zombie
                    self.zombiesx.append(zombiex) # create a new zombie x
                    self.zombiesy.append(zombiey) # create a new zombie y
                    self.spawnTimer = Timer(timerLength, self.spawnClock.getElapsedSeconds())
                else: # if the spawner is not finished
                    self.spawnTimer.update(self.spawnClock.getElapsedSeconds()) # update the timer clock

            # Change states
            if self.isMousePressed == True and self.logoPanelRect.collidepoint(self.mousex, self.mousey): # if the player pressed the logo panel
                self.mainState = "home" # change to home state
            if self.getButtonClicked("options") == True: # if the option button was clicked
                self.mainState = "options"
            if self.getButtonClicked("instructions") == True: # if the instructions button was clicked
                self.mainState = "instructions"
            if self.getButtonClicked("highscore") == True: # if the high score button was clicked
                self.mainState = "highscore"

            # Update STATES
            if self.mainState == "options":
                self.optionScreen.update()

                # Options panel logic
                if self.optionScreen.getButtonClicked("soundon") == True:
                    self.soundOn = True
                if self.optionScreen.getButtonClicked("soundoff") == True:
                    self.soundOn = False
                if self.optionScreen.getButtonClicked("easy") == True:
                    self.difficulty = "easy"
                if self.optionScreen.getButtonClicked("medium") == True:
                    self.difficulty = "medium"
                if self.optionScreen.getButtonClicked("hard") == True:
                    self.difficulty = "hard"

            elif self.mainState == "instructions":
                self.instructionScreen.update()

    # Draw the main menu
    def draw(self, canvas):
        canvas.blit(self.background, (0, 0)) # draw the background image

        # Draw Logo Panel:
        pygame.draw.rect(canvas, self.logoColor, self.logoPanelRect, 0) # draw the background
        pygame.draw.rect(canvas, (0, 0, 0), self.logoPanelRect, 6) # draw the border
        canvas.blit(self.logo, (self.logoPanelRect.center[0] - (self.logo.get_width() / 2), self.logoPanelRect.center[1] - (self.logo.get_height() / 2)))

        # Draw side panel:
        pygame.draw.rect(canvas, self.sidePanelColor, self.sidePanelRect, 0) # draw background
        pygame.draw.rect(canvas, (0, 0, 0), self.sidePanelRect, 2) # draw border

        # Draw highscore panel:
        pygame.draw.rect(canvas, self.highScorePanelColor, self.highScorePanelRect, 0) # draw background
        pygame.draw.rect(canvas, (0, 0, 0), self.highScorePanelRect, 2)

        # Draw finished state main menu objects
        if self.state == "finished":
            # Draw kymed games logo:
            canvas.blit(self.kymedGamesLogo, (self.kymedGamesLogoX, self.kymedGamesLogoY))

            # Draw buttons:
            self.playButton.draw(canvas)
            self.instructionButton.draw(canvas)
            self.highScoreButton.draw(canvas)
            self.optionButton.draw(canvas)
            self.exitButton.draw(canvas)

            # Draw background zombies:
            if self.mainState == "home":
                for zombie in range(len(self.zombies)): # run a for loop for all zombies
                    canvas.blit(self.zombies[zombie], (self.zombiesx[zombie], self.zombiesy[zombie])) # blit the zombie and it's location
            elif self.mainState == "options": # if it's on the option screen than draw optionScreen
                self.optionScreen.draw(canvas) # draw option screen
            elif self.mainState == "instructions": # if it's on the instruction screen than draw instruction screen
                self.instructionScreen.draw(canvas) # draw instruction screen
            elif self.mainState == "highscore": # if it's on the high score screen than high scores
                self.highScoreScreen.draw(canvas)

            # Draw Kyle Meade Games logo
            pygame.draw.rect(canvas, (200, 0, 0), (self.kymedGamesLogoX, self.kymedGamesLogoY, self.kymedGamesLogo.get_width(), self.kymedGamesLogo.get_height()), 3)
