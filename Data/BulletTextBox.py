import pygame

class BulletTextBox(object): # worst class in the whole game

    # Call constructor
    def __init__(self, screenWidth, originy, padding, font):
        self.originx = screenWidth
        self.originy = originy
        self.x = self.originx
        self.y = self.originy
        self.font = font

        self.padding = padding

        self.width = 0
        self.height = 0
        self.Rect = pygame.Rect((self.x, self.y),(self.width, self.height))

        self.texts = []
        self.textX = []
        self.textY = []

        BLACK = (0, 0, 0)
        self.normal_Text = font.render("[1] Normal bullets", True, BLACK)
        self.bouncy_Text = font.render("[2] Bouncy bullets", True, BLACK)
        self.explosive_Text = font.render("[3] explosive bullets", True, BLACK)
        self.spray_Text = font.render("[4] spray bullets", True, BLACK)
        self.flame_Text = font.render("[5] flame bullets", True, BLACK)

    # Set origin X, Y
    def setOrigin(self, x, y):
        self.originx = x
        self.originy = y

    # Update
    def update(self, bouncy_isUnlocked, explosive_isUnlocked, spray_isUnlocked, flame_isUnlocked):
        # GENERATE TEXTS #
        self.texts = []
        self.texts.append(self.normal_Text)
        if bouncy_isUnlocked == True: self.texts.append(self.bouncy_Text)
        if explosive_isUnlocked == True: self.texts.append(self.explosive_Text)
        if spray_isUnlocked == True: self.texts.append(self.spray_Text)
        if flame_isUnlocked == True: self.texts.append(self.flame_Text)
        # GENERATE TEXTS #

        # RESET PROPERTIES #
        self.x = self.originx
        self.y = self.originy
        self.textsX = []
        self.textsY = []
        self.width = 0
        self.height = 0
        # RESET PROPERTIES #

        # CREATE BOX PROPERTIES BASED OFF OF HOW MANY TEXTS CREATED #
        for text in range(len(self.texts)):
            if self.texts[text].get_width() > self.width + self.padding: # check if the current text is larger than the box's width including padding
                self.width = self.texts[text].get_width() + self.padding # adjust according
            self.height += self.texts[text].get_height() # adjust the boxes height for the new height
            self.y -= self.texts[text].get_height() # adjust the box upwards for the new text
        self.x = self.originx - self.width - (self.padding * 2) # adjust x
        self.y -= self.padding * 2
        self.width += self.padding # adjust box to padding (x)
        self.height += self.padding # adjust box to padding (y)
        self.Rect = pygame.Rect((self.x, self.y),(self.width, self.height))
        # CREATE BOX PROPERTIES BASED OFF OF HOW MANY TEXTS CREATED #

        # ADJUST TEXT COORDINATES BASED OFF OF HOW MANY TEXTS CREATED #
        self.textsX.append(self.x + self.padding) # for normal text
        self.textsY.append(self.y + self.padding) # for normal text
        for text in range(1, len(self.texts)): # run a for loop for all texts
            self.textsX.append(self.x + self.padding) # create text X in order of texts
            self.textsY.append(self.y + (text * self.texts[text].get_height()) + self.padding) # create text Y in order of texts
        # ADJUST TEXT COORDINATES BASED OFF OF HOW MANY TEXTS CREATED #

    # Draw
    def draw(self, canvas):
        if len(self.texts) > 1: # only draw the bullet text box if they have bullet types (other than normal)
            pygame.draw.rect(canvas, (192, 192, 192), self.Rect, 0) # draw background
            pygame.draw.rect(canvas, (0, 0, 0), self.Rect, 2) # draw border
            for text in range(len(self.texts)): # run a for loop for all texts
                canvas.blit(self.texts[text], (self.textsX[text], self.textsY[text]))
            
        

        
    
