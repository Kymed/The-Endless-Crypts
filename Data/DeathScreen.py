import pygame
from Data.Button import Button
from Data.Clock import Clock
from Data.Timer import Timer
class DeathScreen(object):

    # Call constructor
    def __init__(self, x, y, width, height, scoreEarned, wavesSurvived):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scoreEarned = scoreEarned
        self.wavesSurvived = wavesSurvived
        self.finalScore = scoreEarned + (wavesSurvived * 100)

        self.state = 1 # text display state
        self.gameClock = Clock() # internal clock for timers
        self.stateTimer = Timer(1 + self.state, 0) # timer to adjust to next state

        self.scaleWidth = width / 1280
        # each state a new thing will be drawn

        self.isMousePressed = False
        self.mousex = self.mousey = 0

        self.gameDataReset = False # for main to check if data was reset or not

        # BUTTONS #
        buttonFont = pygame.font.SysFont("Droid sans", int(width / 17))
        self.buttonWidth = width / 10
        self.buttonHeight = height / 10
        self.mainMenuButtonX = self.width - (self.buttonWidth * 2)
        self.mainMenuButtonY = self.height - (self.buttonHeight * 2)
        self.mainMenuButton = Button(self.mainMenuButtonX, self.mainMenuButtonY, self.buttonWidth, self.buttonHeight, (255, 0, 0), (125, 0, 0), buttonFont, "Main Menu")
        self.playButton = Button(self.mainMenuButtonX - (self.buttonWidth * 2), self.mainMenuButtonY, self.buttonWidth, self.buttonHeight, (255, 0, 0), (125, 0, 0), buttonFont, "Play Again")
        # BUTTONS #

        # SCORE EARNED TEXT #
        self.textFont = pygame.font.SysFont("Aller sans", int(width / 26))
        self.scoreEarnedString = "Score Earned: %d" %(self.scoreEarned)
        self.scoreEarnedText = self.textFont.render(self.scoreEarnedString, True, (255, 255 , 255))
        self.scoreEarnedTextX = self.scoreEarnedText.get_width() / 3
        self.scoreEarnedTextY = self.scoreEarnedText.get_height()

        self.particle1 = pygame.image.load("Data/images/bloodparticles/particle1.png")
        self.particle1Width = self.particle1.get_width() * self.scaleWidth
        self.particle1Height = int(self.scoreEarnedText.get_height() * 2.5)
        self.particle1 = pygame.transform.scale(self.particle1, (self.particle1Width, self.particle1Height))
        self.particle1X = (self.scoreEarnedTextX + (self.scoreEarnedText.get_width() / 2)) - (self.particle1Width / 2)
        self.particle1Y =  (self.scoreEarnedTextY + (self.scoreEarnedText.get_height() / 2)) - (self.particle1Height / 2)
        self.particle1Rect = pygame.Rect((self.particle1X,self.particle1Y),(self.particle1Width, self.particle1Height))
        # SCORE EARNED TEXT #

        # WAVE SURVIVED TEXT #
        self.wavesSurvivedString = "Waves Survived: %d" %(self.wavesSurvived)
        self.wavesSurvivedText = self.textFont.render(self.wavesSurvivedString, True, (255, 255, 255))
        self.wavesSurvivedTextX = self.scoreEarnedTextX
        self.wavesSurvivedTextY = self.scoreEarnedTextY + (self.wavesSurvivedText.get_height() * 3)

        self.particle2 = pygame.image.load("Data/images/bloodparticles/particle2.png")
        self.particle2Width = self.particle2.get_width() * self.scaleWidth
        self.particle2Height = int(self.wavesSurvivedText.get_height() * 2.5)
        self.particle2 = pygame.transform.scale(self.particle2, (self.particle2Width, self.particle2Height))
        self.particle2X = (self.wavesSurvivedTextX + (self.wavesSurvivedText.get_width() / 2)) - (self.particle2Width / 2)
        self.particle2Y = (self.wavesSurvivedTextY + (self.wavesSurvivedText.get_height() / 2)) - (self.particle2Height / 2)
        self.particle2Rect = pygame.Rect((self.particle2X, self.particle2Y),(self.particle2Width, self.particle2Height))
        # WAVE SURVIVED TEXT #

        # FINAL SCORE TEXT #
        self.finalScoreString = "Final Score Achieved: %d" %(self.finalScore)
        self.finalScoreText = self.textFont.render(self.finalScoreString, True, (255, 255, 255))
        self.finalScoreTextX = self.scoreEarnedTextX
        self.finalScoreTextY = self.wavesSurvivedTextY + (self.finalScoreText.get_height() * 3)

        self.particle3 = pygame.image.load("Data/images/bloodparticles/particle3.png")
        self.particle3Width = self.particle3.get_width() * self.scaleWidth
        self.particle3Height = int(self.finalScoreText.get_height() * 2.5)
        self.particle3 = pygame.transform.scale(self.particle3, (self.particle3Width, self.particle3Height))
        self.particle3X = (self.finalScoreTextX + (self.finalScoreText.get_width() / 2)) - (self.particle3Width / 2)
        self.particle3Y = (self.finalScoreTextY + (self.finalScoreText.get_height() / 2)) - (self.particle3Height / 2)
        self.particle3Rect = ((self.particle3X, self.particle3Y),(self.particle3Width, self.particle3Height))
        # FINAL SCORE TEXT #

    # Get data reset
    def getDataReset(self):
        return self.gameDataReset

    # Set data reset
    def setDataReset(self, isReset):
        self.gameDataReset = isReset

    # pass events
    def passEvent(self, event):
        # Pass events
        self.mainMenuButton.passEvent(event) # pass event to main menu button
        self.playButton.passEvent(event) # pass event to play button
        def passEvent(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.isMousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.isMousePressed = False
            if event.type == pygame.MOUSEMOTION:
                self.mousex, self.mousey = event.pos

    # Get Button clicked
    def getClicked(self, button):
        if button == "mainmenu":
            return self.mainMenuButton.getClicked()
        elif button == "play":
            return self.playButton.getClicked()

    # Update
    def update(self, fps):
        self.gameClock.update(fps)
        if self.stateTimer.getAlert() == True: # if the state timer is finished
            self.state += 1 # add 1 to state
            self.stateTimer = Timer(1 + self.state, self.gameClock.getElapsedSeconds()) # reset timer
        else: # if not
            self.stateTimer.update(self.gameClock.getElapsedSeconds()) # update timer

        self.mainMenuButton.update()
        self.playButton.update()


    # Draw screen
    def draw(self, canvas):
        canvas.fill((0, 0, 0))

        if self.state > 1: canvas.blit(self.particle1, self.particle1Rect)
        if self.state > 2: canvas.blit(self.particle2, self.particle2Rect)
        if self.state > 3: canvas.blit(self.particle3, self.particle3Rect)

        if self.state > 1: canvas.blit(self.scoreEarnedText, (self.scoreEarnedTextX, self.scoreEarnedTextY)) # draw score earned text if a second passed
        if self.state > 2: canvas.blit(self.wavesSurvivedText, (self.wavesSurvivedTextX, self.wavesSurvivedTextY)) # draw waves survived text if two seconds passed
        if self.state > 3: canvas.blit(self.finalScoreText, (self.finalScoreTextX, self.finalScoreTextY)) # draw final score text if three seconds passed

        if self.state > 4: # if 4 seconds passed
            self.mainMenuButton.draw(canvas) # draw main menu button
            self.playButton.draw(canvas) # draw play button
