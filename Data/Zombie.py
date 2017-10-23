from __future__ import division # allow float point division
import pygame, math
from Vector import Vec2d
from Clock import Clock
from Timer import Timer

class Zombie(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight, spawnx, spawny, vel, health, image, drawBounds):
        # SET PARAMETER VARIABLES #
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.x = spawnx
        self.y = spawny
        self.vel = vel
        self.health = health
        self.maxHealth = health
        self.drawBounds = drawBounds
        # SET PARAMETER VARIABLES #

        # CREATE SIZE OF THE IMAGE #
        self.scaleWidth = self.screenWidth / 1280
        self.scaleHeight = self.screenHeight / 768
        self.image = image
        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scaleWidth), int(self.image.get_height() * self.scaleWidth))) # yes i know that's two scalewidths
        self.image = pygame.transform.scale(self.image, (int(self.image.get_rect().width * 0.75), int(self.image.get_rect().height * 0.75))) # rescale image
        # CREATE SIZE OF THE IMAGE #

        # SET BASIC VARIABLES #
        self.zombie = self.image
        self.isAlive = True
        self.dx = 0
        self.dy = 0
        self.Rect = pygame.Rect((self.x, self.y), (self.zombie.get_width(),self.zombie.get_height()))
        self.originalRectWidth = self.Rect.width # I keep originals because it width/height changes as the zombie rotates. Which makes the health bars look bad.
        self.originalRectHeight = self.Rect.height
        self.isFrozen = False
        self.frozenParticleTimer = None
        # SET BASIC VARIABLES #

        # ZOMBIE ATTACK SYSTEM #
        self.canAttack = True
        self.existingAttackTimer = False
        self.attackTimer = None
        # ZOMBIE ATTACK SYSTEM #

        # SET ZOMBIE-COLLISION RECTANGLES #
        self.left_Rect = pygame.Rect((self.Rect.x - 1, self.Rect.y), (1,self.Rect.height)) # Make the rect to the left of main rect
        self.right_Rect = pygame.Rect((self.Rect.x + self.Rect.width + 1, self.Rect.y), (1, self.Rect.height)) # Make the rect to the right of main rect
        self.top_Rect = pygame.Rect((self.Rect.x, self.Rect.y - 1),(self.Rect.width, 1)) # Make the rect to the top of main rect
        self.bottom_Rect = pygame.Rect((self.Rect.x, self.Rect.y + self.Rect.height), (self.Rect.width, 1)) # Make the rect to the bottom of main rect
        # SET RECTANGLES #

        # SET WALL-COLLISION RECTANGLES #
        self.colRectWidth = self.Rect.width * 0.60
        self.colRectHeight = self.Rect.height * 0.60
        self.colRectX = self.Rect.center[0] - (self.colRectWidth / 2)
        self.colRectY = self.Rect.center[1] - (self.colRectHeight / 2)
        self.col_left_Rect = pygame.Rect((self.colRectX, self.colRectY),(1, self.colRectHeight)) # left wall ( smaller for collision )
        self.col_right_Rect = pygame.Rect((self.colRectX + self.colRectWidth - 1, self.colRectY), (1, self.colRectHeight)) # right wall ( smaller for collision )
        self.col_top_Rect = pygame.Rect((self.colRectX, self.colRectY - 1),(self.colRectWidth, 1))  # top wall ( smaller for collision )
        self.col_bottom_Rect = pygame.Rect((self.colRectX, self.colRectY + self.colRectHeight - 1),(self.colRectWidth, 1)) # bottom wall ( smaller for collision )
        # SET WALL-COLLISION RECTANGLES #

        # COLLISION BOUND VARIABLES #
        self.leftWallCollided = False
        self.rightWallCollided = False
        self.topWallCollided = False
        self.bottomWallCollided = False
        # COLLISION BOUND VARIABLES #

        # HEALTH BAR #
        self.healthBarWidth = self.Rect.width
        self.healthBar = pygame.Rect((self.x, self.y - 1),(self.Rect.width, 1))
        # HEALTH BAR #

        # ON FIRE BASED DATA #
        self.onFire = False
        self.fireDamageTimer = None
        self.onFireOffTimer = None
        # ON FIRE BASED DATA #

    # Get width
    def getWidth(self):
        return self.Rect.width

    # Get height
    def getHeight(self):
        return self.Rect.height

    # Set Displacement
    def setD(self, dx, dy):
        self.dx = dx
        self.dy = dy

    # Set Displacement X
    def setDX(self, dx):
        self.dx = dx

    # Set Displacement Y
    def setDY(self, dy):
        self.dy = dy

    # Get zombie rectangle
    def getRect(self, r):
        return self.Rect

    # Get zombie collision rectangle
    def getCollisionRect(self):
        return pygame.Rect((self.colRectX, self.colRectY),(self.colRectWidth, self.colRectHeight))

    # Get zombie wall rects
    def getWall(self, wall): # wall --> (1 = left, 2 = right, 3 = top, 4 = bottom)
        if wall == 1:
            return self.left_Rect
        elif wall == 2:
            return self.right_Rect
        elif wall == 3:
            return self.top_Rect
        elif wall == 4:
            return self.bottom_Rect

    # Get zombie collision wall rects
    def getBlockCollisionWall(self, wall): # wall --> (1 = left, 2 = right, 3 = top, 4 = bottom)
        if wall == 1:
            return self.col_left_Rect
        elif wall == 2:
            return self.col_right_Rect
        elif wall == 3:
            return self.col_right_Rect
        elif wall == 4:
            return self.col_right_Rect

    # Update wall collider rectangles:
    def updateWallColliderRectangles(self):
        self.colRectWidth = self.Rect.width * 0.60
        self.colRectHeight = self.Rect.height * 0.60
        self.colRectX = self.Rect.center[0] - (self.colRectWidth / 2)
        self.colRectY = self.Rect.center[1] - (self.colRectHeight / 2)
        self.col_left_Rect = pygame.Rect((self.colRectX, self.colRectY),(1, self.colRectHeight)) # left wall ( smaller for collision )
        self.col_right_Rect = pygame.Rect((self.colRectX + self.colRectWidth - 1, self.colRectY), (1, self.colRectHeight)) # right wall ( smaller for collision )
        self.col_top_Rect = pygame.Rect((self.colRectX, self.colRectY - 1),(self.colRectWidth, 1))  # top wall ( smaller for collision )
        self.col_bottom_Rect = pygame.Rect((self.colRectX, self.colRectY + self.colRectHeight - 1),(self.colRectWidth, 1)) # bottom wall ( smaller for collision )

    # Get if a collision is bound:
    def getCollisionBound(self, wall): # wall --> (1 = left, 2 = right, 3 = top, 4 = bottom)
        if wall == 1:
            return self.leftWallCollided
        elif wall == 2:
            return self.rightWallCollided
        elif wall == 3:
            return self.topWallCollided
        elif wall == 4:
            return self.bottomWallCollided

    # Set a collision bound:
    def setCollisionBound(self, wall, _bool): # wall --> (1 = left, 2 = right, 3 = top, 4 = bottom) || _bool --> (True, False)
        if wall == 1:
            self.leftWallCollided = _bool
        elif wall == 2:
            self.rightWallCollided = _bool
        elif wall == 3:
            self.topWallCollided = _bool
        elif wall == 4:
            self.bottomWallCollided = _bool

    # Collision movement prevention:
    def checkWallCollision(self, playerRect):
        if self.leftWallCollided == True or self.rightWallCollided == True:
            self.setDX(0)
        if self.topWallCollided == True or self.bottomWallCollided == True:
            self.setDY(0)

    # Check double colliders ( prevent corner bugs )
    def checkDoubleWallCollision(self):
        if self.topWallCollided == True and self.leftWallCollided == True and self.bottomWallCollided == True and self.rightWallCollided == True: # If every wall has collided
            middleVector = Vec2d(int(self.screenWidth / 2), int(self.screenHeight / 2)) # create a vector of the screen middle
            zombieVector = Vec2d(int(self.Rect.center[0]), int(self.Rect.center[1])) # create a vector of the zombie
            zombieToMiddleVector = Vec2d(middleVector - zombieVector) # create a vector of the direction between middle and zombie
            zombieToMiddleVector = zombieToMiddleVector.normalized() # normalize to the shortest length
            zombiepos = self.x, self.y # throw zombie coordinates in a tuple so they can be adjusted via zombieToMiddleVector
            zombiepos += zombieToMiddleVector * (self.getVelocity() * 2) # translate the zombie
            self.x, self.y = zombiepos # unpack the tuple back into the x,y coordinates of the zombie

    # Set an attack timer
    def setAttackTimer(self, attackDelay, elapsedSeconds):
        self.attackTimer = Timer(attackDelay, elapsedSeconds)
        self.existingAttackTimer = True

    # Get if the zombie can attack
    def getAttackStatus(self):
        return self.canAttack

    # Set if the zombie can attack
    def setAttackAbility(self, status):
        self.canAttack = status

    # Get Zombie X
    def getX(self):
        return self.x

    # Get Zombie Y
    def getY(self):
        return self.y

    # Get Zombie Displacement X
    def getDX(self):
        return self.dx

    # Get Zombie Displacement Y
    def getDY(self):
        return self.dy

    # Get Zombie Displacement
    def getD(self):
        return (self.dx, self.dy)

    # Get Zombie Velocity
    def getVelocity(self):
        return self.vel

    # Get Zombie Rect
    def getRect(self):
        return self.Rect

    # Get Zombie life status
    def getLifeStatus(self):
        return self.isAlive

    # Set Zombie life status
    def setLifeStatus(self, status):
        self.isAlive = status

    # Translate Zombie Location
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    # Translate zombie x coordinate
    def translateX(self, dx):
        self.x += dx

    # Translate zombie y coordinate
    def translateY(self, dy):
        self.y += dy

    # Rotation Common Function:
    def rotateToAngle(self, x1, y1, x2, y2): # (x,y)1 is the coordinates to rotate too | (x,y)2 is the point your rotating too
        return 360-math.atan2(y2 - y1,x2-x1)*180/math.pi

    # Change Health Function:
    def changeHealth(self, health):
        self.health += health

    # Get zombie health
    def getHealth(self):
        return self.health

    # Set if the zombie is frozen or not
    def setFrozen(self, isFrozen, elapsedSeconds):
        self.isFrozen = isFrozen
        if self.isFrozen == True: # if the program is setting the zombie frozen (True)
            self.frozenParticleTimer = Timer(2, elapsedSeconds)

    # Get whether the zombie is frozen or not
    def getFrozen(self):
        return self.isFrozen

    # Set the zombie on fire
    def setOnFire(self, game_Clock):
        if self.onFire != True: # if the zombie isn't already on fire
            self.onFire = True
            self.fireDamageTimer = Timer(1, game_Clock.getElapsedSeconds())
            self.onFireOffTimer = Timer(4, game_Clock.getElapsedSeconds())

    # Rotate Zombie
    def rotate(self, angle):
        self.zombie = pygame.transform.rotate(self.image, angle) # Create a Transformation of the original image
        self.Rect = self.zombie.get_rect(center=(self.x, self.y)) # Recenter to the position

        """ RESET RECTANGLES """
        self.left_Rect = pygame.Rect((self.Rect.x - 1, self.Rect.y), (1,self.Rect.height)) # Make the rect to the left of main rect
        self.right_Rect = pygame.Rect((self.Rect.x + self.Rect.width + 1, self.Rect.y), (1, self.Rect.height)) # Make the rect to the right of main rect
        self.top_Rect = pygame.Rect((self.Rect.x, self.Rect.y - 1),(self.Rect.width, 1)) # Make the rect to the top of main rect
        self.bottom_Rect = pygame.Rect((self.Rect.x, self.Rect.y + self.Rect.height), (self.Rect.width, 1)) # Make the rect to the bottom of main rect
        """ RESET RECTANGLES """

    # Path zombie to player
    def pathFind(self, playerRect):
        self.setD(0, 0) # Start Displacement at 0
        if self.Rect.colliderect(playerRect) != True: # See if the zombie is not overlapping the player
            if self.x > playerRect.center[0] + 2: # see if zombie is to the right of player, add 2 to end stutter area
                self.setDX(-self.getVelocity())
            if self.x < playerRect.center[0] - 2: # see if zombie is to the left of player, subtract 2 to end stutter area
                self.setDX(self.getVelocity())
            if self.y > playerRect.center[1] + 2: # see if player is on top of zombie, add 2 to end stutter area
                self.setDY(-self.getVelocity())
            if self.y < playerRect.center[1] - 2: # see if player is under zombie , subtract 2 to end stutter area
                self.setDY(self.getVelocity())

    # Update neccessary zombie logic
    def update(self, playerRect, game_Clock, zombieParticleManager):
        """ FIND PATH TO PLAYER: """
        self.pathFind(playerRect)
        """ ROTATE ZOMBIE TO WHERE IT'S MOVING OR TO THE PLAYER IF THEY'RE OVERLAPPING """
        rotationAngle = 0 # Default it at 0
        if self.Rect.colliderect(playerRect): # check if your overlapping the player
            rotationAngle = self.rotateToAngle(self.getX(), self.getY(), playerRect.center[0], playerRect.center[1]) # rotate to player
        else:
            rotationAngle = self.rotateToAngle(self.getX(), self.getY(), self.getX() + self.dx, self.getY() + self.dy) # rotate to travel direction
        self.rotate(rotationAngle)
        """ ROTATE ZOMBIE TO WHERE IT'S MOVING OR TO THE PLAYER IF THEY'RE OVERLAPPING """

        """ CHECK IF THE ZOMBIE IS ON FIRE AND FROZEN, ACT ACCORDINGLY """
        if self.getFrozen() == True and self.onFire == True: # if the zombie is frozen and on fire
            self.setFrozen(False, game_Clock.getElapsedSeconds()) # unfreeze the zombie
            self.onFire = False # make the zombie no longer on fire
        """ CHECK IF THE ZOMBIE IS ON FIRE AND FROZEN, ACT ACCORDINGLY """

        """ IF THE ZOMBIE IS ON FIRE, UPDATE ACCORDINGLY """
        if self.onFire == True: # if the zombie is on fire
            if self.onFireOffTimer.getAlert() == True: # if the zombie is finished being on fire
                self.onFire = False # Take the zombie off being on fire
            else: # if the zombie is still on fire
                self.onFireOffTimer.update(game_Clock.getElapsedSeconds()) # update the timer to take the zombie off fire
                if self.fireDamageTimer.getAlert() == True: # if a seconds elapsed and it's time to take damage
                    self.changeHealth(-1) # lose 1 hp
                    self.fireDamageTimer = Timer(1, game_Clock.getElapsedSeconds())
                    zombieParticleManager.addParticles(self.getRect().center[0], self.getRect().center[1], (226, 88, 34), self.getWidth() / 2, self.getHeight() / 2) # spawn fire particles
                else: # if it hasn't
                    self.fireDamageTimer.update(game_Clock.getElapsedSeconds()) # update the take damage timer
        """ IF THE ZOMIBE IS ON FIRE, UPDATE ACCORDINGLY """

        """ CHECK IF THE ZOMBIE IS EVEN ALIVE """
        if self.health <= 0:
            self.setLifeStatus(False)
        """ CHECK IF THE ZOMBIE IS EVEN ALIVE """

        """ CHECK IF THE ZOMBIE CAN ATTACK """
        if self.existingAttackTimer == True:
            if self.attackTimer.getAlert() == True:
                self.existingAttackTimer = False
                self.attackTimer = None
                self.setAttackAbility(True)
            else:
                self.attackTimer.update(game_Clock.getElapsedSeconds())
                self.setAttackAbility(False)
        else:
            self.setAttackAbility(True)
        """ CHECK IF THE ZOMBIE CAN ATTACK """

        """ UPDATE HEALTH BAR """
        missingHp = float(self.getHealth() / self.maxHealth)
        self.healthBarWidth = float(self.originalRectWidth * missingHp)
        healthBarX = self.getX() - (self.originalRectWidth / 2)
        healthBarY = self.getY() - (self.originalRectHeight / 2)
        self.healthBar = pygame.Rect((int(healthBarX), int(healthBarY)),(int(self.healthBarWidth), 2))
        """ UPDATE HEALTH BAR """

        self.updateWallColliderRectangles() # Update collision rectangles for adjusted zombie

    # Update post collision logic
    def finalUpdate(self, playerRect, game_Clock):
        if self.getFrozen() == True: # if the zombie is frozen
            if self.frozenParticleTimer != None: # if a frozen particle timer exists
                if self.frozenParticleTimer.getAlert() == True: # if the frozen particle timer is finished
                    self.frozenParticleTimer = Timer(2, game_Clock.getElapsedSeconds())
                    zombieParticleManager.addParticles(self.getRect().center[0], self.getRect().center[1], (0, 191, 255), self.getWidth() / 2, self.getHeight() / 2) # spawn ice particles
            else:
                self.frozenParticleTimer = Timer(2, game_Clock.getElapsedSeconds()) # set a timer
        else: # if not
            self.translate(self.dx, self.dy) # Translate zombie

        """ ROTATE ZOMBIE TO WHERE IT'S MOVING OR TO THE PLAYER IF THEY'RE OVERLAPPING """
        rotationAngle = 0 # Default it at 0
        if self.Rect.colliderect(playerRect): # check if your overlapping the player
            rotationAngle = self.rotateToAngle(self.getX(), self.getY(), playerRect.center[0], playerRect.center[1]) # rotate to player
        else:
            rotationAngle = self.rotateToAngle(self.getX(), self.getY(), self.getX() + self.dx, self.getY() + self.dy) # rotate to travel direction
        self.rotate(rotationAngle)
        """ ROTATE ZOMBIE TO WHERE IT'S MOVING OR TO THE PLAYER IF THEY'RE OVERLAPPING """

    # Draw the zombie
    def draw(self, canvas):
        canvas.blit(self.zombie, self.getRect())
        if self.maxHealth > 1: # draw the health bar if it actually has health
            pygame.draw.rect(canvas, (255, 0, 0), self.healthBar, 0) # draw the health bar
        if self.drawBounds == True:
            boundColor = (255, 50, 50)
            pygame.draw.rect(canvas, boundColor, self.col_left_Rect, 1)
            pygame.draw.rect(canvas, boundColor, self.col_right_Rect, 1)
            pygame.draw.rect(canvas, boundColor, self.col_top_Rect, 1)
            pygame.draw.rect(canvas, boundColor, self.col_bottom_Rect, 1)
