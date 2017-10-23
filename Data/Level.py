import pygame, random, math
from BloodExplosionManager import BloodExplosionManager
from ZombieParticleManager import ZombieParticleManager
from TileManager import FireTileManager, IceTileManager
from GrenadeManager import GrenadeManager
from BulletManager import BulletManager
from ZombieManager import ZombieManager
from ZombieSpawner import ZombieSpawner
from SoundManager import SoundManager
from BladeManager import BladeManager
from LevelDesign import LevelDesigns
from Strings import StringManager
from Zombie import Zombie
from Vector import Vec2d
from Clock import Clock
from Timer import Timer
from Arrow import Arrow

class Level(object):

    # Call constructor:
    def __init__(self, screenWidth, screenHeight, cryptnum, accuracyLevel, magAmmo, fps, tileWidth, tileHeight, blockImage, spawnerImage, backgroundImage, arrowImage, playerSpawnX, playerSpawnY, zombieImage, drawBounds, maxZombies, zombieHealth, zombieVelMin, zombieVelMax, zombieSpawnTimeMin, zombieSpawnTimeMax):
        """
        Constructor Arguments:
        screen width
        screen height
        cryptnum
        accuracyLevel
        magAmmo
        fps
        tile width
        tile height
        blockImage
        spawnerImage
        backgroundImage
        arrowImage
        playerSpawnX
        playerSpawnY
        zombieImage
        drawbounds | developer tool
        maxZombies
        zombieHealth
        zombieMinVel
        zombieMaxVel
        zombieSpawnTimeMin
        zombieSpawnTimeMax
        """

        # Basic Level Data:
        self.levelLoaded = False
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.cryptnum = cryptnum
        self.fps = fps
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.isMousePressed = False
        self.mousex = self.mousey = 0

        # Load Images:
        self.blockImage = blockImage
        self.spawnerImage = spawnerImage
        self.backgroundImage = backgroundImage
        self.block = pygame.transform.scale(self.blockImage, (self.tileWidth, self.tileHeight)) # transform to fit tile
        self.zblock = pygame.transform.scale(self.spawnerImage, (self.tileWidth, self.tileHeight)) # transform to fit tile
        self.background = pygame.transform.scale(self.backgroundImage, (self.screenWidth, self.screenHeight)) # transform to fit tile
        self.zombieImage = zombieImage
        self.tileZombie = pygame.transform.scale(self.zombieImage, (int(self.tileWidth * 0.60), int(self.tileHeight * 0.60)))
        self.distractionOrb = pygame.image.load("Data/images/distractionorb.png")
        self.distractionOrb = pygame.transform.scale(self.distractionOrb, (self.tileWidth, self.tileHeight)) # scale to fit a tile
        self.grenadeImage = pygame.image.load("Data/images/grenade.png")
        self.bladeImage = pygame.image.load("Data/images/blade.png")
        # Set the player spawn x,y:
        self.playerSpawnX = playerSpawnX
        self.playerSpawnY = playerSpawnY

        # Choose randomized Level
        self.levelDesigns = LevelDesigns()
        self.levelDesigns.generateLevels()
        self.level = random.randint(1, self.levelDesigns.getLevelAmount())

        # Get game-progression Data
        self.maxZombies = maxZombies
        self.zombieHealth = zombieHealth
        self.zombieVelMin = zombieVelMin
        self.zombieVelMax = zombieVelMax
        self.zombieSpawnTimeMin = zombieSpawnTimeMin
        self.zombieSpawnTimeMax = zombieSpawnTimeMax
        self.zombieAttackDelay = 2
        self.accuracyLevel = accuracyLevel
        self.magammo = magAmmo
        self.ammoSize = 20

        # Level Data:
        self.levelBlit = False
        self.Rects = []
        self.zombieSpawners = []
        self.rotatingZombies = []
        self.isLevelFinished = False # level finished variable
        self.roomEntrance = ""#to  keep track of where the room was entered
        self.roomEntranceSet = False # keep track of the entrance was properly recorded
        self.notifyFont = pygame.font.SysFont("Verdana", 36)
        self.bulletType = "normal"
        self.addGrenade = False
        self.addBlade = False
        self.addIceTile = False
        self.addDistractionOrb = False

        # Distraction Orb
        self.distractionOrbActive = False
        self.distractionOrbTimer = None
        self.distractionOrbRect = pygame.Rect((0, 0),(self.tileWidth, self.tileHeight)) # coordinate rectangle

        # Initalize Level Based Objects:
        self.stringManager = StringManager()
        self.bulletManager = BulletManager(self.screenWidth, self.screenHeight, self.notifyFont, self.ammoSize, self.magammo, 2)
        self.zombieManager = ZombieManager(self.screenWidth, self.screenHeight, self.zombieAttackDelay, zombieImage, drawBounds)
        self.zombieParticleManager = ZombieParticleManager()
        self.bloodExplosionManager = BloodExplosionManager(self.screenWidth, self.screenHeight)
        self.fireTileManager = FireTileManager(self.screenWidth, self.screenHeight, self.tileWidth, self.tileHeight)
        self.iceTileManager = IceTileManager(self.screenWidth, self.screenHeight, self.tileWidth, self.tileHeight)
        self.grenadeManager = GrenadeManager(self.tileWidth, self.tileHeight, self.grenadeImage)
        self.bladeManager = BladeManager(self.screenWidth, self.screenHeight, self.tileWidth, self.tileHeight, self.bladeImage)
        self.gameClock = Clock()

        # End-level arrow data:
        self.arrowImage = arrowImage
        self.arrows = []
        self.arrows.append(Arrow(self.arrowImage, (self.screenWidth / 2) - (self.tileWidth / 2), (self.tileHeight * 2) / 2, 90, 1, 20)) # create the top arrow
        self.arrows.append(Arrow(self.arrowImage, (self.screenWidth / 2) - (self.tileWidth / 2), self.screenHeight - ((self.tileHeight * 2) / 2), -90, 1, 20)) # create the bottom arrow
        self.arrows.append(Arrow(self.arrowImage, (self.tileWidth * 3) / 2, self.screenHeight / 2, 180, 2, 20)) # create the left arrow
        self.arrows.append(Arrow(self.arrowImage, self.screenWidth - ((self.tileWidth * 3) / 2), self.screenHeight / 2, 0, 2, 20)) # create the right arrow

    # Get level progression function (whether it's finished or not):
    def getLevelProgression(self):
        return self.isLevelFinished

    # Set the player spawn based off of level:
    def spawnPlayer(self, player):
        player.setX(self.playerSpawnX)
        player.setY(self.playerSpawnY)

    # Get tile size
    def getTileSize(self):
        return (self.tileWidth, self.tileHeight)

    # Load the level data to create blocks and spawners:
    def loadLevel(self):
        if self.level == 1: # Check if level chosen was level 1
            levelData = self.levelDesigns.getLevel1() # Get the level Data of level 1
        elif self.level == 2: # Check if the level chosen was level 2
            levelData = self.levelDesigns.getLevel2() # Get the level Data of level 2
        elif self.level == 3: # Check if the level chosen was level 3
            levelData = self.levelDesigns.getLevel3() # Get the level Data of level 3
        elif self.level == 4: # Check if level chosen was level 4
            levelData = self.levelDesigns.getLevel4() # Get the level Data of level 4
        elif self.level == 5: # Check if level chosen was level 5
            levelData = self.levelDesigns.getLevel5() # Get the level Data of level 5
        elif self.level == 6: # Check if level chosen was level 6
            levelData = self.levelDesigns.getLevel6() # Get the level Data of level 6
        elif self.level == 7: # Check if level chosen was level 7
            levelData = self.levelDesigns.getLevel7() # Get the level Data of level 7
        elif self.level == 8: # Check if level chosen was level 8
            levelData = self.levelDesigns.getLevel8() # Get the level Data of level 8
        elif self.level == 9: # Check if level chosen was level 9
            levelData = self.levelDesigns.getLevel9() # Get the level Data of level 9
        elif self.level == 10: # Check if level chosen was level 10
            levelData = self.levelDesigns.getLevel10() # Get the level Data of level 10
        x = 0 # Start X at 0
        y = 0 # Start Y at 0
        for row in levelData: # run a for loop for all the rows in level data
            for col in row: # run a for loop for all the colums in the row
                if col == "1": # check if the column section is labeled 1
                    self.Rects.append(pygame.Rect((x, y),(self.tileWidth, self.tileHeight))) # append a rectangle
                if col == "2": # check if the column section is labeled 2
                    self.Rects.append(pygame.Rect((x, y),(self.tileWidth, self.tileHeight))) # append a rectangle
                if col == "3": # check if the column section is labeled 3
                    self.zombieSpawners.append(ZombieSpawner(x, y, self.zombieManager, int(self.maxZombies / self.levelDesigns.getSpawnerAmount(self.level)), self.zombieSpawnTimeMin, self.zombieSpawnTimeMax, self.zombieVelMin, self.zombieVelMax, self.zombieHealth)) # Initalize a zombie spawner with given data
                    self.rotatingZombies.append(0)
                x += self.tileWidth # adjust x
            y += self.tileHeight # adjust y
            x = 0 # reset row
        self.levelData = levelData
        self.levelLoaded = True

    # Record where the room was entered for post-battle room transitioning
    def recordRoomEntrance(self, playerRect):
        if self.playerSpawnX == self.screenWidth - self.tileWidth: # if the player spawn x was the east entrance
            self.roomEntrance = "east"
        elif self.playerSpawnX == self.tileWidth: # if the player spawn x was the west entrance
            self.roomEntrance = "west"
        elif self.playerSpawnY >= self.screenHeight - self.tileHeight: # if the player spawn y was the south entrance
            self.roomEntrance = "south"
        elif self.playerSpawnY == 0: # if the player spawn y was the north entrance
            self.roomEntrance = "north"

    # Pass pygame events:
    def passEvent(self, event, soundManager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isMousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.isMousePressed = False
        if event.type == pygame.MOUSEMOTION:
            self.mousex, self.mousey = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.bulletManager._reload(self.getGameClock(), self.stringManager, soundManager)

    # Use an item by calling it's ID
    def useItemById(self, item):
        if item == "distractionorb":
            self.addDistractionOrb = True
        elif item == "grenade":
            self.addGrenade = True
        elif item == "blade":
            self.addBlade = True
        elif item == "icetile":
            self.addIceTile = True

    # Update the current bullet type set in main
    def updateCurrentBulletType(self, bulletType):
        self.bulletType = bulletType

    # Check if a point collides with any of the blocks
    def checkPath(self, x, y):
        r = pygame.Rect((x,y), (1,1))
        for block in range(len(self.Rects)):
            if r.colliderect(self.Rects[block]):
                return False
        return True

    # Get game clock
    def getGameClock(self):
        return self.gameClock

    # Get total ammunition from bullet amanger
    def getAmmunition(self):
        return (self.bulletManager.getAmmo(), self.bulletManager.getMagazines())

    # Set the accuracy level
    def setAccuracyLevel(self, accuracyLevel):
        self.accuracyLevel = accuracyLevel

    # Get the accuracy level
    def getAccuracyLevel(self):
        return self.accuracyLevel

    # Get the tile where the distraction orb will be based off of the mouse location
    def distractionOrb_setLocation(self, mousex, mousey):
        for i in range(int(self.screenHeight / self.tileHeight)): # run a for loop for the amount of tiles on the y axis
            for z in range(int(self.screenWidth / self.tileWidth)): # run a for loop for the amount of tiles on the x axis
                tileRect = pygame.Rect((z * self.tileWidth, i * self.tileHeight),(self.tileWidth, self.tileHeight)) # generate the tile as a pygame rectangle
                if tileRect.collidepoint(mousex, mousey) == True: # check if the mouse lands on the tile
                    self.distractionOrbRect = tileRect # place tile

    # Set distraction orb active
    def distractionOrb_setActive(self, activity):
        self.distractionOrbActive = activity
        self.distractionOrbTimer = Timer(10, self.getGameClock().getElapsedSeconds())

    # Add a magazine to the bullet manager
    def addMagazine(self, magazines):
        self.bulletManager.addMagazines(magazines)

    # Check if a point doesn't land on a level block
    def checkPointBlockCollision(self, x, y):
        for block in range(len(self.Rects)): # run a for loop for all blocks
            if self.Rects[block].collidepoint(x, y) == True: # if the point lands on the block
                return True # say that the point lands on one of the blocks
        for spawner in range(len(self.zombieSpawners)): # run a for loop for all zombie spawners
            spawnerRect = pygame.Rect((self.zombieSpawners[spawner].getX(), self.zombieSpawners[spawner].getY()),(self.tileWidth, self.tileHeight)) # generate a rect of spawner
            if spawnerRect.collidepoint(x, y) == True: # if the point lands on the block
                return True # say that the point lands on one of the spawners
        return False # return False if it hasn't returned true yet, because it means it hasn't landed on any blocks

    # Update level data & logic:
    def update(self, player, soundManager):
        if self.levelLoaded == False: # Check if the level was loaded
            self.loadLevel()
            newLevelString = "Crypt: %d" %self.cryptnum
            textInstance = self.notifyFont.render(newLevelString, True, (255, 0, 0)) # for size reference
            self.stringManager.addText(newLevelString, (0, 255, 0), self.notifyFont, ((self.screenWidth / 2) - (textInstance.get_width() / 2), self.screenHeight - (self.screenHeight * 0.75)), 4, -3, self.getGameClock()) # add the text for a new crypt
        if self.roomEntranceSet == False: # if the entrance hasn't been recorded
            self.recordRoomEntrance(player.getRect()) # set the room entrance
            self.roomEntranceSet = True
        self.gameClock.update(self.fps)

        self.zombieManager.update(player, self.gameClock, self.zombieParticleManager, self.distractionOrbActive, self.distractionOrbRect) # Update zombie manager

        """ CHECK IF THE LEVEL IS FINISHED """
        if self.zombieManager.getZombiesKilled() >= self.maxZombies + 4: # check if the amount of zombies killed = the amount of every existing zombies
            self.isLevelFinished = True
        """ CHECK IF THE LEVEL IS FINISHED """

        """ UPDATE DISTRACTION ORB """
        if self.addDistractionOrb == True: # if the player pressed Q
            self.addDistractionOrb = False # switch/off to kill spam
            self.distractionOrb_setLocation(self.mousex, self.mousey) # place location
            self.distractionOrb_setActive(True) # set the distraction orb in the level active

        if self.distractionOrbActive == True: # if there currently is a distraction orb
            if self.distractionOrbTimer.getAlert() == True: # if the distraction orb is finished and must despawn
                self.distractionOrbActive = False # turn off the distraction orb
            else: # if not
                self.distractionOrbTimer.update(self.getGameClock().getElapsedSeconds()) # update the distraction orb timer
        """ UPDATE DISTRACTION ORB """

        """ UPDATE GRENADES """
        if self.addGrenade == True:
            self.addGrenade = False
            self.grenadeManager.addGrenade(player.getRect().center[0], player.getRect().center[1], self.mousex, self.mousey) # spawn a grenade
        self.grenadeManager.update(self.Rects, self.zombieManager.getZombies(), player)
        """ UPDATE GRENADES """

        """ UPDATE BLADES """
        if self.addBlade == True: # if the player pressed C
            self.addBlade = False # turn off to kill spam
            self.bladeManager.addBlade(self.mousex, self.mousey, self.getGameClock()) # add blade
        """ UPDATE BLADES """

        """ ADD ICE TILE """
        if self.addIceTile == True: # if player pressed v
            self.addIceTile = False # turn off to kill spam
            self.iceTileManager.addTile(self.mousex, self.mousey, self.getGameClock()) # add a tile
        """ ADD ICE TILE """

        """ SHOOT A BULLET """
        if self.isMousePressed == True and player.getRunningStatus() == False and player.getRect().collidepoint(self.mousex, self.mousey) == False and self.bulletManager.isReloading() == False: # Check if player clicked and if the player isn't running and check if the mouse isn't overlapping the player and they aren't reloading
            soundManager.playSound("bang") # play the bullet shoot sound
            self.isMousePressed = False # Set to false to prevent bullet Spam
            self.bulletManager.addBullet(player.getX(), player.getY(), self.mousex, self.mousey, self.getAccuracyLevel(), self.bulletType) # create a bullet

        """ CHECK PLAYER COLLISION WITH WALLS """
        for i in range(1, 5): # run a for loop for all player walls
                player.setCollisionBound(i, False) # default all wall collisions to be false
        for block in range(len(self.Rects)): # run a for loop for all existing blocks
            for wall in range(1, 5): # run a for loop for all walls
                if player.getWall(wall).colliderect(self.Rects[block]): # Check if the current wall collided with the current block
                    player.setCollisionBound(wall, True)
        """ CHECK PLAYER COLLISION WITH WALLS """

        """ CHECK IF THE ZOMBIES COLLIDED WITH THE FIRE & ICE TILES """
        self.zombieManager.checkFireTileCollision(self.fireTileManager, self.getGameClock()) # update to set zombies on fire
        self.zombieManager.checkIceTileCollision(self.iceTileManager, self.getGameClock()) # update to set zombies frozen
        """ CHECK IF THE ZOMBIES COLLIDED WITH THE FIRE & ICE TILES """

        """ CHECK BULLET COLLISION WITH WALLS """
        if self.bulletManager.getBulletAmount() > 0: # check if bullets exist
            bulletX = self.bulletManager.getBulletLocationX() # import bullet x array
            bulletY = self.bulletManager.getBulletLocationY() # import bullet y array
            for bullet in range(self.bulletManager.getBulletAmount()): # run a for loop for all bullets
                if self.bulletManager.getBulletActivity(bullet) == True: # check if the bullet is active before any relevant code happens
                    bx = bulletX[bullet] - int(self.bulletManager.getBulletRadius(bullet) / 2) # Set the bullet X as if it was a rectangle
                    by = bulletY[bullet] - int(self.bulletManager.getBulletRadius(bullet) / 2) # Set the bullet Y as if it was a rectangle
                    bl = self.bulletManager.getBulletRadius(bullet) * 2 # Set the Width & Height (Length) of the bullet as if it was a rectangle
                    bulletRect = pygame.Rect((bx, by),(bl, bl)) # Create the Rectangle with the created Data
                    for block in range(len(self.Rects)): # run a for loop for all blocks
                        if bulletRect.colliderect(self.Rects[block]) == True:
                            if self.bulletManager.getBulletType(bullet) != "bouncy":
                                self.bulletManager.setBulletActivity(bullet, False)
                            else: # if the bullet type is bouncy
                                if self.bulletManager.getBouncyBulletBounces(bullet) >= 3: # if it's bounced 3 times
                                    self.bulletManager.setBulletActivity(bullet, False) # set the bullet inactive
                                else:
                                    _block = self.Rects[block]
                                    blockTop = pygame.Rect((_block.x - 1, _block.y - 1),(_block.width + 1, 3))
                                    blockBottom = pygame.Rect((_block.x, _block.y + _block.height - 1),(_block.width + 1, 2))
                                    blockLeft = pygame.Rect((_block.x - 1, _block.y  - 1),(2, _block.height + 1))
                                    blockRight = pygame.Rect((_block.x + _block.width - 1, _block.y - 1),(3, _block.height + 1))
                                    if blockTop.colliderect(bulletRect) or blockBottom.colliderect(bulletRect):
                                        self.bulletManager.flipVectorY(bullet)# flip direction Y
                                    if blockLeft.colliderect(bulletRect) or blockRight.colliderect(bulletRect):
                                        self.bulletManager.flipVectorX(bullet)# flip direction X
                                    self.bulletManager.lungeBullet(bullet)
                                    self.bulletManager.addBouncyBulletBounce(bullet)

        """ CHECK BULLET COLLISION WITH WALLS """


        """ IF A BLOCK IS INCOMING. GO AROUND IT PATHFINDING"""
        for zombie in range(len(self.zombieManager.getZombies())): # run a for loop for all zombies
                if self.zombieManager.getZombies()[zombie].getLifeStatus() == True: # check if the zombie is alive before you do anything with it
                    for block in range(len(self.Rects)): # run a for loop for all blocks
                        if self.zombieManager.getZombies()[zombie].getCollisionRect().colliderect(self.Rects[block]) == True: # Check if the zombie is colliding with the block in the first place
                            differenceX = self.zombieManager.getZombies()[zombie].getCollisionRect().center[0] - self.Rects[block].center[0]
                            differenceY = self.zombieManager.getZombies()[zombie].getCollisionRect().center[1] - self.Rects[block].center[1]
                            if differenceX < 0:
                                differenceX *= - 1
                            if differenceY < 0:
                                differenceY *= - 1
                            if differenceX <= self.Rects[block].width / 2 and differenceX >= 0 and differenceY <= self.Rects[block].height/2 and differenceY >= 0:
                                # Check if the zombie's collision rectangle's midleft x  is in between the block center and the right side of the block
                                if self.zombieManager.getZombies()[zombie].getRect().midleft[0] < self.Rects[block].center[0] + self.Rects[block].width and self.zombieManager.getZombies()[zombie].getCollisionRect().midleft[0] > self.Rects[block].center[0]:
                                    self.zombieManager.getZombies()[zombie].setCollisionBound(1, True) # Tell the zombie's left wall is collided
                                    zombieLeftSide = self.zombieManager.getZombies()[zombie].getCollisionRect().midleft[0]
                                    self.zombieManager.getZombies()[zombie].translate(self.Rects[block].midright[0] - zombieLeftSide, 0) # Translate the zombie away from the wall ( to the right)
                                # Check if the zombie's collision rectangle's midright x is in between the block center and the left side of the block
                                if self.zombieManager.getZombies()[zombie].getRect().midright[0] > self.Rects[block].center[0] - self.Rects[block].width and self.zombieManager.getZombies()[zombie].getCollisionRect().midright[0] < self.Rects[block].center[0]:
                                    self.zombieManager.getZombies()[zombie].setCollisionBound(2, True) # Tell the zombie's right wall is collided
                                    zombieRightSide = self.zombieManager.getZombies()[zombie].getCollisionRect().midright[0]
                                    self.zombieManager.getZombies()[zombie].translate(self.Rects[block].midleft[0] - zombieRightSide, 0) # Translate the zombie away from the wall ( to the left )
                                # Check if the zombie's collision rectangle's midtop y is in between the block center and the bottom side of the block
                                if self.zombieManager.getZombies()[zombie].getRect().midtop[1] < self.Rects[block].center[1] + self.Rects[block].height and self.zombieManager.getZombies()[zombie].getCollisionRect().midtop[1] > self.Rects[block].center[1]:
                                    self.zombieManager.getZombies()[zombie].setCollisionBound(3, True) # Tell the zombie's top wall is collided
                                    zombieTopSide = self.zombieManager.getZombies()[zombie].getCollisionRect().midtop[1]
                                    self.zombieManager.getZombies()[zombie].translate(0, self.Rects[block].midbottom[1] - zombieTopSide) # Translate the zombie away from the wall ( to the bottom )
                                # Check if the zombie's collision rectangle's midbottom y is in between the block center and the top side of the block
                                elif self.zombieManager.getZombies()[zombie].getRect().midbottom[1] > self.Rects[block].center[1] - self.Rects[block].height and self.zombieManager.getZombies()[zombie].getCollisionRect().midbottom[1] < self.Rects[block].center[1]:
                                    self.zombieManager.getZombies()[zombie].setCollisionBound(4, True) # Tell the zombie's bottom wall is collided
                                    zombieBottomSide = self.zombieManager.getZombies()[zombie].getCollisionRect().midbottom[1]
                                    self.zombieManager.getZombies()[zombie].translate(0, self.Rects[block].midtop[1] - zombieBottomSide)
        """ IF A BLOCK IS INCOMING, GO AROUND IT PATHFINDING """

        """ CHECK ZOMBIE COLLISION WITH WALLS """
        for zombie in range(len(self.zombieManager.getZombies())):
            if self.zombieManager.getZombies()[zombie].getLifeStatus() == True:
                if self.zombieManager.getZombies()[zombie].getRect().colliderect(player.getRect()) != True: # if they are not colliding with the player
                    currentZombie = self.zombieManager.getZombies()[zombie]
                    for block in range(len(self.Rects)):
                        if currentZombie.getDX() > 0: # if the zombie's current disp. is heading right
                            midRightRect = pygame.Rect((currentZombie.getCollisionRect().midright[0] + currentZombie.getVelocity(), currentZombie.getCollisionRect().midright[1]), (1, 1)) # set a rectangle in upcoming unit
                            if midRightRect.colliderect(self.Rects[block]) == True: # if the area they are approaching has a block
                                currentZombie.setD(0, -currentZombie.getVelocity()) # stop the zombie from going in that direction and have them head upwards
                        if currentZombie.getDX() < 0: # if the zombie's current disp. is heading left
                            midLeftRect = pygame.Rect((currentZombie.getCollisionRect().midleft[0] - currentZombie.getVelocity(), currentZombie.getCollisionRect().midleft[1]),(1, 1)) # set a rectangle in upcoming unit
                            if midLeftRect.colliderect(self.Rects[block]) == True: # if the area they are approaching has a block
                                currentZombie.setD(0, currentZombie.getVelocity()) # stop the zombie from going in that direction and have them head downwards
                        if currentZombie.getDY() > 0: # if the zombie's current disp. is heading down
                            midBottomRect = pygame.Rect((currentZombie.getCollisionRect().midbottom[0], currentZombie.getCollisionRect().midbottom[1] + currentZombie.getVelocity()),(1, 1)) # set a rectangle in upcoming direction
                            if midBottomRect.colliderect(self.Rects[block])  == True: # if the area they are approaching has a block
                                currentZombie.setD(currentZombie.getVelocity(), 0) # stop the zombie from going in that direction and have them head to the right
                        if currentZombie.getDY() < 0: # if the zombie's current disp. is heading up
                            midTopRect = pygame.Rect((currentZombie.getCollisionRect().midtop[0], currentZombie.getCollisionRect().midtop[1] - currentZombie.getVelocity()),(1, 1)) # set a rectangle in upcoming direction
                            if midTopRect.colliderect(self.Rects[block]) == True: # if the area they are approaching has a block
                                currentZombie.setD(-currentZombie.getVelocity(), 0) # stop the zombie from going in that direction and have them head to the left
                        #if currentZombie.getDX() > 0 and currentZombie.getDY() > 0: # if the zombie is going northeast direction
                            #northEastRect = pygame.Rect((currentZombie.getCollisionRect().),())
        """ CHECK ZOMBIE COLLISION WITH WALLS """

        """ MANAGE COLLISION WITH BLOOD PARTICLES """
        for particle in range(self.bloodExplosionManager.getLength()):
            if self.bloodExplosionManager.getParticleActive(particle) == True:
                if player.getRect().collidepoint(self.bloodExplosionManager.getX(particle), self.bloodExplosionManager.getY(particle)) == True: # if the player rect overlaps the current particle
                    self.bloodExplosionManager.setParticleActive(particle, False) # set that particle inactive
                for block in range(len(self.Rects)): # run a for loop for all blocks
                    if self.Rects[block].collidepoint(self.bloodExplosionManager.getX(particle), self.bloodExplosionManager.getY(particle)) == True: # if the current block overlaps current particle
                        self.bloodExplosionManager.setParticleActive(particle, False) # set that particle inactive
        """ MANAGE COLLISION WITH BLOOD PARTICLES """

        """ CHECK IF ANY ICE TILES / FIRE TILES OVERLAP, DELETE IF SO """
        for iceTile in range(len(self.iceTileManager.getTiles())): # run a for loop for all ice tiles
            if self.iceTileManager.getActive(iceTile) == True: # if the ice tile is active
                for fireTile in range(len(self.fireTileManager.getTiles())): # run a for loop for all fire tiles
                    if self.fireTileManager.getActive(fireTile) == True: # if the fire tile is active
                        if self.iceTileManager.getTiles()[iceTile].colliderect(self.fireTileManager.getTiles()[fireTile]) == True: # if the ice tile is overlapping with the fire tile
                            self.iceTileManager.setActive(iceTile, False) # set ice tile inactive
                            self.fireTileManager.setActive(fireTile, False) # set fire tile inactive
        """ CHECK IF ANY ICE TILES / FIRE TILES OVERLAP, DELETE IF SO """

        """ UPDATE ARROW TRANSLATIONS """
        if self.getLevelProgression() == True: # if the level was completed
            for arrow in range(len(self.arrows)): # run a for loop for all arrows
                self.arrows[arrow].update(self.gameClock.getElapsedFrames()) # update the arrows translations
        """ UPDATE ARROW TRANSLATIONS """

        """ UPDATING ROTATING ZOMBIES IN SPAWNERS """
        for zombie in range(len(self.zombieSpawners)):
            self.rotatingZombies[zombie] += 6
            if self.rotatingZombies[zombie] >= 360:
                self.rotatingZombies[zombie] = 0
        """ UPDATING ROTATING ZOMBIES IN SPAWNERS """

        """ MANAGE LEVEL RESPONSIBILITIES """
        if self.isLevelFinished == False: # If the level isn't finished (secondary measure):
            for spawner in range(len(self.zombieSpawners)): # Run a for loop for all zombie spawners
                self.zombieSpawners[spawner].update(self.gameClock) # Update Zombie Spawners
        self.bulletManager.update(self.getGameClock(), self.stringManager, soundManager) # Update bullets

        if self.distractionOrbActive == True: # if the distraction orb is active
            self.zombieManager.finalUpdate(self.distractionOrbRect, self.getGameClock()) # post-collision zombie update, have it face D_ORB
        else: # if the distraction orb is not active
            self.zombieManager.finalUpdate(player.getRect(), self.getGameClock()) # Post-collision zombie update

        self.zombieManager.checkBulletCollision(soundManager, self.bulletManager.getBulletLocationX(), self.bulletManager.getBulletLocationY(), self.bulletManager, player, self.bloodExplosionManager, self.fireTileManager, self.bulletType, self.getGameClock()) # check the bullet collision between the bullets and zombies
        self.stringManager.update(self.getGameClock())
        self.bloodExplosionManager.update()
        self.zombieParticleManager.update()
        self.fireTileManager.update(self.getGameClock())
        self.iceTileManager.update(self.getGameClock())
        self.bladeManager.update(self.zombieManager.getZombies(), player, self.getGameClock())
        """ MANAGE LEVEL RESPONSIBILITIES """

    # Check zombie to player collision
    def checkZombiePlayerCollision(self, player, soundManager):
        for zombie in range(len(self.zombieManager.getZombies())): # run a for loop for all zombies
            if self.zombieManager.getZombies()[zombie].getLifeStatus() == True:
                if self.zombieManager.getZombies()[zombie].getAttackStatus() == True:
                    if self.zombieManager.getZombies()[zombie].getRect().colliderect(player.getRect()): # if the current zombie is colliding with the player
                        soundManager.playSound("attack") # play the zombie attack sound
                        player.giveHealth(-1) # take 1 hp away from the player
                        playerVec = Vec2d(player.getRect().center[0], player.getRect().center[1])
                        zombieVec = Vec2d(self.zombieManager.getZombies()[zombie].getRect().center[0], self.zombieManager.getZombies()[zombie].getRect().center[1])
                        playerToZombieVec = Vec2d(playerVec - zombieVec)
                        playerToZombieVec = playerToZombieVec.normalized()

                        # translate to the player ( Lunge like ) by half the width and height of it's collision rectangle
                        self.zombieManager.getZombies()[zombie].translate(playerToZombieVec[0] * (player.getRect().width / 2), playerToZombieVec[1] * (player.getRect().height / 2))
                        self.zombieManager.setZombieAttacked(zombie, self.getGameClock())

                        # Draw the zombie speech string:
                        zombieQuotes = ["Scratch!", "Swipe!", "Chomp!", "Slash!", "Whack!", "Slam!", "Grrgah!", "Kick!", "Bite!", "Stomp!"]
                        zombieSpeech = random.randint(0,9) # Select out of the 4 speeches
                        zombieSpeech = zombieQuotes[zombieSpeech]
                        font = pygame.font.SysFont("Trebuchet MS", 10)
                        self.stringManager.addText(zombieSpeech, (255, 25, 25), font, self.zombieManager.getZombies()[zombie].getRect().center, 1, -1, self.getGameClock())
                        font = None # Delete from memory

    # Get the velocity of the last spawned zombie
    def getLatestZombieVelocity(self):
        return self.zombieManager.getZombies()[len(self.zombieManager.getZombies()) - 1].getVelocity()

    # Get the amount of zombies spawned:
    def getZombiesSpawned(self):
        zombiesSpawned = 0
        for spawner in range(len(self.zombieSpawners)):
            zombiesSpawned += self.zombieSpawners[spawner].getZombiesSpawned()
        return zombiesSpawned

    # Draw relevant level data (Zombies, bullet's, blocks, spawners)
    def draw(self, canvas, playerRect):
        canvas.blit(self.background, (0, 0)) # draw background image

        # Draw arrows:
        if self.getLevelProgression() == True: # if level is finished
            if self.getRoomEntrance(playerRect) != "north": # if the player entrance isn't north
                self.arrows[0].draw(canvas) # draw north arrow
            if self.getRoomEntrance(playerRect) != "south": # if the player entrance isn't south
                self.arrows[1].draw(canvas) # draw south arrow
            if self.getRoomEntrance(playerRect) != "west": # if the player entrance isn't west
                self.arrows[2].draw(canvas) # draw west arrow
            if self.getRoomEntrance(playerRect) != "east": # if the player entrance isn't east
                self.arrows[3].draw(canvas) # draw east arrow


        for rect in range(len(self.Rects)): # for loop to run all rects
            canvas.blit(self.block, (self.Rects[rect].x, self.Rects[rect].y)) #draw a block
        for spawner in range(len(self.zombieSpawners)):
            pygame.draw.rect(canvas, (153, 0, 0), (self.zombieSpawners[spawner].getX(), self.zombieSpawners[spawner].getY(), self.tileWidth, self.tileHeight), 0)
            zombie = pygame.transform.rotate(self.tileZombie, self.rotatingZombies[spawner])
            zombieRect = zombie.get_rect(center=(self.zombieSpawners[spawner].getX() + int(self.tileWidth / 2), self.zombieSpawners[spawner].getY() + int(self.tileHeight / 2)))
            if self.zombieSpawners[spawner].getActive() == True:
                canvas.blit(zombie, zombieRect)
            canvas.blit(self.zblock, (self.zombieSpawners[spawner].getX(), self.zombieSpawners[spawner].getY()))
        if self.distractionOrbActive == True: # if there is currently a distraction orb placed
            canvas.blit(self.distractionOrb, self.distractionOrbRect) # draw the distraction Orb
        self.bladeManager.draw(canvas)
        self.iceTileManager.draw(canvas) # draw ice tiles
        self.fireTileManager.draw(canvas) # draw fire tiles
        self.bulletManager.draw(canvas, playerRect) # draw bullets
        self.zombieManager.draw(canvas) # draw zombies
        self.grenadeManager.draw(canvas) # draw grenades
        self.bloodExplosionManager.draw(canvas) # draw blood explosions
        self.zombieParticleManager.draw(canvas) # draw zombie fire/frost particles
        self.stringManager.draw(canvas) # draw texts

    # Get where the room entrance was:
    def getRoomEntrance(self, playerRect):
        if self.roomEntranceSet == False: # if the room entrance wasn't recorded yet
            self.recordRoomEntrance(playerRect)# record the rooms entrance
            self.roomEntranceSet = True # say that the room entrance was recorded
        return self.roomEntrance

    # Dispose of level (Data, set everything to inactive)
    def dispose(self):
        for spawner in range(len(self.zombieSpawners)):
            self.zombieSpawners[spawner].dispose()
        self.zombieManager.dispose() # dispose of all zombies and zombieManager
        self.bulletManager.dispose() # dispose of all bullets and bulletManager
        self.stringManager.dispose() # dispose of all the strings
        self.bloodExplosionManager.dispose() # dispose of all blood explosions
        self.zombieParticleManager.dispose() # dispose of all zombie particles
