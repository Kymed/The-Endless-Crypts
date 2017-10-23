# Kyle Meade
# ICS3U Class Game
# Manages all the game classes and puts themtogether
import sys, pygame, math
import Data.inputbox as inputbox
from pygame.locals import *
from Data.Level import Level
from Data.Clock import Clock
from Data.Player import Player
from Data.MenuHUD import MenuHUD
from Data.Mainmenu import Mainmenu
from Data.DeathScreen import DeathScreen
from Data.PauseScreen import PauseScreen
from Data.SoundManager import SoundManager
from Data.SplashScreen import SplashScreen
from Data.BulletTextBox import BulletTextBox

# TODO #
"""
difficulties
"""
# TODO #

# DEVELOPER TOOLS #
drawBounds = False
godMode = False
spamLevelProgress = False
infiniteScore = False
unlockBulletTypes = False
unlimitedItems = False
# DEVELOPER TOOLS #

# GET WIDTH & HEIGHT #  
WIDTH = HEIGHT = 0
res = open("Data/saveddata/resolution.txt", "r") # open resolution file for read
lines = 0
for line in res:
    if lines == 0:
        WIDTH = int(line)
        lines += 1
    else:
        HEIGHT = int(line)
res.close()
# GET WIDTH & HEIGHT #

# INITALIZE PYGAME #
pygame.init()
dimensions = (WIDTH, HEIGHT)
flags = DOUBLEBUF | HWSURFACE
canvas = pygame.display.set_mode(dimensions, flags)
pygame.display.set_caption("The Endless Crypts By Kyle Meade")
clock = pygame.time.Clock()
FPS = 60
WHITE = (255,255,255) # create the white colored variable in RGB
BLACK = (0,0,0) # create the white colored variable in RGB
RED = (255,0,0) # create the red colored variable in RGB
GREEN = (0,255,0)	# create the green colored variable in RGB
BLUE = (0,0,255) # create the blue colored variable in RGB
GRAY = (193, 193, 193) # create the gray colored variable in RGB
YELLOW = (235, 235, 0) # create the yellow colored variable in RGB
canvas.fill(WHITE) # clear the screen white
pygame.display.update()
isMousePressed = False
mousex = mousey = 0
hudFont = "Cartographic"
hudFont1 = pygame.font.SysFont(hudFont,36)
hudFont2 = pygame.font.SysFont(hudFont,32)
hudFont3 = pygame.font.SysFont(hudFont,28)
hudFont4 = pygame.font.SysFont(hudFont,24)
scoreSaved = False

tileWidth = int(WIDTH / 20)
tileHeight = int(HEIGHT / 12)
oldState = 1
difficulty = "medium"
# INITALIZE PYGAME #

# LOAD IMAGES #
zombieImg = pygame.image.load("Data/images/zombie.png") # Load Zombie Image
pistolCharImg = pygame.image.load("Data/images/survivor-move_handgun_0.png") # Load Player Image
backgroundImg = pygame.image.load("Data/images/background.jpg").convert() # load background image
spawnerImg = pygame.image.load("Data/images/spawnerImg.png") # load zombie spawner image
block1Image = pygame.image.load("Data/images/block.png").convert() # load block 1 image
arrowImage = pygame.image.load("Data/images/arrow.png") # load the arrow image
gradient = pygame.image.load("Data/images/HDgradient.png") # load the gradient overcast

icon_traits = pygame.image.load("Data/images/icons/traitsarrow.png") # load traits arrow icon
icon_bullet = pygame.image.load("Data/images/icons/bullet.png") # load bullet icon
icon_star = pygame.image.load("Data/images/icons/ministar.png") # load star icon
icon_bullets = pygame.image.load("Data/images/icons/bullets.png") # load bullets icon

kymed = pygame.image.load("Data/images/kymed.png").convert() # load kymed image
# LOAD IMAGES #

# INITALIZE MENUS #
splashScreen = SplashScreen(WIDTH, HEIGHT, kymed, FPS)
mainMenu = Mainmenu(WIDTH, HEIGHT)
# INITALIZE MENUS #

# PROGRESSIVE DATA #
roomsElapsed = 0
roomsElapsed_Counter2 = 0 #keep track when to increase max zombies
maxZombies = 4
zombieHealth = 1
zombieMinVel = 1
zombieMaxVel = 4
zombieMinSpawnTime = 1
zombieMaxSpawnTime = 4
if difficulty == "easy":
    playerHealth = 14
    playerStamina = 4
if difficulty == "medium":
    playerHealth = 10
    playerStamina = 3
if difficulty == "hard":
    playerHealth = 7
    playerStamina = 2

playerMaxHealth = 25
accuracyLevel = 80
playerMaxAgility = 2.30
magAmmo = 120
maxMagazineAmmo = 240
# PROGRESSIVE DATA #

# ITEM DATA #
bulletType = "normal"
if unlockBulletTypes != True:
    bulletType_bouncy_isUnlocked = False
    bulletType_explosive_isUnlocked = False
    bulletType_spray_isUnlocked = False
    bulletType_flame_isUnlocked = False
else:
    bulletType_bouncy_isUnlocked = True
    bulletType_explosive_isUnlocked = True
    bulletType_spray_isUnlocked = True
    bulletType_flame_isUnlocked = True

if unlimitedItems == False: # if developer tools unlimited items isn't on
    distractionOrbs = 1 # give 1 of each item off the bat
    grenades = 1
    blades = 1
    iceblocks = 1
else: # if it is on
    distractionOrbs = 99999999
    grenades = 9999999999
    blades = 999999999
    iceblocks = 999999999
# ITEM DATA #

# INITALIZE OBJECTS #
_clock = Clock() # Create the timer clock
player = Player(WIDTH, HEIGHT, "Crypt Keeper", pistolCharImg, WIDTH / 2, HEIGHT / 2, playerHealth, playerStamina, FPS, drawBounds) # Start Player Object

playerSpawnX = int(WIDTH / 2)
playerSpawnY = HEIGHT - tileHeight
currentLevel = Level(WIDTH, HEIGHT, roomsElapsed + 1, accuracyLevel, magAmmo, FPS, tileWidth, tileHeight, block1Image, spawnerImg, backgroundImg, arrowImage, playerSpawnX, playerSpawnY, zombieImg, drawBounds, maxZombies, zombieHealth, zombieMinVel, zombieMaxVel, zombieMinSpawnTime, zombieMaxSpawnTime) # Initalize first level
currentLevel.spawnPlayer(player)
menu = MenuHUD(WIDTH, HEIGHT, gradient, icon_traits, icon_bullet, icon_star, icon_bullets) # initalize hud
bulletTextBox = BulletTextBox(WIDTH, HEIGHT, int(HEIGHT / 153), hudFont3)
pauseScreen = PauseScreen(WIDTH, HEIGHT, mainMenu.getScaleWidth(), mainMenu.getScaleHeight())
soundManager = SoundManager()
# INITALIZE OBJECTS #

name = None
if infiniteScore == True:
    player.addScore(99999999999)

def save(name, score):
    scoreFile = open("Data/saveddata/scores.txt", "a")
    s = "%s %d" %(name, score)
    scoreFile.write(s) # write new score
    scoreFile.close() # close file

# Pre loop variables:
mousex, mousey = (0, 0)
running = True
gameRunning = True # Tool to turn on/off game update & draw. Primarily used to end game updates when accessing the menu
STATE = 4 # SET STATE, 1 = mainmenu, 2 = game, 3 = death screen, 4 = splash screen, 5 = name select
soundManager.playSound("dankhorn")
leftPauseScreen = False
while running: # GAME LOOP:
    if STATE == 0:
        running = False
    elif STATE == 1: # MAIN MENU STATE:
        clock.tick(FPS)
        for event in pygame.event.get():
            mainMenu.passEvent(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                isMousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                isMousePressed = False
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos

        mainMenu.update(FPS, soundManager) # update main menu
        soundManager.setActive(mainMenu.isSoundOn())# update the sound manager if the player turned sound on or off
        difficulty = mainMenu.getDifficulty() # get the difficulty from main menu
        
        # Checked click buttons
        if mainMenu.getButtonClicked("play"): # if the play button was clicked
            STATE = 5 # change to name select state
        if mainMenu.getButtonClicked("exit"): # if the exit button was clicked
            STATE = 0 # exit the program
        
        canvas.fill(WHITE) # clear the screen
        mainMenu.draw(canvas) # draw the main menu
        pygame.display.update() # update the screen

    elif STATE == 2: # GAME STATE
        pause = False
        _clock.update(FPS)
        clock.tick(FPS)
        for event in pygame.event.get():
            if gameRunning == True:
                player.passEvent(event)
                currentLevel.passEvent(event, soundManager)
            else: # if the game state is not active
                menu.passEvent(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                isMousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                isMousePressed = False
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and gameRunning == True:
                    g = pygame.transform.scale(gradient, (WIDTH, HEIGHT)) # scale the gradient to fit screen
                    canvas.blit(g, (0, 0)) # draw gradient over the screen
                    soundManager.pauseMusic()
                    pause = True
                    while pause: # pause game loop
                        for event in pygame.event.get():
                            pauseScreen.passEvent(event)
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    soundManager.unpauseMusic()
                                    pause = False
                        if pauseScreen.getFinished() == True:
                            save(player.getName(), player.getTotalScore())
                            STATE = 0
                            pause = False
                            running = False
                            pygame.quit()
                            sys.exit()
                        if pauseScreen.gotoMainMenu() == True:
                            leftPauseScreen = True
                            oldState = 1
                            STATE = 6
                            pause = False
                        pauseScreen.update()
                        pauseScreen.draw(canvas)
                        pygame.display.update()
                if leftPauseScreen == True:
                    leftPauseScreen = False
                    break
                if event.key == pygame.K_f and gameRunning == True: # check if player pressed f while game was running
                    gameRunning = False
                    soundManager.pauseMusic()
                    menu.openHud(canvas)
                if event.key == pygame.K_t and spamLevelProgress == True:
                    currentLevel.isLevelFinished = True
                if event.key == pygame.K_1:
                    bulletType = "normal"
                if event.key == pygame.K_2 and bulletType_bouncy_isUnlocked == True:
                    bulletType = "bouncy"
                if event.key == pygame.K_3 and bulletType_explosive_isUnlocked == True:
                    bulletType = "explosive"
                if event.key == pygame.K_4 and bulletType_spray_isUnlocked == True:
                    bulletType = "spray"
                if event.key == pygame.K_5 and bulletType_flame_isUnlocked == True:
                    bulletType = "flame"
                if event.key == pygame.K_z and distractionOrbs > 0 and currentLevel.checkPointBlockCollision(mousex, mousey) != True: # if they pressed z and have distraction orbs and if the mouse point doesn't land on a block or spawner
                    distractionOrbs -= 1
                    currentLevel.useItemById("distractionorb")
                if event.key == pygame.K_x and grenades > 0: # if they pressed x and have grenades
                    grenades -= 1
                    currentLevel.useItemById("grenade")
                if event.key == pygame.K_c and blades > 0 and currentLevel.checkPointBlockCollision(mousex, mousey) != True: # if they pressed c and have blades and if the mouse point doesn't land on a block or spawner
                    blades -= 1
                    currentLevel.useItemById("blade")
                if event.key == pygame.K_v and iceblocks > 0 and currentLevel.checkPointBlockCollision(mousex, mousey) != True: # if they pressed v and have ice tiles and if the mouse point doesn't land on a block or spawner
                    iceblocks -= 1
                    currentLevel.useItemById("icetile")
            if event.type == pygame.KEYUP:
                pass
        if gameRunning == True: # CHECK IF THE GAME IS ACTIVE
            # LOGIC :
            player.update(mousex, mousey) # Update Player
            currentLevel.update(player, soundManager) # update level, give player data
            currentLevel.checkZombiePlayerCollision(player, soundManager) # check if any zombies collided with the player
            player.checkDoubleWallCollision() # Run collision after updated levgetel data and translations
            currentLevel.updateCurrentBulletType(bulletType) # update the current bullet type
            # CHECK IF THE PLAYER DIED #
            if godMode == False:
                if player.getLifeStatus() == False:
                    soundManager.endMusic()
                    deathScreen = DeathScreen(0, 0, WIDTH, HEIGHT, player.getTotalScore(), roomsElapsed)
                    STATE = 3 # death screen state
            # CHECK IF THE PLAYER DIED #

            # CHECK TO ADVANCE LEVEL #
            if currentLevel.getLevelProgression() == True: #check if the level is finished | load the next room
                advanceLevel = False

                if player.getX() < tileWidth * 2 and player.getDX() < 0: # if player entered left entrance and is moving in that direction
                    if currentLevel.getRoomEntrance(player.getRect()) != "west":
                        playerSpawnX = WIDTH - tileWidth
                        playerSpawnY = player.getY()
                        advanceLevel = True
                elif player.getX() > WIDTH - (tileWidth * 2) and player.getDX() > 0: # if player entered right entrance and is moving in that direction
                    if currentLevel.getRoomEntrance(player.getRect()) != "east":
                        playerSpawnX = tileHeight
                        playerSpawnY = player.getY()
                        advanceLevel = True
                elif player.getY() < tileHeight and player.getDY() < 0: # if player entered north entrance and the player is moving in that direction
                    if currentLevel.getRoomEntrance(player.getRect()) != "north":
                        playerSpawnX = player.getX()
                        playerSpawnY = HEIGHT - tileHeight
                        advanceLevel = True
                elif player.getY() > HEIGHT - tileHeight and player.getDY() > 0: # if player entered south entrace and the player is moving in that direction
                    if currentLevel.getRoomEntrance(player.getRect()) != "south":
                        playerSpawnX = player.getX()
                        playerSpawnY = 0
                        advanceLevel = True
                if advanceLevel == True: # check if the player has been in a room entry location
                    player.setHealth(player.getMaxHealth()) # Regenerate player health
                    roomsElapsed += 1 # increase rooms elapsed by 1
                    if difficulty == "easy":
                        velIncreaser = 9
                        spawnTimeFactor = 19
                        healthIncreaser = 4
                    elif difficulty == "medium":
                        velIncreaser = 6
                        spawnTimeFactor = 14
                        healthIncreaser = 3
                    elif difficulty == "hard":
                        velIncreaser = 4
                        spawnTimeFactor = 9
                        healthIncreaser = 2
                    zombieMinVel = 1 + int(roomsElapsed / velIncreaser)
                    zombieMaxVel = 2 + int(roomsElapsed / velIncreaser)
                    zombieMinSpawnTime = 3 - int(roomsElapsed / spawnTimeFactor)
                    zombieMaxSpawnTime = 6 - int(roomsElapsed / spawnTimeFactor)
                    zombieHealth = 1 + int(roomsElapsed / healthIncreaser)
                    if zombieMinVel > 3:
                        zombieMinVel = 3
                    if zombieMaxVel > 6:
                        zombieMaxVel = 6
                    if zombieMinSpawnTime < 1:
                        zombieMinSpawnTime = 1
                    if zombieMaxSpawnTime < 2:
                        zombieMaxSpawnTime = 2
                    if zombieHealth > 10:
                        zombieHealth = 10
                    if roomsElapsed < 2: # spawn 4 zombies every room for the first 2 rooms
                        maxZombies += 4 # have those 4 extra zombies
                    else: # if it's past the first 2 rooms
                        roomsElapsed_Counter2 += 1 # increase max zombie increaser counter
                    if roomsElapsed_Counter2 >= 3: # every 3 rooms increase max zombies by 4
                        maxZombies += 4

                    currentLevel = Level(WIDTH, HEIGHT, roomsElapsed + 1, accuracyLevel, magAmmo, FPS, tileWidth, tileHeight, block1Image, spawnerImg, backgroundImg, arrowImage, playerSpawnX, playerSpawnY, zombieImg, drawBounds, maxZombies, zombieHealth, zombieMinVel, zombieMaxVel, zombieMinSpawnTime, zombieMaxSpawnTime)
                    currentLevel.spawnPlayer(player)
                    currentLevel.updateCurrentBulletType(bulletType)
                    player.addScore((roomsElapsed + 1) * 5) # give the player score for completing the room
            # CHECK TO ADVANCE LEVEL #

            # HUD #

            fpsString = "FPS: %d" %int(clock.get_fps()) # FPS STRING
            fps = hudFont2.render(fpsString, True, BLACK) # RENDER FPS

            fpsBoxX = 3
            fpsBoxY = 3
            fpsBoxWidth = fps.get_width() + 3
            fpsBoxHeight = fps.get_height() + 3

            fpsBox = pygame.Rect((fpsBoxX, fpsBoxY),(fpsBoxWidth, fpsBoxHeight))

            fpsTextX = fpsBox.center[0] - (fps.get_width() / 2)
            fpsTextY = fpsBox.center[1] - (fps.get_height() / 2)

            totalScoreString = "Total Score Obtained: %d" %player.getTotalScore() # TOTAL SCORE STRING
            totalScoreText = hudFont2.render(totalScoreString, True, BLACK) # TOTAL SCORE TEXT
            totalScoreTextY = HEIGHT - 10 - totalScoreText.get_height() # very bottom left, in the box
            totalScoreTextX = 6 # in the box

            roomNum = roomsElapsed + 1
            roomString = "Room #: %d" %roomNum # ROOM STRING
            roomText = hudFont2.render(roomString, True, BLACK) # RENDER ROOM TEXT
            roomTextX = totalScoreTextX # same x as total score
            roomTextY = totalScoreTextY - 10 - roomText.get_height() # above total score text

            scoreString = "Score: %d" %player.getScore() # SCORE STRING
            scoreText = hudFont2.render(scoreString, True, BLACK) # RENDER SCORE
            scoreTextX = totalScoreTextX # same x as total score
            scoreTextY = roomTextY - scoreText.get_height() - 6# Above room text

            # #BOTTOM LEFT BOX:
            bottomLeftBoxX = totalScoreTextX - 1
            bottomLeftBoxY = scoreTextY - 1
            bottomLeftBoxWidth = totalScoreText.get_width() + 40
            bottomLeftBoxHeight = totalScoreText.get_height() * 3 + 20
            bottomLeftBox = pygame.Rect((bottomLeftBoxX, bottomLeftBoxY),(bottomLeftBoxWidth, bottomLeftBoxHeight)) # Bottom left box

            # #HEALTH BAR:
            resourceBarWidth = (tileWidth * 5) * 0.75
            resourceBarHeight = tileHeight * 0.75
            healthBarX = WIDTH - int(resourceBarWidth) - 2
            healthBarY = 1
            healthBar = pygame.Rect((healthBarX, healthBarY),(int(resourceBarWidth), int(resourceBarHeight)))

            healthText = hudFont1.render("Health:", True, RED) # Health bar text
            healthTextX = healthBarX - healthText.get_width() - 1
            healthTextY = healthBarY + (resourceBarHeight / 2) - (healthText.get_height() / 2)

            if godMode == False:
                healthWidth = resourceBarWidth * player.getMissingHealth()
            else:
                healthWidth = resourceBarWidth
            activeHealthBar = pygame.Rect((healthBarX, healthBarY),(int(healthWidth), int(resourceBarHeight)))

            # # STAMINA BAR:
            staminaBarX = healthBarX
            staminaBarY = healthBarY + resourceBarHeight + 1
            staminaBar = pygame.Rect((staminaBarX, staminaBarY),(int(resourceBarWidth), int(resourceBarHeight)))

            staminaText = hudFont1.render("Stamina: ", True, YELLOW) # Stamina bar text
            staminaTextX = staminaBarX - staminaText.get_width() - 1
            staminaTextY = staminaBarY + (resourceBarHeight / 2) - (staminaText.get_height() / 2)

            staminaWidth = resourceBarWidth * player.getMissingStamina()
            activeStaminaBar = pygame.Rect((staminaBarX + 1, staminaBarY),(int(staminaWidth) - 1, int(resourceBarHeight))) # the + 1 - 1 to adjust for when being at 0 stamina causes the bar to go behind the border

            # # AMMO BOX:
            currentAmmunition = currentLevel.getAmmunition() # GET AMMO FROM CURRENT LEVEL
            ammoString = "%d / %d" %(currentAmmunition[0], currentAmmunition[1]) # AMMO STRING
            ammoText = hudFont2.render(ammoString, True, BLACK) #  RENDER TEXT

            ammoBoxX = WIDTH - ammoText.get_width() - 24
            ammoBoxY = HEIGHT - ammoText.get_height() - 24
            ammoBoxWidth = ammoText.get_width() + 12
            ammoBoxHeight = ammoText.get_height() + 12
            ammoBox = pygame.Rect((ammoBoxX, ammoBoxY),(ammoBoxWidth, ammoBoxHeight))

            ammoTextX = ammoBoxX + (ammoBoxWidth / 2) - (ammoText.get_width() / 2)
            ammoTextY = ammoBoxY + (ammoBoxHeight / 2) - (ammoText.get_height() / 2)

            # # BULLET TYPES HUD:
            bulletTextBox.setOrigin(WIDTH,  ammoTextY)
            bulletTextBox.update(bulletType_bouncy_isUnlocked, bulletType_explosive_isUnlocked, bulletType_spray_isUnlocked, bulletType_flame_isUnlocked)

            # # ITEMS HUD:
            if distractionOrbs > 1000: dOrb_Int = ">1x10^3"
            else: dOrb_Int = distractionOrbs
            dOrb_String = "[z] Distraction Orb (You have: x%s)" %str(dOrb_Int)

            if grenades > 1000: nade_Int = ">1x10^3"
            else: nade_Int = grenades
            nade_String = "[x] Grenades (You have: x%s)" %str(nade_Int)

            if blades > 1000: blade_Int = ">1x10^3"
            else: blade_Int = blades
            blade_String = "[c] Blades (You have x%s)" %str(blade_Int)

            if iceblocks > 1000: ice_Int = ">1x10^3"
            else: ice_Int = iceblocks
            ice_String = "[v] Freeze blocks (You have x%s)" %str(ice_Int)

            dOrb_Text = hudFont4.render(dOrb_String, True, BLACK)
            nade_Text = hudFont4.render(nade_String, True, BLACK)
            blade_Text = hudFont4.render(blade_String, True, BLACK)
            ice_Text = hudFont4.render(ice_String, True, BLACK)

            itemBoxWidth = dOrb_Text.get_width() + 30 + 6
            itemBoxHeight = (dOrb_Text.get_height() * 4) + 6

            itemBoxX = fpsBoxX
            itemBoxY = fpsBoxY + fpsBoxHeight

            itemBox = pygame.Rect((itemBoxX, itemBoxY),(itemBoxWidth, itemBoxHeight))

            dOrb_TextX = itemBoxX + 3
            dOrb_TextY = itemBoxY + 3

            nade_TextX = itemBoxX + 3
            nade_TextY = itemBoxY + dOrb_Text.get_height() + 3

            blade_TextX = itemBoxX + 3
            blade_TextY = itemBoxY + (dOrb_Text.get_height() * 2) + 3

            ice_TextX = itemBoxX + 3
            ice_TextY = itemBoxY + (dOrb_Text.get_height() * 3) + 3


            # HUD #

            """ DRAW : """

            canvas.fill(WHITE) # Clear the screen
            currentLevel.draw(canvas, player.getRect()) # draw player items

            player.draw(canvas) # Draw the player from the object

            # DRAW HUD #

            # BOXES #
            pygame.draw.rect(canvas, GRAY, fpsBox, 0) # fps background
            pygame.draw.rect(canvas, BLACK, fpsBox, 2) # fps box border

            pygame.draw.rect(canvas, GRAY, bottomLeftBox, 0)
            pygame.draw.rect(canvas, BLACK, bottomLeftBox, 2)

            pygame.draw.rect(canvas, GRAY, healthBar, 0) # Health bar background
            if godMode == True:
                pygame.draw.rect(canvas, BLUE, activeHealthBar, 0) # draw god mode health bar
            else:
                pygame.draw.rect(canvas, RED, activeHealthBar, 0) # Draw health bar
            pygame.draw.rect(canvas, BLACK, healthBar, 2) # Draw health bar border

            pygame.draw.rect(canvas, GRAY, staminaBar, 0) # Stamina bar background
            pygame.draw.rect(canvas, YELLOW, activeStaminaBar, 0) # Draw stamina bar
            pygame.draw.rect(canvas, BLACK, staminaBar, 2) # Draw stamina bar border

            pygame.draw.rect(canvas, GRAY, ammoBox, 0) # ammo box background
            pygame.draw.rect(canvas, BLACK, ammoBox, 2) # ammo box border

            pygame.draw.rect(canvas, GRAY, itemBox, 0) # draw item box background
            pygame.draw.rect(canvas, BLACK, itemBox, 2) # draw item box border

            # BOXES #

            # TEXT #
            canvas.blit(fps, (fpsTextX, fpsTextY)) # Draw fps
            canvas.blit(totalScoreText, (totalScoreTextX, totalScoreTextY))
            canvas.blit(roomText, (roomTextX, roomTextY))
            canvas.blit(scoreText, (scoreTextX, scoreTextY))

            canvas.blit(healthText, (healthTextX, healthTextY))
            canvas.blit(staminaText, (staminaTextX, staminaTextY))

            canvas.blit(ammoText, (ammoTextX, ammoTextY)) # draw ammo text

            canvas.blit(dOrb_Text, (dOrb_TextX, dOrb_TextY))
            canvas.blit(nade_Text, (nade_TextX, nade_TextY))
            canvas.blit(blade_Text, (blade_TextX, blade_TextY))
            canvas.blit(ice_Text, (ice_TextX, ice_TextY))

            # Bullet type box:
            bulletTextBox.draw(canvas)

            # TEXT #
            # DRAW HUD #

        if gameRunning == False:
            # Update menu:
            menu.update(player.getScore())
            currentLevel.updateCurrentBulletType(bulletType)
            bulletTextBox.update(bulletType_bouncy_isUnlocked, bulletType_explosive_isUnlocked, bulletType_spray_isUnlocked, bulletType_flame_isUnlocked)

            # Draw menu:
            menu.draw(canvas)

            # Check if the buy health button was clicked:
            if menu.actionPanel("health", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("health", "getcost"): # if they have enough score
                    player.addMaxHealth(1)
                    player.delScore(menu.actionPanel("health", "getcost"))
                    menu.actionPanel("health", "addcost")
                else:
                    menu.actionPanel("health", "setpanelnotenough") # say they don't have enough score

            # Check if they maxed player health:
            if player.getHealth() >= playerMaxHealth:
                player.setMaxHealth(playerMaxHealth) # re-adjust excess
                menu.actionPanel("health", "setpanelmaxed")

            # Check if the buy accuracy button was clicked:
            if menu.actionPanel("accuracy", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("accuracy", "getcost"): # if they have enough score
                    accuracyLevel -= 8
                    currentLevel.setAccuracyLevel(accuracyLevel) # reset accuracy level to current level
                    player.delScore(menu.actionPanel("accuracy", "getcost"))
                    menu.actionPanel("accuracy", "addcost")
                else:
                    menu.actionPanel("accuracy", "setpanelnotenough")# say they don't have enough score

            # Check if they maxed player accuracy:
            if accuracyLevel <= 0:
                accuracyLevel = 0 # re-adjust excess
                menu.actionPanel("accuracy", "setpanelmaxed")

            # Check if the buy agility button was clicked:
            if menu.actionPanel("agility", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("agility", "getcost"): # if they have enough score
                    player.addAgility(0.10) # increase player agility
                    player.delScore(menu.actionPanel("agility", "getcost"))
                    menu.actionPanel("agility", "addcost")
                else:
                    menu.actionPanel("agility", "setpanelnotenough") # say they don't have enough score

            # Check if they maxed their agility
            if player.getAgility() >= playerMaxAgility:
                player.setAgility(playerMaxAgility) # re-adjust excess
                menu.actionPanel("agility", "setpanelmaxed")

            # Check if the buy max ammo button was clicked:
            if menu.actionPanel("maxammo", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("maxammo", "getcost"): # if they have eenough score
                    magAmmo += 20
                    player.delScore(menu.actionPanel("maxammo", "getcost"))
                    menu.actionPanel("maxammo", "addcost")
                else:
                    menu.actionPanel("maxammo", "setpanelnotenough") # say they don't have enough score

            # Check if they maxed their magazine ammo
            if magAmmo >= maxMagazineAmmo:
                magAmmo = maxMagazineAmmo # re-adjust excess
                menu.actionPanel("maxammo", "setpanelmaxed")

            # Check if the buy 'bouncy' bullet type was clicked:
            if menu.actionPanel("bouncy", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("bouncy", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("bouncy", "getcost")) # deduct the cost
                    bulletType_bouncy_isUnlocked = True #unlock bullet type
                    menu.actionPanel("bouncy", "setpanelmaxed") # max the panel
                else:
                    menu.actionPanel("bouncy", "setpanelnotenough") # say they don't have enough score

            # Check if the buy 'spray' bullet type was clicked:
            if menu.actionPanel("spray", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("spray", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("spray", "getcost")) # deduct the cost
                    bulletType_spray_isUnlocked = True #unlock bullet type
                    menu.actionPanel("spray", "setpanelmaxed") # max the panel
                else:
                    menu.actionPanel("spray", "setpanelnotenough") # say they don't have enough score

            # Check if the buy 'explosive' bullet type was clicked:
            if menu.actionPanel("explosive", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("explosive", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("explosive", "getcost")) # deduct the cost
                    bulletType_explosive_isUnlocked = True #unlock bullet type
                    menu.actionPanel("explosive", "setpanelmaxed") # max the panel
                else:
                    menu.actionPanel("explosive", "setpanelnotenough") # say they don't have enough score

            # Check if the buy 'flame' bullet type was clicked:
            if menu.actionPanel("flame", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("flame", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("flame", "getcost")) # deduct the cost
                    bulletType_flame_isUnlocked = True #unlock bullet type
                    menu.actionPanel("flame", "setpanelmaxed") # max the panel
                else:
                    menu.actionPanel("flame", "setpanelnotenough") # say they don't have enough score

            # Check if the buy 'distractionorb' button was clicked:
            if menu.actionPanel("distractionorb", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("distractionorb", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("distractionorb", "getcost")) # deduct the cost
                    distractionOrbs += 1
                else:
                    menu.actionPanel("distractionorb", "setpanelnotenough") # say they don't have enough score

            # Check if the buy 'grenade' button was clicked:
            if menu.actionPanel("grenade", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("grenade", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("grenade", "getcost")) # deduct the cost
                    grenades += 1
                else:
                    menu.actionPanel("grenade", "setpanelnotenough") # say they don't have enough score

            # Check if the buy 'blade' button was clicked:
            if menu.actionPanel("blade", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("blade", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("blade", "getcost")) # deduct the cost
                    blades += 1
                else:
                    menu.actionPanel("blade", "setpanelnotenough") # say they don't have enough score

            # Check if the buy 'iceblock' button was clicked:
            if menu.actionPanel("iceblock", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("iceblock", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("iceblock", "getcost")) # deduct the cost
                    iceblocks += 1
                else:
                    menu.actionPanel("iceblock", "setpanelnotenough") # say they don't have enough score

            # Check if the buy '1 magazine' button was clicked:
            if menu.actionPanel("1mag", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("1mag", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("1mag", "getcost")) # deduct the cost
                    currentLevel.addMagazine(1)
                else:
                    menu.actionPanel("1mag", "setpanelnotenough") # say they don't have enough

            # Check if the buy '2 magazine' button was clicked:
            if menu.actionPanel("2mag", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("2mag", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("2mag", "getcost")) # deduct the cost
                    currentLevel.addMagazine(2)
                else:
                    menu.actionPanel("2mag", "setpanelnotenough") # say they don't have enough

            # Check if the buy '4 magazine' button was clicked:
            if menu.actionPanel("4mag", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("4mag", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("4mag", "getcost")) # deduct the cost
                    currentLevel.addMagazine(4)
                else:
                    menu.actionPanel("4mag", "setpanelnotenough") # say they don't have enough

            # Check if the buy '8 magazine' button was clicked:
            if menu.actionPanel("8mag", "getbuttonclicked") == True:
                if player.getScore() >= menu.actionPanel("8mag", "getcost"): # if they have enough score
                    player.delScore(menu.actionPanel("8mag", "getcost")) # deduct the cost
                    currentLevel.addMagazine(8)
                else:
                    menu.actionPanel("8mag", "setpanelnotenough") # say they don't have enough

            # Check if menu finished:
            if menu.getHudActivity() == False: # if the hud was closed
                soundManager.unpauseMusic()
                gameRunning = True # set the game state to true
                player.setD(0, 0) # kill player displacements

        pygame.display.update() # Update the screen

        if scoreSaved == True: # reset score saved
            scoreSaved = False
    elif STATE == 3: # if it's death screen state
        # SAVE SCORE #
        if scoreSaved == False: # if the score wasnt saved
            scoreFile = open("Data/saveddata/scores.txt", "a")
            s = "%s %d" %(player.getName(), player.getTotalScore())
            #scoreFile.write("\n") # create new line
            scoreFile.write(s) # write new score
            scoreFile.close() # close file
            scoreSaved = True # say the score was saved
        # SAVE SCORE #
                        
        # RESET GAME #
        if deathScreen.getDataReset() == False:
            oldState = STATE
            STATE = 6
            
            deathScreen.setDataReset(True) # tell the deathscreen that data was reset
        # RESET GAME #
        
        for event in pygame.event.get(): # run a for loop for all events
            deathScreen.passEvent(event) # pass death screen events
        deathScreen.update(FPS) # update death screen
        deathScreen.draw(canvas) # draw death screen
        pygame.display.update() # update pygame screen

        # Check if stuff was clicked
        if deathScreen.getClicked("mainmenu") == True: # if the main menu button was clicked
            mainMenu = Mainmenu(WIDTH, HEIGHT) # make a new main menu (clear zombies, etc)
            STATE = 1 # change to main menu state
        if deathScreen.getClicked("play") == True: # if the play button was clicked
            soundManager.playMusic()
            STATE = 6
            oldState = 2 # change to the play state
    elif STATE == 4: # if it's the splash screen state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(FPS)
        splashScreen.update(soundManager) # update splash screen
        canvas.fill(WHITE) # clear screen
        splashScreen.draw(canvas) # draw splash screen
        pygame.display.update() # update display
        if splashScreen.getFinished() == True: # if the splash screen is finished
            STATE = 1 # main menu
    elif STATE == 5: # if it's the name select state
        name = "CryptKeeper"
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            canvas.fill((180, 0, 0)) # clear screen red
            name = inputbox.ask(canvas, "Name (No Spaces)") # ask the player to enter their name
            if name.count(" ") < 1:
                break
        player.setName(name) # set the name to the player
        soundManager.playMusic()
        oldState = 2 # go to game state after next state
        STATE = 6 # reset game data 
    elif STATE == 6: # Reload game
        # Reset game data:
        # PROGRESSIVE DATA #
        roomsElapsed = 0
        roomsElapsed_Counter2 = 0 #keep track when to increase max zombies
        maxZombies = 4
        zombieHealth = 1
        zombieMinVel = 1
        zombieMaxVel = 4
        zombieMinSpawnTime = 1
        zombieMaxSpawnTime = 4
        if difficulty == "easy":
            playerHealth = 14
            playerStamina = 4
        if difficulty == "medium":
            playerHealth = 10
            playerStamina = 3
        if difficulty == "hard":
            playerHealth = 7
            playerStamina = 2

        playerMaxHealth = 25
        accuracyLevel = 80
        playerMaxAgility = 2.30
        magAmmo = 120
        maxMagazineAmmo = 240
        # PROGRESSIVE DATA #

        # ITEM DATA #
        bulletType = "normal"
        if unlockBulletTypes != True:
            bulletType_bouncy_isUnlocked = False
            bulletType_explosive_isUnlocked = False
            bulletType_spray_isUnlocked = False
            bulletType_flame_isUnlocked = False
        else:
            bulletType_bouncy_isUnlocked = True
            bulletType_explosive_isUnlocked = True
            bulletType_spray_isUnlocked = True
            bulletType_flame_isUnlocked = True

        if unlimitedItems == False: # if developer tools unlimited items isn't on
            distractionOrbs = 1 # give 1 of each item off the bat
            grenades = 1
            blades = 1
            iceblocks = 1
        else: # if it is on
            distractionOrbs = 99999999
            grenades = 9999999999
            blades = 999999999
            iceblocks = 999999999
        
        _clock = Clock() # Create the timer clock
        player = Player(WIDTH, HEIGHT, name, pistolCharImg, WIDTH / 2, HEIGHT / 2, playerHealth, playerStamina, FPS, drawBounds) # Start Player Object

        playerSpawnX = int(WIDTH / 2)
        playerSpawnY = HEIGHT - tileHeight
        currentLevel = Level(WIDTH, HEIGHT, roomsElapsed + 1, accuracyLevel, magAmmo, FPS, tileWidth, tileHeight, block1Image, spawnerImg, backgroundImg, arrowImage, playerSpawnX, playerSpawnY, zombieImg, drawBounds, maxZombies, zombieHealth, zombieMinVel, zombieMaxVel, zombieMinSpawnTime, zombieMaxSpawnTime) # Initalize first level
        currentLevel.spawnPlayer(player)
        menu = MenuHUD(WIDTH, HEIGHT, gradient, icon_traits, icon_bullet, icon_star, icon_bullets) # initalize hud
        bulletTextBox = BulletTextBox(WIDTH, HEIGHT, int(HEIGHT / 153), hudFont3)
        pauseScreen = PauseScreen(WIDTH, HEIGHT, mainMenu.getScaleWidth(), mainMenu.getScaleHeight())

        player.addScore(2500) # allow the player to start with a base score of 2500
        if infiniteScore == True:
            player.addScore(99999999999)
        # ITEM DATA #
        STATE = oldState
        
        

pygame.quit()
sys.exit()
