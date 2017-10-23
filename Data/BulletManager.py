import pygame, random
from Vector import Vec2d
from Clock import Clock
from Timer import Timer

class BulletManager(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight, notifyFont, ammo, magAmmo, reloadTime):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.bullets = 0
        self.bulletx = []
        self.bullety = []
        self.bulletv = []
        self.bullet_isActive = []
        self.bulletType = []
        self.bulletSpeed = 8
        self.bulletStartingRadius = 5
        self.bulletRadius = []
        self.bouncyBulletBounces = []

        self.reloading = False

        self.magSize = ammo # set the max ammo in a mag
        self.ammo = ammo # ammo per mag
        self.magAmmo = magAmmo # ammo in magazines
        self.magAmmoDeducted = 0 # ammo taken from magazines when reloading
        self.reloadTime = reloadTime

        self.reloadTimer = None
        self.outOfAmmo = False

        self.notifyFont = notifyFont

    # Create a bullet
    def createBullet(self, spawnx, spawny, mousex, mousey, accuracyLevel, bulletType):
        self.bulletType.append(bulletType)
        self.bullet_isActive.append(True)
        displacement = 0
        if bulletType == "spray":
            displacement = random.randint(0, 16)
        self.bulletx.append(spawnx - displacement) # Add a bullet x
        self.bullety.append(spawny - displacement) # Add a bullet y
        self.bulletRadius.append(self.bulletStartingRadius) # Add a bullet radius
        self.bouncyBulletBounces.append(0)

        if bulletType == "spray":
            _accuracyLevel = accuracyLevel + random.randint(20, 40)
        else:
            _accuracyLevel = accuracyLevel
        accuracy = random.randint(0, _accuracyLevel)
        playerVector = Vec2d(spawnx, spawny)
        directionX = random.randint(mousex - accuracy, mousex + accuracy)
        directionY = random.randint(mousey - accuracy, mousey + accuracy)
        directionVector = Vec2d(directionX, directionY)
        self.bulletv.append(Vec2d(directionVector - playerVector)) # Add a bullet vector
        self.bulletv[self.bullets] = self.bulletv[self.bullets].normalized() # normalize the vector just made to minimal length
        self.bullets += 1 # Increase bullets by 1 (for offset usage)
        self.ammo -= 1 # take away 1 ammo

    # Create a new bullet method
    def addBullet(self, spawnx, spawny, mousex, mousey, accuracyLevel, bulletType):
        if self.ammo > 0:
            if bulletType == "spray": # if the bullet type is spray
                for i in range(3): # create 3 bullets
                    self.createBullet(spawnx, spawny, mousex, mousey, accuracyLevel, bulletType)
            else:
                self.createBullet(spawnx, spawny, mousex, mousey, accuracyLevel, bulletType)

    # Return bullet array location (x)
    def getBulletLocationX(self):
        return self.bulletx # Bullet x array

    # Return bullet array location (y)
    def getBulletLocationY(self):
        return self.bullety # Bullet y array

    # Get specific location of bullet (x, y)
    def getSpecificBulletLocation(self, b):
        return (self.bulletx[b], self.bullety[b])

    # Get specific vector of bullet (v)
    def getSpecificBulletVector(self, b):
        return self.bulletv[b]

    # Set specific vector bullet (v)
    def setSpecificBulletVector(self, b, v):
        self.bulletv[b] = v

    # Flip the Y direction of a bullet
    def flipVectorY(self, b):
        vectorX = self.getSpecificBulletVector(b).x
        vectorY = self.getSpecificBulletVector(b).y
        vectorY *= -1
        vector = (vectorX, vectorY)
        self.setSpecificBulletVector(b, Vec2d(vector))

    # Flip the X direction of a bullet
    def flipVectorX(self, b):
        vectorX = self.getSpecificBulletVector(b).x
        vectorY = self.getSpecificBulletVector(b).y
        vectorX *= -1
        vector = (vectorX, vectorY)
        self.setSpecificBulletVector(b, Vec2d(vector))

    # Flip the vector
    def flipVector(self, b):
        vector = self.getSpecificBulletVector(b)
        vector *= -1
        self.setSpecificBulletVector(b, Vec2d(vector))

    # Set specific location of bullet (x, y)
    def setSpecificBulletLocation(self, b, x, y):
        self.bulletx[b] = x
        self.bullety[b] = y

    # Return bullet array radius (r)
    def getBulletRadius(self, bullet):
        return self.bulletRadius[bullet]

    # Set the radius of the bullet
    def setBulletRadius(self, bullet, radius):
        self.bulletRadius[bullet] = radius

    # Set the activity of the bullet
    def setBulletActivity(self, bullet, activity):
        self.bullet_isActive[bullet] = activity

    # Get the activity of the bullet
    def getBulletActivity(self, bullet):
        return self.bullet_isActive[bullet]

    # Get the number of bullets existing
    def getBulletAmount(self):
        return self.bullets

    # Get bullet activity
    def getBulletActivity(self, b):
        return self.bullet_isActive[b]

    # Get bullet type
    def getBulletType(self, b):
        return self.bulletType[b]

    # Get the amount of times a bouncy bullet has bounced
    def getBouncyBulletBounces(self, b):
        return self.bouncyBulletBounces[b]

    # Add a bouncy bullet bounce
    def addBouncyBulletBounce(self, b):
        self.bouncyBulletBounces[b] += 1

    # Get ammunition
    def getAmmo(self):
        return self.ammo

    # Get magazines
    def getMagazines(self):
        return self.magAmmo

    # Add magazines
    def addMagazines(self, magazines):
        self.magAmmo += self.magSize * magazines

    # Get reloading status
    def isReloading(self):
        return self.reloading

    # Lunge a bouncy bullet away from the block
    def lungeBullet(self, b):
        bulletpos = self.bulletx[b], self.bullety[b] # throw loc in tuple
        bulletpos += self.bulletv[b] * (self.bulletRadius[b] * 6) # add to the tuple via vector tuple
        self.bulletx[b], self.bullety[b] = bulletpos # unpack tuple back to original variables

    # Reload ammo
    def _reload(self, game_Clock, stringManager, soundManager):
        soundManager.playSound("reload") # play the reload sound
        self.reloadTimer = Timer(self.reloadTime, game_Clock.getElapsedSeconds()) # start the reloading timer
        self.reloading = True # notify that they are currently reloading
        if self.magAmmo >= self.magSize: # if they have enough ammo to deduct a full magazine
            self.magAmmo -= self.magSize - self.ammo # deduct 1 magazine
            self.magAmmoDeducted = self.magSize - self.ammo
        else: # if not
            self.magAmmoDeducted = self.magAmmo
            self.magAmmo = 0
        self.ammo = 0 # take away ammo just incase the player reloading with excess
        self.outOfAmmo = False # set that the player still has ammo

        # notify player through string manager that player is reloading #
        textInstance = self.notifyFont.render("Reloading!...", True, (255, 0, 0)) # for size reference
        stringManager.addText("Reloading!...", (0, 255, 0), self.notifyFont, ((self.screenWidth / 2) - (textInstance.get_width() / 2), self.screenHeight - (self.screenHeight * 0.75)), 4, -3, game_Clock)
        # notify player through string manager that player is reloading #

    # Update method:
    def update(self, game_Clock, stringManager, soundManager):
        if self.bullets > 0: # check if bullets exist
            # UPDATE BULLETS:
            for i in range(self.bullets): # for loop of all bullets
                if self.bullety[i] < -10 or self.bullety[i] > self.screenHeight + 10: #Only translate if it's within bounds
                    self.bullet_isActive[i] = False
                if self.bullet_isActive[i] == True:
                    """ Upcoming Tuple transfer. This may seem inefficient but it's like getters and setters, technically superior."""
                    bulletpos = self.bulletx[i], self.bullety[i] # throw loc in tuple
                    bulletpos += self.bulletv[i] * self.bulletSpeed # add to the tuple via vector tuple
                    self.bulletx[i], self.bullety[i] = bulletpos # unpack tuple back to original variables
                    """ This process is called a tuple transfer. Since it's safer then referencing the vector tuple by it's index"""
        # UPDATE RELOAD SYSTEM:
        if self.ammo <= 0: # if the player finished their magazine
            if self.magAmmo > 0 and self.reloading == False: # check if they have magazines left and the reload start wasn't already called
                self._reload(game_Clock, stringManager, soundManager)
            else:
                self.outOfAmmo = True # set that the player is out of ammo
        if self.reloading == True:
            if self.reloadTimer.getAlert() == True: # check if the timer finished
                self.ammo = self.magAmmoDeducted # give player ammo
                self.reloading = False # notify manager that it's finished reloading
                self.reloadTimer = None # delete timer
            else: # if the timer hasn't finished
                self.reloadTimer.update(game_Clock.getElapsedSeconds()) # update timer

    # Draw method:
    def draw(self, canvas, playerRect):
        if self.bullets > 0: # see if bullets exist
            for i in range(self.bullets): # Loop for all bullets
                if self.bullet_isActive[i] == True: # Check if the bullet is active
                    b_rect = pygame.Rect((self.bulletx[i], self.bullety[i]), (self.bulletRadius[i], self.bulletRadius[i])) # Create temporary rectangle for current bullet
                    if b_rect.colliderect(playerRect) != True: # Condition: If the bullet rect isn't overlapping player rect
                        if self.getBulletType(i) == "normal":
                            color = (0, 0, 0) # black
                        elif self.getBulletType(i) == "bouncy":
                            color = (255, 105, 180) # hot pink
                        elif self.getBulletType(i) == "explosive":
                            color = (160, 82, 45) # sienna brown
                        elif self.getBulletType(i) == "spray":
                            color = (255, 255, 0) # yellow
                        elif self.getBulletType(i) == "flame":
                            color = (255, 69, 0) # orangish red
                        pygame.draw.circle(canvas, color, (int(self.bulletx[i]), int(self.bullety[i])), self.getBulletRadius(i), 0) # Draw bullet

    # Dispose of all bullets:
    def dispose(self):
        for bullet in range(self.getBulletAmount()): # run a for loop for all bullets
            self.setBulletActivity(bullet, False) # kill all bullets
        # Kill all arrays
        self.bulletRadius = []
        self.bulletx = []
        self.bullety = []
        self.bulletv = []
        self.bullet_isActive = []
