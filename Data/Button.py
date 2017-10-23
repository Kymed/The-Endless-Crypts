import pygame

class Button(object):

    # Call constructor:
    def __init__(self, x, y, width, height, color, hovercolor, font, text):
        # Set dimensions and rect
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Rect = pygame.Rect((self.x, self.y), (self.width, self.height))

        # Set colors
        self.mainColor = color
        self.hoverColor = hovercolor
        self.color = self.mainColor

        # Set click stuff
        self.isMousePressed = False
        self.clickPos = (0, 0)
        self.mousex = self.mousey = 0
        self.drawHoverBorder = False
        self.isClicked = False
        self.canClick = True

        # Text stuff
        self.text = font.render(text, True, (0, 0, 0)) # create text
        while True: # create a loop to keep scaling down text if it's bigger than the buttons dimensions
            if self.text.get_width() > self.width or self.text.get_height() > self.height:
                self.text = pygame.transform.scale(self.text, (int(self.text.get_width() * 0.80), int(self.text.get_height() * 0.80))) # shorten text
            else:
                break # finish shortener loop
        self.textX = self.Rect.center[0] - (self.text.get_width() / 2)
        self.textY = self.Rect.center[1] - (self.text.get_height() / 2)

        # Create hover quads
        self.quadWidth = int(self.width * 0.20) # pygame has a division bug and I don't want to import to many futures to fix it, performance sake right
        self.quadHeight = int(self.height * 0.40) # 40%
        self.upperLeftQuad = pygame.Rect((self.Rect.topleft[0] - int(self.quadWidth / 3), self.Rect.topleft[1] - int(self.quadHeight / 3)),(self.quadWidth, self.quadHeight))
        self.upperRightQuad = pygame.Rect((self.Rect.topright[0] - int(self.quadWidth / 1.5), self.Rect.topright[1] - int(self.quadHeight / 3)),(self.quadWidth, self.quadHeight))
        self.bottomLeftQuad = pygame.Rect((self.Rect.bottomleft[0] - int(self.quadWidth / 3), self.Rect.bottomleft[1] - int(self.quadHeight / 1.5)),(self.quadWidth, self.quadHeight))
        self.bottomRightQuad = pygame.Rect((self.Rect.bottomright[0] - int(self.quadWidth / 1.5), self.Rect.bottomright[1] - int(self.quadHeight / 1.5)),(self.quadWidth, self.quadHeight))


    # Pass events
    def passEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mousex, self.mousey = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isMousePressed = True
            self.clickPos = (self.mousex, self.mousey)
        if event.type == pygame.MOUSEBUTTONUP:
            self.isMousePressed = False

    # Get clicked
    def getClicked(self):
        clicked = self.isClicked
        if clicked == True:
            self.setClicked(False) # turn off to kill spam spam
        return clicked

    # Set clicked
    def setClicked(self, clicked):
        self.isClicked = clicked

    # Update mouse button
    def update(self):
        # Check if the mouse hovers the button:
        if self.Rect.collidepoint(self.mousex, self.mousey):
            self.color = self.hoverColor
            self.drawHoverBorder = True
        else:
            self.color = self.mainColor
            self.drawHoverBorder = False

        # Check if the mouse clicked the button:
        if self.isMousePressed == True and self.Rect.collidepoint(self.clickPos) and self.canClick == True: # if the player clicked on the button
            self.setClicked(True)
            self.canClick = False

        # Check if the person unclicked
        if self.isMousePressed == False:
            self.canClick = True

    # Draw the button
    def draw(self, canvas):
        black = (0, 0, 0)
        # Draw hover borders:
        if self.drawHoverBorder == True:
            pygame.draw.rect(canvas, black, self.upperLeftQuad, 0) # draw top left quad
            pygame.draw.rect(canvas, black, self.upperRightQuad, 0) # draw top right quad
            pygame.draw.rect(canvas, black, self.bottomLeftQuad, 0) # draw bottom left quad
            pygame.draw.rect(canvas, black, self.bottomRightQuad, 0) # draw bottom right quad

        # Draw button
        pygame.draw.rect(canvas, self.color, self.Rect, 0) # draw background
        pygame.draw.rect(canvas, black, self.Rect, 2) # draw border
        canvas.blit(self.text, (self.textX, self.textY)) # draw text
