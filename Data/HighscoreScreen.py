import pygame

class HighscoreScreen(object):

    # Call constructor
    def __init__(self, x, y, width, height, scaleWidth, scaleHeight, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scaleWidth = scaleWidth
        self.scaleHeight = scaleHeight
        self.font = font

        # SORT SCORES IN FILE FROM HIGHEST TO LOWEST #
        import Data.scoresorter as scoreSorter
        scoreSorter.sortScores("Data/saveddata/scores.txt")
        # SORT SCORES IN FILE FROM HIGHEST TO LOWEST #

        # LOAD HIGH SCORES FROM FILE #
        self.highScores = []
        scoreFile = open("Data/saveddata/scores.txt", "r")
        lines = 0
        for line in scoreFile:
            newLine = line.rstrip("\n")
            self.highScores.append(newLine)
            lines += 1
            if lines > 15:
                break
        scoreFile.close()
        # LOAD HIGH SCORES FROM FILE #

        # CREATE TEXTS #
        self.scoreTexts = []
        self.scorePos = []
        y = self.y
        for score in self.highScores: # run a for loop for all loaded scores
            text = font.render(score, True, (255, 255, 255)) # render text
            if self.scaleWidth != 1 or self.scaleHeight != 1: # check if scale is abnormal
                text = pygame.transform.scale(text, (int(text.get_width() * self.scaleWidth), int(text.get_height() * self.scaleHeight))) # transform to scale
            self.scoreTexts.append(text) # add the new rendered text
            self.scorePos.append((self.x, y)) # create it's position
            y += text.get_height() # add y for every text made
        # CREATE TEXTS #

    # Draw
    def draw(self, canvas):
        for text in range(len(self.scoreTexts)): # run a for loop for all score texts
            canvas.blit(self.scoreTexts[text], self.scorePos[text]) # draw the text
