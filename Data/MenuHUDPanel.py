import pygame

class MenuHUDPanel(object):

    # Call constructor
    def __init__(self, x, y, width, height, icon, titleFont, buttonFont, maxedFont, costFont, title, initialCost, titleColor, buttonTextColor, buttonBackgroundColor, onHoverButtonColor):
        # INITIALIZE SCALE DATA #
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # INITALIZE SCALE DATA #

        # INITALIZE DATA #
        self.isClicked = False
        self.isMousePressed = False
        self.canClick = True
        self.mousex = self.mousey = 0
        self.showButton = True
        self.cost = initialCost
        self.costFont = costFont
        
        self.defaultButtonBackgroundColor = buttonBackgroundColor
        self.onHoverButtonColor = onHoverButtonColor
        self.buttonBackgroundColor = buttonBackgroundColor
        # INITALIZE DATA #

        # GENERATE PANEL #
        # Rect:
        self.Rect = pygame.Rect((self.x, self.y),(self.width, self.height))

        # Title:
        upperRightQuad = pygame.Rect((self.x + (self.width / 2), self.y), (self.width / 2, self.height / 2))
        self.title = titleFont.render(title, True, titleColor)
        if self.title.get_width() > upperRightQuad.width: # if the text is too wide
            self.title = pygame.transform.scale(self.title, (int(self.title.get_width() * 0.75), int(self.title.get_height() * 0.75))) # shorten it
        self.titleX = upperRightQuad.center[0] - (self.title.get_width() / 2)
        self.titleY = upperRightQuad.center[1] - (self.title.get_height() / 2)

        # Button:
        lowerLeftQuad = pygame.Rect((self.x, self.y + (self.height / 2)),(self.width/2, self.height / 2))
        self.buttonWidth = int(self.width * 0.30)
        self.buttonHeight = int(self.height * 0.30)
        self.button = pygame.Rect((lowerLeftQuad.center[0] - (self.buttonWidth / 2), lowerLeftQuad.center[1] - (self.buttonHeight / 2)),(self.buttonWidth, self.buttonHeight))

        # Button Text:
        self.buttonText = buttonFont.render("Buy", True, buttonTextColor)
        self.buttonTextX = self.button.center[0] - (self.buttonText.get_width() / 2)
        self.buttonTextY = self.button.center[1] - (self.buttonText.get_height() / 2)

        # Maxed Text (If the button is off):
        lowerHalf = pygame.Rect((self.x, self.y + (self.height / 2)),(self.width, self.height / 2))
        
        self.maxedText = maxedFont.render("Maxed", True, (255, 0, 0))
        self.maxedTextX = lowerHalf.center[0] - (self.maxedText.get_width() / 2)
        self.maxedTextY = lowerHalf.center[1] - (self.maxedText.get_height() / 2)

        # Initial cost text:
        self.lowerRightQuad = pygame.Rect((self.x + (self.width / 2), self.y + (self.height / 2)),(self.width / 2, self.height / 2))
        self.costText = self.costFont.render(str(self.cost), True, (0, 0, 0))
        self.costX = self.lowerRightQuad.center[0] - (self.costText.get_width() / 2)
        self.costY = self.lowerRightQuad.center[1] - self.costText.get_height()

        # Not enough text:
        self.showNotEnough = False
        self.notEnoughText = self.costFont.render("Not enough!", True, (0, 0, 0))
        self.notEnoughTextX = self.lowerRightQuad.center[0] - (self.notEnoughText.get_width() / 2)
        self.notEnoughTextY = self.lowerRightQuad.center[1] + 1

        # Panel Icon:
        upperLeftQuad = pygame.Rect((self.x, self.y),(self.width / 2, self.height / 2))
        self.Icon = pygame.transform.scale(icon, (int(self.width / 4), int(self.height / 4)))
        self.IconX = upperLeftQuad.center[0] - (self.Icon.get_width() / 2)
        self.IconY = upperLeftQuad.center[1] - (self.Icon.get_height() / 2)
        
        # GENERATE PANEL #

    # Set button background color
    def setButtonBackgroundColor(self, color):
        self.buttonBackgroundColor = color

    # Get buttonbackground color
    def getButtonBackgroundColor(self):
        return self.buttonBackgroundColor
    
    # Set click state
    def setClick(self, activity):
        self.isClicked = activity
    
    # Get click state
    def onClick(self):
        return self.isClicked

    # On hover data
    def onHover(self):
        self.setButtonBackgroundColor(self.onHoverButtonColor)

    # Set Show Not Enough Text
    def setShowNotEnough(self, activity):
        self.showNotEnough= activity

    # Get Show Not Enough Text
    def getShowNotEnough(self):
        return self.showNotEnough

    # Set Bool if panel can Show Button
    def setShowButton(self, activity):
        self.showButton = activity

    # Set the cost of whatever is in the panel
    def setCost(self, cost):
        self.cost = cost

    # Get the cost of whatever is in the panel
    def getCost(self):
        return self.cost

    # Increase the cost by the value from what it already is
    def addCost(self, cost):
        self.cost += cost

    # Get bool if panel can show Button
    def getShowButton(self):
        return self.showButton

    # Pass events
    def passEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isMousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.isMousePressed = False
        if event.type == pygame.MOUSEMOTION:
            self.mousex, self.mousey = event.pos

    # When the menu is closed
    def close(self):
        self.isMousePressed = False
        self.canClick = True
        self.setClick(False)
        
    # Update
    def update(self):

        # Update cost text (Because it changes) #
        self.costText = self.costFont.render(str(self.cost), True, (0, 0, 0))
        self.costX = self.lowerRightQuad.center[0] - (self.costText.get_width() / 2)
        self.costY = self.lowerRightQuad.center[1] - self.costText.get_height()
        # Update cost text (Because it changes) #

        if self.button.collidepoint(self.mousex, self.mousey) == True and self.getShowButton() == True: # if the mouse is hovering the button and the button exists
            self.onHover() # do any necessary changes when mouse is hovering button
            if self.isMousePressed == True and self.canClick == True: # check if the mouse was clicked
                self.canClick = False # to kill spam
                self.setClick(True)
        else: # if it isn't hovering
            self.setButtonBackgroundColor(self.defaultButtonBackgroundColor) # set the background default
            self.isMousePressed = False # So you won't buy the trait when u click then drag into the button
        
        
        if self.isMousePressed == False: # if the mouse isn't pressed
            self.canClick = True # check that the player can click the button
            self.setClick(False) # unclick
            

    # Draw
    def draw(self, canvas):
        canvas.blit(self.title, (self.titleX, self.titleY)) # draw title
        canvas.blit(self.Icon, (self.IconX, self.IconY)) # draw icon
        pygame.draw.rect(canvas, (0, 0, 0), (self.IconX, self.IconY, self.Icon.get_width(), self.Icon.get_height()), 2) # draw icon border
        if self.getShowButton() == True:
            canvas.blit(self.costText, (self.costX, self.costY)) # draw cost
            # Draw Button:
            pygame.draw.rect(canvas, self.getButtonBackgroundColor(), self.button, 0) # draw button background
            pygame.draw.rect(canvas, (0, 0, 0), self.button, 2) # draw button border
            canvas.blit(self.buttonText, (self.buttonTextX, self.buttonTextY)) # draw button text
        else: # if button is off
            # Draw Maxed:
            canvas.blit(self.maxedText, (self.maxedTextX, self.maxedTextY)) # draw maxed text
        if self.getShowNotEnough() == True and self.getShowButton() == True: # if the player didn't have enough to purchase text in the panel and the button exists
            canvas.blit(self.notEnoughText, (self.notEnoughTextX, self.notEnoughTextY)) # draw not enough text
            
