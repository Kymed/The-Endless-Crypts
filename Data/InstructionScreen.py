from __future__ import division
import pygame

class InstructionScreen(object):

    # Call constructor
    def __init__(self, x, y, width, height, scaleWidth, scaleHeight):
        # SCALE #
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scaleWidth = scaleWidth
        self.scaleHeight = scaleHeight
        # SCALE #

        # DATA #
        self.isMousePressed = False
        self.mousex = 0
        self.mousey = 0
        # DATA #

        # IMPORT PAGES #
        self.page = 0
        self.pages = []
        self.pages.append(pygame.image.load("Data/images/instructionpanels/page1.png"))
        self.pages.append(pygame.image.load("Data/images/instructionpanels/page2.png"))
        self.pages.append(pygame.image.load("Data/images/instructionpanels/page3.png"))
        self.pages.append(pygame.image.load("Data/images/instructionpanels/page4.png"))
        # IMPORT PAGES #

        # SCALE IMAGES #
        """for page in self.pages: # shorten pages
            page = pygame.transform.scale(page, (int(page.get_width() / 2),  int(page.get_height() / 2))) # shorten pages
            if self.scaleWidth != 1 or self.scaleHeight != 1:
                print "aids"
                page = pygame.transform.scale(page, (int(page.get_width() * self.scaleWidth), int(page.get_height() * self.scaleHeight)))"""
        for page in range(len(self.pages)):
            self.pages[page] = pygame.transform.scale(self.pages[page], (int(self.pages[page].get_width() / 1.8), int(self.pages[page].get_height() / 1.8))) # shorten pages
            if self.scaleWidth != 1 or self.scaleHeight != 1:
                self.pages[page] = pygame.transform.scale(self.pages[page], (int(self.pages[page].get_width() * self.scaleWidth), int(self.pages[page].get_height() * self.scaleHeight)))
        # SCALE IMAGES #

        # IMPORT & SCALE ARROWS #
        self.rightArrow = pygame.image.load("Data/images/arrow.png")
        self.leftArrow = pygame.transform.rotate(self.rightArrow, 180)
        self.rightHoverArrow = pygame.image.load("Data/images/hoverarrow.png")
        self.leftHoverArrow = pygame.transform.rotate(self.rightHoverArrow, 180)

        if self.scaleWidth != 1 or self.scaleHeight != 1: # if scale is abnormal
            self.rightArrow = pygame.transform.scale(self.rightArrow, (int(self.rightArrow.get_width() * self.scaleWidth), int(self.rightArrow.get_height() * self.scaleHeight)))
            self.leftArrow = pygame.transform.scale(self.leftArrow, (int(self.leftArrow.get_width() * self.scaleWidth), int(self.leftArrow.get_height() * self.scaleHeight)))
            self.rightHoverArrow = pygame.transform.scale(self.rightHoverArrow, (int(self.rightHoverArrow.get_width() * self.scaleWidth), int(self.rightHoverArrow.get_height() * self.scaleHeight)))
            self.leftHoverArrow = pygame.transform.scale(self.leftHoverArrow, (int(self.leftHoverArrow.get_width() * self.scaleWidth), int(self.leftHoverArrow.get_height() * self.scaleHeight)))
        # IMPORT & SCALE ARROWS #


        # ARROW DATA #
        self.rightArrowHovered = False
        self.leftArrowHovered = False

        self.pageRect = pygame.Rect((self.x, self.y),(int(self.width / 1.5), int(self.height / 1.5)))
        self.leftArrowRect = pygame.Rect((self.x, self.y + self.pages[0].get_height()),(self.leftArrow.get_width(), self.leftArrow.get_height()))
        self.rightArrowRect = pygame.Rect((self.x + self.pages[0].get_width(), self.y + self.pages[0].get_height()),(self.leftArrow.get_width(), self.leftArrow.get_height()))

        # ARROW DATA #

    # Pass events
    def passEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isMousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.isMousePressed = False
        if event.type == pygame.MOUSEMOTION:
            self.mousex, self.mousey = event.pos

    # Update
    def update(self):
        if self.leftArrowRect.collidepoint(self.mousex, self.mousey): # if the mouse is hovering the left arrow
            self.leftArrowHovered = True # set the left arrow being hovered to true
            if self.isMousePressed == True: # if the mouse was clicked
                self.isMousePressed = False # set mouse click false to kill switch spam
                self.page -= 1 # turn page left
                if self.page < 0: # if under first page
                    self.page = 0 # switch back to first page
        else: # if not
            self.leftArrowHovered = False # set the left arrow being hovered to false

        if self.rightArrowRect.collidepoint(self.mousex, self.mousey): # if the mouse is hovering the left arrow
            self.rightArrowHovered = True # set the left arrow being hovered to true
            if self.isMousePressed == True: # if the mouse was clicked
                self.isMousePressed = False # set mouse click false to kill switch spam
                self.page += 1 # turn page right
                if self.page > len(self.pages) - 1: # if over last page
                    self.page = len(self.pages) - 1 # switch back to last page
        else: # if not
            self.rightArrowHovered = False # set the left arrow being hovered to false

    # Draw
    def draw(self, canvas):
        canvas.blit(self.pages[self.page], self.pageRect) # draw current instructions page

        # Draw arrows
        if self.leftArrowHovered == True: # if the player is hovering the left arrow
            canvas.blit(self.leftHoverArrow, self.leftArrowRect) # draw left arrow (hovered version)
        else: # if not
            canvas.blit(self.leftArrow, self.leftArrowRect) # draw left arrow
        if self.rightArrowHovered == True: # if the player is hovering the right arrow
            canvas.blit(self.rightHoverArrow, self.rightArrowRect) # draw right arrow (hovered version)
        else: # if not
            canvas.blit(self.rightArrow, self.rightArrowRect) # draw right arrow
