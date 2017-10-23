from __future__ import division
from MenuHUDPanel import MenuHUDPanel
import pygame

class MenuHUD(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight, gradient, icon_traits, icon_bullet, icon_star, icon_bullets):
        # INITIALIZE SCALING PROPERTIES #
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.hudScale = 0.45
        self.hudWidth = self.screenWidth * self.hudScale
        self.hudHeight = self.screenHeight * self.hudScale

        self.hudX = (self.screenWidth - self.hudWidth) / 2
        self.hudY = (self.screenHeight - self.hudHeight) / 2

        self.hudRect = pygame.Rect((self.hudX, self.hudY),(self.hudWidth, self.hudHeight))
        # INITALIZE SCALING PROPERTIES #

        # INITALIZE FONTS #
        self.font = "Open Sans Semibold"
        self.fontSize14 = pygame.font.SysFont(self.font, 14)
        # INITALIZE FONTS #

        # INITALIZE COLORS #
        self.colorWhite = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (192, 192, 192)
        self.darkGray = (160, 160, 160)

        self.backgroundColor = self.gray
        # INITALIZE COLORS #

        # LOAD ICONS #
        self.icon_trait_health = pygame.image.load("Data/images/icons/healthtrait.png") # load health traits image
        self.icon_trait_agility = pygame.image.load("Data/images/icons/agilitytrait.png") # load agility traits image
        self.icon_trait_accuracy = pygame.image.load("Data/images/icons/accuracytrait.png") # load accuracy traits image
        self.icon_trait_maxammo = pygame.image.load("Data/images/icons/normalmag.png") # load max ammo traits image

        self.icon_bulletType_bouncymag = pygame.image.load("Data/images/icons/bouncymag.png") # load bouncy magazine image
        self.icon_bulletType_explosivemag = pygame.image.load("Data/images/icons/explosivemag.png") # load explosive magazine image
        self.icon_bulletType_spraymag = pygame.image.load("Data/images/icons/spraymag.png") # load spray magazine image
        self.icon_bulletType_flamemag = pygame.image.load("Data/images/icons/flamemag.png") # load flame magazine image

        self.icon_item_distractionorb = pygame.image.load("Data/images/icons/distractionorb.png") # load accuracy orb image
        self.icon_item_grenade = pygame.image.load("Data/images/icons/grenade.png") # load grenade image
        self.icon_item_blade = pygame.image.load("Data/images/icons/blade.png") # load blade image
        self.icon_item_icicles = pygame.image.load("Data/images/icons/icicles.png") # load icicles image

        self.icon_ammo_mag1 = pygame.image.load("Data/images/icons/mag1.png") # load 1 magazine image
        self.icon_ammo_mag2 = pygame.image.load("Data/images/icons/mag2.png") # load 2 magazine image
        self.icon_ammo_mag4 = pygame.image.load("Data/images/icons/mag4.png") # load 4 magazine image
        self.icon_ammo_mag8 = pygame.image.load("Data/images/icons/mag8.png") # load 8 magazine image
        # LOAD ICONS #

        # SCORE HEADER #
        self.scoreTextFont = pygame.font.SysFont("Aller sans", 26)
        self.scoreString = "Score: "
        self.scoreText = self.scoreTextFont.render(self.scoreString, True, self.black)

        self.scoreTextBox = pygame.Rect((self.hudX, self.hudY - (self.scoreText.get_height() / 4) - self.scoreText.get_height() - 5),(self.hudWidth, self.scoreText.get_height() + 10))

        self.scoreTextX = self.scoreTextBox.center[0] - (self.scoreText.get_width () / 2)
        self.scoreTextY = self.scoreTextBox.center[1] - (self.scoreText.get_height() / 2)
        # SCORE HEADER #

        # BOTTOM PANEL #
        self.bottomPanelWidth = self.hudWidth
        self.bottomPanelHeight = self.hudHeight * 0.09
        self.bottomPanelX = self.hudX
        self.bottomPanelY = (self.hudY + self.hudHeight) - self.bottomPanelHeight

        self.bottomPanel = pygame.Rect((self.bottomPanelX, self.bottomPanelY),(self.bottomPanelWidth, self.bottomPanelHeight)) # bottom panel rect
        # BOTTOM PANEL #

        # LEFT PANEL #
        self.leftPanelWidth = self.hudWidth * 0.25
        self.leftPanelHeight = self.hudHeight - self.bottomPanelHeight

        self.leftPanel = pygame.Rect((self.hudX, self.hudY),(self.leftPanelWidth, self.leftPanelHeight)) #left panel rect
        # LEFT PANEL #

        # MAIN PANEL QUARTER #
        self.mainPanelWidth = int((self.hudWidth - self.leftPanelWidth) / 2)
        self.mainPanelHeight = int((self.hudHeight - self.bottomPanelHeight) / 2)

        mainPanelTitleFont = pygame.font.SysFont("PT Sans", 25)
        mainPanelButtonFont = pygame.font.SysFont("Droid Sans", 18)
        mainPanelMaxedFont = pygame.font.SysFont("IM Fell Great Primer", 32)
        mainPanelCostFont = pygame.font.SysFont("IM Fell Great Primer", 22)
        # MAIN PANEL QUARTER #

        # MAIN PANEL 1 #
        self.mainPanel_1x = self.hudX + self.leftPanelWidth
        self.mainPanel_1y = self.hudY

        self.mainPanel_1 = pygame.Rect((self.mainPanel_1x, self.mainPanel_1y),(self.mainPanelWidth, self.mainPanelHeight))
        self.mainPanel_1_Data = [] # 0 = Traits, 1 = bullet types,  2 = items, 3 = ammo
        self.mainPanel_1_Data.append(MenuHUDPanel(self.mainPanel_1x, self.mainPanel_1y, self.mainPanelWidth, self.mainPanelHeight, self.icon_trait_health, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Max Health", 650, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_1_Data.append(MenuHUDPanel(self.mainPanel_1x, self.mainPanel_1y, self.mainPanelWidth, self.mainPanelHeight, self.icon_bulletType_bouncymag, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Bouncy", 3000, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_1_Data.append(MenuHUDPanel(self.mainPanel_1x, self.mainPanel_1y, self.mainPanelWidth, self.mainPanelHeight, self.icon_item_distractionorb, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Distraction Orb", 550, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_1_Data.append(MenuHUDPanel(self.mainPanel_1x, self.mainPanel_1y, self.mainPanelWidth, self.mainPanelHeight, self.icon_ammo_mag1, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "1 Mag", 300, self.black, self.black, self.backgroundColor, self.darkGray))
        # MAIN PANEL 1 #

        # MAIN PANEL 2 #
        self.mainPanel_2x = self.mainPanel_1x
        self.mainPanel_2y = self.mainPanel_1y + self.mainPanelHeight

        self.mainPanel_2 = pygame.Rect((self.mainPanel_2x, self.mainPanel_2y),(self.mainPanelWidth, self.mainPanelHeight))
        self.mainPanel_2_Data = [] # 0 = Traits, 1 = bullet types,  2 = items, 3 = ammo
        self.mainPanel_2_Data.append(MenuHUDPanel(self.mainPanel_2x, self.mainPanel_2y, self.mainPanelWidth, self.mainPanelHeight, self.icon_trait_agility, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Agility", 750, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_2_Data.append(MenuHUDPanel(self.mainPanel_2x, self.mainPanel_2y, self.mainPanelWidth, self.mainPanelHeight, self.icon_bulletType_explosivemag, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Explosive", 4500, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_2_Data.append(MenuHUDPanel(self.mainPanel_2x, self.mainPanel_2y, self.mainPanelWidth, self.mainPanelHeight, self.icon_item_grenade, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Grenade",  450, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_2_Data.append(MenuHUDPanel(self.mainPanel_2x, self.mainPanel_2y, self.mainPanelWidth, self.mainPanelHeight, self.icon_ammo_mag4, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "4 Mags", 1000, self.black, self.black, self.backgroundColor, self.darkGray))
        # MAIN PANEL 2 #

        # MAIN PANEL 3 #
        self.mainPanel_3x = self.mainPanel_1x + self.mainPanelWidth
        self.mainPanel_3y = self.mainPanel_1y

        self.mainPanel_3 = pygame.Rect((self.mainPanel_3x, self.mainPanel_3y),(self.mainPanelWidth, self.mainPanelHeight))
        self.mainPanel_3_Data = [] # 0 = Traits, 1 = bullet types,  2 = items, 3 = ammo
        self.mainPanel_3_Data.append(MenuHUDPanel(self.mainPanel_3x, self.mainPanel_3y, self.mainPanelWidth, self.mainPanelHeight, self.icon_trait_accuracy, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Accuracy", 650, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_3_Data.append(MenuHUDPanel(self.mainPanel_3x, self.mainPanel_3y, self.mainPanelWidth, self.mainPanelHeight, self.icon_bulletType_spraymag, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Spray", 4000, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_3_Data.append(MenuHUDPanel(self.mainPanel_3x, self.mainPanel_3y, self.mainPanelWidth, self.mainPanelHeight, self.icon_item_blade, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Blade", 350, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_3_Data.append(MenuHUDPanel(self.mainPanel_3x, self.mainPanel_3y, self.mainPanelWidth, self.mainPanelHeight, self.icon_ammo_mag2, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "2 Mags",  550, self.black, self.black, self.backgroundColor, self.darkGray))
        # MAIN PANEL 3 #

        # MAIN PANEL 4 #
        self.mainPanel_4x = self.mainPanel_1x + self.mainPanelWidth
        self.mainPanel_4y = self.mainPanel_1y + self.mainPanelHeight

        self.mainPanel_4 = pygame.Rect((self.mainPanel_4x, self.mainPanel_4y),(self.mainPanelWidth, self.mainPanelHeight))
        self.mainPanel_4_Data = [] # 0 = Traits, 1 = bullet types,  2 = items, 3 = ammo
        self.mainPanel_4_Data.append(MenuHUDPanel(self.mainPanel_4x, self.mainPanel_4y, self.mainPanelWidth, self.mainPanelHeight, self.icon_trait_maxammo, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Max Ammo", 700, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_4_Data.append(MenuHUDPanel(self.mainPanel_4x, self.mainPanel_4y, self.mainPanelWidth, self.mainPanelHeight, self.icon_bulletType_flamemag, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Flame", 3500, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_4_Data.append(MenuHUDPanel(self.mainPanel_4x, self.mainPanel_4y, self.mainPanelWidth, self.mainPanelHeight, self.icon_item_icicles, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "Freeze Block", 250, self.black, self.black, self.backgroundColor, self.darkGray))
        self.mainPanel_4_Data.append(MenuHUDPanel(self.mainPanel_4x, self.mainPanel_4y, self.mainPanelWidth, self.mainPanelHeight, self.icon_ammo_mag8, mainPanelTitleFont, mainPanelButtonFont, mainPanelMaxedFont, mainPanelCostFont, "8 Mags", 1750, self.black, self.black, self.backgroundColor, self.darkGray))
        # MAIN PANEL 4 #

        # EXIT BUTTON #
        self.exitButtonWidth = int(self.bottomPanelWidth / 6)
        self.exitButtonHeight = int(self.bottomPanelHeight * 0.75)
        self.exitButtonX = int(self.bottomPanelX + (self.bottomPanelWidth / 2) - (self.exitButtonWidth / 2))
        self.exitButtonY = int(self.bottomPanelY + (self.bottomPanelHeight / 2) - (self.exitButtonHeight / 2))

        self.exitButton = pygame.Rect((self.exitButtonX, self.exitButtonY),(self.exitButtonWidth, self.exitButtonHeight))
        self.exitButton_BC = self.backgroundColor # background color

        self.exitButtonText = self.fontSize14.render("Exit", True, self.black)
        # EXIT BUTTON #

        # LEFT PANEL BUTTON #
        self.leftButtonWidth = self.leftPanelWidth * 0.60
        self.leftButtonHeight = int((self.leftPanelHeight / 4) * 0.80)
        # LEFT PANEL BUTTON #

        # LEFT PANEL BUTTON 1 #
        self.leftButton_1x = self.hudX + ((self.leftPanelWidth * 0.40) / 2)
        self.leftButton_1y = int(self.hudY + ((self.leftPanelHeight - (self.leftButtonHeight * 4)) / 8))

        self.leftButton_1 = pygame.Rect((self.leftButton_1x, self.leftButton_1y),(self.leftButtonWidth, self.leftButtonHeight))
        self.leftButton_1_BC = self.backgroundColor # background color

        self.icon_traits = pygame.transform.scale(icon_traits, (int(self.leftButtonWidth * 0.30), int(self.leftButtonHeight * 0.40))) # load icon image, scale rect to hud
        # LEFT PANEL BUTTON 1 #

        # LEFT PANEL BUTTON 2 #
        self.leftButton_2x = self.leftButton_1x
        self.leftButton_2y = int(self.leftButton_1y + self.leftButtonHeight + (((self.leftPanelHeight - (self.leftButtonHeight * 4)) / 4)))

        self.leftButton_2 = pygame.Rect((self.leftButton_2x, self.leftButton_2y),(self.leftButtonWidth, self.leftButtonHeight))
        self.leftButton_2_BC = self.backgroundColor # background color
        self.icon_bullet = pygame.transform.scale(icon_bullet, (int(self.leftButtonWidth * 0.30), int(self.leftButtonHeight * 0.40))) # load icon image, scale rect to hud
        # LEFT PANEL BUTTON 2 #

        # LEFT PANEL BUTTON 3 #
        self.leftButton_3x = self.leftButton_1x
        self.leftButton_3y = int(self.leftButton_2y + self.leftButtonHeight + (((self.leftPanelHeight - (self.leftButtonHeight * 4)) / 4)))

        self.leftButton_3 = pygame.Rect((self.leftButton_3x, self.leftButton_3y),(self.leftButtonWidth, self.leftButtonHeight))
        self.leftButton_3_BC = self.backgroundColor # background color
        self.icon_star = pygame.transform.scale(icon_star, (int(self.leftButtonWidth * 0.30), int(self.leftButtonHeight * 0.40))) # load icon image, scale rect to hud
        # LEFT PANEL BUTTON 3 #

        # LEFT PANEL BUTTON 4 #
        self.leftButton_4x = self.leftButton_1x
        self.leftButton_4y = int(self.leftButton_3y + self.leftButtonHeight + (((self.leftPanelHeight - (self.leftButtonHeight * 4)) / 4)))

        self.leftButton_4 = pygame.Rect((self.leftButton_4x, self.leftButton_4y),(self.leftButtonWidth, self.leftButtonHeight))
        self.leftButton_4_BC = self.backgroundColor # background color
        self.icon_bullets = pygame.transform.scale(icon_bullets, (int(self.leftButtonWidth * 0.30), int(self.leftButtonHeight * 0.40))) # load icon image, scale rect to hud
        # LEFT PANEL BUTTON 4 #

        # LOAD HUD IMAGES #
        self.gradient = pygame.transform.scale(gradient, (self.screenWidth, self.screenHeight)) # load gradient and adjust to res
        # LOAD HUD IMAGES #

        # HUD DATA #
        self.hudActive = False # if hud is active
        self.isMousePressed = False
        self.mousex = 0
        self.mousey = 0

        self.menuState = 0  # 0 = Traits, 1 = bullet types,  2 = items, 3 = buy ammo
        # HUD DATA #

    # Set Menu State
    def setMenuState(self, state):
        self.menuState = state

    # Get Menu State
    def getMenuState(self):
        return self.menuState

    # Get hud activity
    def getHudActivity(self):
        return self.hudActive

    # Set hud activity
    def setHudActivity(self, activity):
        self.hudActive = activity

    # Call when the hud is opened
    def openHud(self, canvas):
        # Tint the game screen
        canvas.blit(self.gradient, (0,0)) # draw gradient
        self.setHudActivity(True) # Set the hud active

        # Set all "Not enough" texts off
        self.mainPanel_1_Data[0].setShowNotEnough(False)
        self.mainPanel_1_Data[1].setShowNotEnough(False)
        self.mainPanel_1_Data[2].setShowNotEnough(False)
        self.mainPanel_1_Data[3].setShowNotEnough(False)
        self.mainPanel_2_Data[0].setShowNotEnough(False)
        self.mainPanel_2_Data[1].setShowNotEnough(False)
        self.mainPanel_2_Data[2].setShowNotEnough(False)
        self.mainPanel_2_Data[3].setShowNotEnough(False)
        self.mainPanel_3_Data[0].setShowNotEnough(False)
        self.mainPanel_3_Data[1].setShowNotEnough(False)
        self.mainPanel_3_Data[2].setShowNotEnough(False)
        self.mainPanel_3_Data[3].setShowNotEnough(False)
        self.mainPanel_4_Data[0].setShowNotEnough(False)
        self.mainPanel_4_Data[1].setShowNotEnough(False)
        self.mainPanel_4_Data[2].setShowNotEnough(False)
        self.mainPanel_4_Data[3].setShowNotEnough(False)

    # Event method (pass pygame.Event to HUD)
    def passEvent(self, event):
        # PASS MAIN PANEL EVENTS #
        self.mainPanel_1_Data[self.getMenuState()].passEvent(event)
        self.mainPanel_2_Data[self.getMenuState()].passEvent(event)
        self.mainPanel_3_Data[self.getMenuState()].passEvent(event)
        self.mainPanel_4_Data[self.getMenuState()].passEvent(event)
        # PASS MAIN PANEL EVENTS #

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isMousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.isMousePressed = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self.setHudActivity(False)
        if event.type == pygame.MOUSEMOTION:
            self.mousex, self.mousey = event.pos

    # Get / set / do an action within the panel
    # @param "self = instance, string = paneltype, action = event(string)"
    def actionPanel(self, string, action):
        if string == "health": # if they requested the health button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_1_Data[0].onClick() == True:
                    self.mainPanel_1_Data[0].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_1_Data[0].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_1_Data[0].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_1_Data[0].getCost()
            if action == "addcost":
                self.mainPanel_1_Data[0].addCost(30) # increase cost by 30
        elif string == "agility": # if they requested the agility button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_2_Data[0].onClick() == True:
                    self.mainPanel_2_Data[0].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_2_Data[0].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_2_Data[0].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_2_Data[0].getCost()
            if action == "addcost":
                self.mainPanel_2_Data[0].addCost(75) # increase cost by 75
        elif string == "accuracy": # if they requested the accuracy button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_3_Data[0].onClick() == True:
                    self.mainPanel_3_Data[0].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_3_Data[0].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_3_Data[0].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_3_Data[0].getCost()
            if action == "addcost":
                self.mainPanel_3_Data[0].addCost(75) # increase cost by 75
        elif string == "maxammo": # if they requested the maxammo button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_4_Data[0].onClick() == True:
                    self.mainPanel_4_Data[0].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_4_Data[0].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_4_Data[0].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_4_Data[0].getCost()
            if action == "addcost":
                self.mainPanel_4_Data[0].addCost(75) # increase cost by 75
        elif string == "bouncy": # if they requested the bouncy button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_1_Data[1].onClick() == True:
                    self.mainPanel_1_Data[1].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_1_Data[1].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_1_Data[1].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_1_Data[1].getCost()
        elif string == "explosive": # if they requested the spray button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_2_Data[1].onClick() == True:
                    self.mainPanel_2_Data[1].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_2_Data[1].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_2_Data[1].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_2_Data[1].getCost()
        elif string == "spray": # if they requested the explosive button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_3_Data[1].onClick() == True:
                    self.mainPanel_3_Data[1].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_3_Data[1].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_3_Data[1].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_3_Data[1].getCost()
        elif string == "flame": # if they requested the flame button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_4_Data[1].onClick() == True:
                    self.mainPanel_4_Data[1].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_4_Data[1].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_4_Data[1].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_4_Data[1].getCost()
        elif string == "distractionorb": # if they requested the distractionorb button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_1_Data[2].onClick() == True:
                    self.mainPanel_1_Data[2].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_1_Data[2].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_1_Data[2].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_1_Data[2].getCost()
        elif string == "blade": # if they requested the blade button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_3_Data[2].onClick() == True:
                    self.mainPanel_3_Data[2].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_3_Data[2].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_3_Data[2].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_3_Data[2].getCost()
        elif string == "grenade": # if they requested the grenade button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_2_Data[2].onClick() == True:
                    self.mainPanel_2_Data[2].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_2_Data[2].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_2_Data[2].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_2_Data[2].getCost()
        elif string == "iceblock": # if they requested the icicles button was clicked
            if action == "getbuttonclicked":
                if self.mainPanel_4_Data[2].onClick() == True:
                    self.mainPanel_4_Data[2].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_4_Data[2].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_4_Data[2].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_4_Data[2].getCost()
        elif string == "1mag":
            if action == "getbuttonclicked":
                if self.mainPanel_1_Data[3].onClick() == True:
                    self.mainPanel_1_Data[3].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_1_Data[3].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_1_Data[3].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_1_Data[3].getCost()
        elif string == "2mag":
            if action == "getbuttonclicked":
                if self.mainPanel_3_Data[3].onClick() == True:
                    self.mainPanel_3_Data[3].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_3_Data[3].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_3_Data[3].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_3_Data[3].getCost()
        elif string == "4mag":
            if action == "getbuttonclicked":
                if self.mainPanel_2_Data[3].onClick() == True:
                    self.mainPanel_2_Data[3].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_2_Data[3].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_2_Data[3].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_2_Data[3].getCost()
        elif string == "8mag":
            if action == "getbuttonclicked":
                if self.mainPanel_4_Data[3].onClick() == True:
                    self.mainPanel_4_Data[3].setClick(False) #unclick button to kill spam
                    return True
                return False
            if action == "setpanelmaxed":
                self.mainPanel_4_Data[3].setShowButton(False)
            if action == "setpanelnotenough":
                self.mainPanel_4_Data[3].setShowNotEnough(True)
            if action == "getcost":
                return self.mainPanel_4_Data[3].getCost()

    # When the menu is closed
    def onClose(self):
        self.mainPanel_1_Data[0].close()
        self.mainPanel_1_Data[1].close()
        self.mainPanel_1_Data[2].close()
        self.mainPanel_1_Data[3].close()
        self.mainPanel_2_Data[0].close()
        self.mainPanel_2_Data[1].close()
        self.mainPanel_2_Data[2].close()
        self.mainPanel_2_Data[3].close()
        self.mainPanel_3_Data[0].close()
        self.mainPanel_3_Data[1].close()
        self.mainPanel_3_Data[2].close()
        self.mainPanel_3_Data[3].close()
        self.mainPanel_4_Data[0].close()
        self.mainPanel_4_Data[1].close()
        self.mainPanel_4_Data[2].close()
        self.mainPanel_4_Data[3].close()
    # Update method
    def update(self, playerScore):

        # UPDATE SCORE HEADER #
        self.scoreString = "Score: %d" %playerScore
        self.scoreText = self.scoreTextFont.render(self.scoreString, True, self.black)

        self.scoreTextBox = pygame.Rect((self.hudX, self.hudY - (self.scoreText.get_height() / 4) - self.scoreText.get_height() - 5),(self.hudWidth, self.scoreText.get_height() + 5))

        self.scoreTextX = self.scoreTextBox.center[0] - (self.scoreText.get_width () / 2)
        self.scoreTextY = self.scoreTextBox.center[1] - (self.scoreText.get_height() / 2)
        # UPDATE SCORE HEADER #

        # BUTTON HOVER COLOR CHANGES #
        if self.exitButton.collidepoint(self.mousex, self.mousey): # if the mouse is hovering the button
            self.exitButton_BC = self.darkGray # set the button's background color to dark gray
            if self.isMousePressed == True: # if the player clicked
                self.isMousePressed = False # to allow back in once closed
                self.setHudActivity(False) # turn off hud
        else: # if not
            self.exitButton_BC = self.backgroundColor # keep it normal

        if self.leftButton_1.collidepoint(self.mousex, self.mousey): # if the mouse is hovering the button
            self.leftButton_1_BC = self.darkGray # set the button's background color to dark gray
            if self.isMousePressed == True: # if the player clicked
                self.isMousePressed = False # to allow back in once closed
                self.setMenuState(0)
        else: # if not
            self.leftButton_1_BC = self.backgroundColor # keep it normal

        if self.leftButton_2.collidepoint(self.mousex, self.mousey): # if the mouse is hovering the button
            self.leftButton_2_BC = self.darkGray # set the button's background color to dark gray
            if self.isMousePressed == True: # if the player clicked
                self.isMousePressed = False # to allow back in once closed
                self.setMenuState(1)
        else: # if not
            self.leftButton_2_BC = self.backgroundColor # keep it normal

        if self.leftButton_3.collidepoint(self.mousex, self.mousey): # if the mouse is hovering the button
            self.leftButton_3_BC = self.darkGray # set the button's background color to dark gray
            if self.isMousePressed == True: # if the player clicked
                self.isMousePressed = False # to allow back in once closed
                self.setMenuState(2)
        else: # if not
            self.leftButton_3_BC = self.backgroundColor # keep it normal

        if self.leftButton_4.collidepoint(self.mousex, self.mousey): # if the mouse is hovering the button
            self.leftButton_4_BC = self.darkGray # set the button's background color to dark gray
            if self.isMousePressed == True: # if the player clicked
                self.isMousePressed = False # to allow back in once closed
                self.setMenuState(3)
        else: # if not
            self.leftButton_4_BC = self.backgroundColor # keep it normal
        # BUTTON HOVER COLOR CHANGES #

        # UPDATE MAIN PANELS #
        self.mainPanel_1_Data[self.getMenuState()].update()
        self.mainPanel_2_Data[self.getMenuState()].update()
        self.mainPanel_3_Data[self.getMenuState()].update()
        self.mainPanel_4_Data[self.getMenuState()].update()
        # UPDATE MAIN PANELS #

    # Draw method
    def draw(self, canvas):

        # Draw HUD Header:
        pygame.draw.rect(canvas, self.backgroundColor, self.scoreTextBox, 0) # draw header backrgound
        pygame.draw.rect(canvas, self.black, self.scoreTextBox, 3) # draw header border
        canvas.blit(self.scoreText, (self.scoreTextX, self.scoreTextY)) # draw canvas text

        pygame.draw.rect(canvas, self.backgroundColor, self.hudRect, 0) # CLEAR THE HUD AREA

        # Draw HUD:
        pygame.draw.rect(canvas, self.black, self.hudRect, 4) # draw the hud border
        pygame.draw.rect(canvas, self.black, self.leftPanel, 4) # draw the left panel

        # # Bottom panel buttons:
        pygame.draw.rect(canvas, self.exitButton_BC, self.exitButton, 0) # draw exit button background
        pygame.draw.rect(canvas, self.black, self.exitButton, 2) # draw the exit button
        canvas.blit(self.exitButtonText, (self.exitButton.center[0] - (self.exitButtonText.get_width() / 2), self.exitButton.center[1] - (self.exitButtonText.get_height() / 2))) # draw exit text

        # # Left panel buttons:
        pygame.draw.rect(canvas, self.leftButton_1_BC, self.leftButton_1, 0) # draw first left button <Traits> (background)
        pygame.draw.rect(canvas, self.leftButton_2_BC, self.leftButton_2, 0) # draw second left button <bullet types> (background)
        pygame.draw.rect(canvas, self.leftButton_3_BC, self.leftButton_3, 0) # draw the third button <items> (background)
        pygame.draw.rect(canvas, self.leftButton_4_BC, self.leftButton_4, 0) # draw the fourth button <ammo> (background)

        pygame.draw.rect(canvas, self.black, self.leftButton_1, 3) # draw first left button <Traits>
        pygame.draw.rect(canvas, self.black, self.leftButton_2, 3) # draw second left button <bullet types>
        pygame.draw.rect(canvas, self.black, self.leftButton_3, 3) # draw the third button <items>
        pygame.draw.rect(canvas, self.black, self.leftButton_4, 3) # draw the fourth button <ammo>

        canvas.blit(self.icon_traits, (self.leftButton_1.center[0] - (self.icon_traits.get_width() / 2), self.leftButton_1.center[1] - (self.icon_traits.get_height() / 2))) # draw traits icon on first left button
        canvas.blit(self.icon_bullet, (self.leftButton_2.center[0] - (self.icon_bullet.get_width() / 2), self.leftButton_2.center[1] - (self.icon_bullet.get_height() / 2))) # draw bullet types icon on second left button
        canvas.blit(self.icon_star, (self.leftButton_3.center[0] - (self.icon_star.get_width() / 2), self.leftButton_3.center[1] - (self.icon_star.get_height() / 2))) # draw tstar icon on first left button
        canvas.blit(self.icon_bullets, (self.leftButton_4.center[0] - (self.icon_bullets.get_width() / 2), self.leftButton_4.center[1] - (self.icon_bullets.get_height() / 2))) # draw bullets icon on first left button <Traits>

        # # Main Panels:
        pygame.draw.rect(canvas, self.black, self.mainPanel_1, 4) # draw top left main panel
        pygame.draw.rect(canvas, self.black, self.mainPanel_2, 4) # draw bottom left main panel
        pygame.draw.rect(canvas, self.black, self.mainPanel_3, 4) # draw top right main panel
        pygame.draw.rect(canvas, self.black, self.mainPanel_4, 4) # draw the bottom right main panel

        # # Draw Main Panel Data:
        self.mainPanel_1_Data[self.getMenuState()].draw(canvas)
        self.mainPanel_2_Data[self.getMenuState()].draw(canvas)
        self.mainPanel_3_Data[self.getMenuState()].draw(canvas)
        self.mainPanel_4_Data[self.getMenuState()].draw(canvas)


        pygame.draw.rect(canvas, self.black, self.bottomPanel, 4) # Draw bottom panel
