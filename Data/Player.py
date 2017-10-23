from __future__ import division # allow float point division
import pygame, math
from Vector import Vec2d
import os

class Player(object):

    # Initalize Player:
    def __init__(self, screenWidth, screenHeight, name, image, spawnx, spawny, startingHealth, stamina, fps, drawBounds):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.scaleWidth = self.screenWidth / 1280
        self.scaleHeight = self.screenHeight / 768

        if self.scaleWidth != 1 or self.scaleHeight != 1:
            self.image = pygame.transform.scale(image, (int(image.get_width() * self.scaleWidth), int(image.get_height() * self.scaleWidth)))
        else:
            self.image = image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_rect().width * 0.75), int(self.image.get_rect().height * 0.75))) # rescale image
        self.x = spawnx
        self.y = spawny
        self.dx = 0
        self.dy = 0
        self.health = startingHealth
        self.maxHealth = self.health # set the full health as reference as it changes
        self.isAlive = True
        self.vel = 6

        self.mousex = self.mousey = 0

        self.drawBounds = drawBounds
        self.player = self.image # The reason we use this is because we draw the player because image is going to be rotated. We need self.image untouched to be rotated and be saved as self.player

        # Set player rectangles:
        self.playerRect = self.player.get_rect(center=(self.x, self.y))
        self.originalWidth = self.playerRect.width # Because it changes as the player rotate, making name plate display unsmooth
        self.originalHeight = self.playerRect.height # Same thing for height, getting the original/normal rectangle height
        self.colRectWidth = self.playerRect.width * 0.50
        self.colRectHeight = self.playerRect.height * 0.50
        self.colRectX = self.playerRect.center[0] - (self.colRectWidth / 2)
        self.colRectY = self.playerRect.center[1] - (self.colRectHeight / 2)
        self.left_Rect = pygame.Rect((self.colRectX, self.colRectY),(1, self.colRectHeight)) # left wall ( smaller for collision )
        self.right_Rect = pygame.Rect((self.colRectX + self.colRectWidth - 1, self.colRectY), (1, self.colRectHeight)) # right wall ( smaller for collision )
        self.top_Rect = pygame.Rect((self.colRectX, self.colRectY - 1),(self.colRectWidth, 1))  # top wall ( smaller for collision )
        self.bottom_Rect = pygame.Rect((self.colRectX, self.colRectY + self.colRectHeight - 1),(self.colRectWidth, 1)) # bottom wall ( smaller for collision )


        # COLLISION BOUND VARIABLES #
        self.leftWallCollided = False
        self.rightWallCollided = False
        self.topWallCollided = False
        self.bottomWallCollided = False
        # COLLISION BOUND VARIABLES #

        # SCORE #
        self.score = 0
        self.totalScore = 0
        # SCORE #

        # RUNNING #
        self.agility = 1.30
        self.isRunning = False
        self.canRun = True
        self.stamina = stamina * fps
        self.maxStamina = self.stamina
        # RUNNING #

        # NAME PLATE #
        self.name = name
        self.toggleNamePlate = True
        self.nameFont = pygame.font.SysFont("Verdana", 12)
        self.nameRender = self.nameFont.render(self.name, True, (255, 255, 255))
        # NAME PLATE #

    # Set the name of the player
    def setName(self, name):
        self.name = name
        self.nameRender = self.nameFont.render(self.name, True, (255, 255, 255))

    # Get the name of the player
    def getName(self):
        return self.name

    # Get player agility
    def getAgility(self):
        return self.agility

    # Set player agility
    def setAgility(self, agility):
        self.agility = agility

    # Add player agility
    def addAgility(self, agility):
        self.agility += agility

    # Get max player stamina
    def getMaxStamina(self):
        return self.maxStamina

    # Set player stamina
    def setStamina(self, stamina):
        self.stamina = stamina

    # Get player stamina
    def getStamina(self):
        return self.stamina

    # Add player stamina
    def addStamina(self, stamina):
        self.stamina += stamina

    # Get player health
    def getHealth(self):
        return self.health

    # Set player health
    def setHealth(self, health):
        self.health = health

    # give player health
    def giveHealth(self, health):
        self.health += health

    # Get max health
    def getMaxHealth(self):
        return self.maxHealth

    # Set max health
    def setMaxHealth(self, maxHealth):
        self.maxHealth = maxHealth

    # Add player max hp
    def addMaxHealth(self, health):
        self.maxHealth += 1
        self.health += 1

    # Get missing health
    def getMissingHealth(self):
        return self.getHealth() / self.getMaxHealth()

    # Get missing stamina
    def getMissingStamina(self):
        return self.stamina / self.maxStamina

    # Set score
    def setScore(self, score):
        self.score = score

    # Add score
    def addScore(self, score):
        self.score += score
        self.totalScore += score

    # Take score away
    def delScore(self, score):
        self.score -= score

    # Get score
    def getScore(self):
        return self.score

    # Get total score
    def getTotalScore(self):
        return self.totalScore

    # Set DX Method:
    def setDX(self, dx):
        self.dx = dx

    # Set DY Method:
    def setDY(self, dy):
        self.dy = dy

    # Set displacement method:
    def setD(self, dx, dy):
        self.dx = dx
        self.dy = dy

    # Get DX Method:
    def getDX(self):
        return self.dx

    # Get DY Method:
    def getDY(self):
        return self.dy

    # Translate Player:
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    # Get rotate angle function
    def rotateToAngle(self, x1, y1, x2, y2): # (x,y)1 is the coordinates to rotate too | (x,y)2 is the point your rotating too
        return 360-math.atan2(y2 - y1,x2-x1)*180/math.pi

    # Get if the player is running
    def getRunningStatus(self):
        return self.isRunning

    # Toggle the name plate on/off
    def toggleName(self):
        if self.toggleNamePlate == True:
            self.toggleNamePlate = False
        else:
            self.toggleNamePlate = True

    # Event code method:
    def passEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.isRunning = True
            if event.key == pygame.K_e:
                self.toggleName()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.isRunning = False
        if event.type == pygame.MOUSEMOTION:
            self.mousex, self.mousey = event.pos

    # Rotate Player:
    def rotate(self, angle):
        self.player = pygame.transform.rotate(image, angle) # Rotate the original image and set that to the image used to be drawn
        self.playerRect = self.player.get_rect(center=(self.x, self.y)) # Recenter the player rectangle

    # Set player x:
    def setX(self, x):
        self.x = x

    # Set player y :
    def setY(self, y):
        self.y = y

    # Get player x:
    def getX(self):
        return self.x

    # Get player y
    def getY(self):
        return self.y

    # Set player velocity:
    def setVelocity(self, vel):
        self.vel = vel

    # Get player velocity:
    def getVelocity(self):
        return self.vel

    # Get player rectangle:
    def getRect(self):
        return self.playerRect

    # Get player collision rectangle:
    def getCollisionRect(self):
        return pygame.Rect((self.colRectX, self.colRectY),(self.colRectWidth, self.colRectHeight))

    # Get player width:
    def getWidth(self):
        return self.playerRect.width

    # Get player height:
    def getHeight(self):
        return self.playerRect.height

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

    # Get player wall rects
    def getWall(self, wall): # wall --> (1 = left, 2 = right, 3 = top, 4 = bottom)
        if wall == 1:
            return self.left_Rect
        elif wall == 2:
            return self.right_Rect
        elif wall == 3:
            return self.top_Rect
        elif wall == 4:
            return self.bottom_Rect

    # Collision movement prevention:
    def checkWallCollision(self, sprintScale):
        if self.topWallCollided == True: # if his top wall has collided with a wall
            self.y += self.getVelocity() * sprintScale # have the player go down by it's velocity
        if self.bottomWallCollided == True: # if the bottom wall has collided with a wall
            self.y -= self.getVelocity() * sprintScale # have the player go up by it's velocity
        if self.leftWallCollided == True: # if the left wall has collided with a wall
            self.x += self.getVelocity() * sprintScale # have the player go right by it's velocity
        if self.rightWallCollided == True: # if the right wall has collided with a wall
            self.x -= self.getVelocity() * sprintScale # have the player go left by it's velocity

    # Check double colliders ( prevent corner bugs )
    def checkDoubleWallCollision(self):
        if self.topWallCollided == True and self.leftWallCollided == True and self.bottomWallCollided == True and self.rightWallCollided == True: # If every wall has collided
            middleVector = Vec2d(int(self.screenWidth / 2), int(self.screenHeight / 2)) # create a vector of the screen middle
            playerVector = Vec2d(int(self.playerRect.center[0]), int(self.playerRect.center[1])) # create a vector of the player
            playerToMiddleVector = Vec2d(middleVector - playerVector) # create a vector of the direction between middle and player
            playerToMiddleVector = playerToMiddleVector.normalized() # normalize to the shortest length
            playerpos = self.x, self.y # throw player coordinates in a tuple so they can be adjusted via playerToMiddleVector
            playerpos += playerToMiddleVector * (self.getVelocity() * 2) # translate the player
            self.x, self.y = playerpos # unpack the tuple back into the x,y coordinates of the player

    # Update player collision walls method:
    def updateCollisionWalls(self):
        # WIDTH, HEIGHT, X, Y changes as player rotates so these numbers must be updated
        self.colRectWidth = self.playerRect.width * 0.50
        self.colRectHeight = self.playerRect.height * 0.50
        self.colRectX = self.playerRect.center[0] - (self.colRectWidth / 2)
        self.colRectY = self.playerRect.center[1] - (self.colRectHeight / 2)
        self.left_Rect = pygame.Rect((self.colRectX, self.colRectY),(1, self.colRectHeight)) # left wall ( smaller for collision )
        self.right_Rect = pygame.Rect((self.colRectX + self.colRectWidth - 1, self.colRectY), (1, self.colRectHeight)) # right wall ( smaller for collision )
        self.top_Rect = pygame.Rect((self.colRectX, self.colRectY - 1),(self.colRectWidth, 1))  # top wall ( smaller for collision )
        self.bottom_Rect = pygame.Rect((self.colRectX, self.colRectY + self.colRectHeight - 1),(self.colRectWidth, 1))

    # Check if the player is alive
    def getLifeStatus(self):
         return self.isAlive

    # Set if the player is alive or not
    def setLifeStatus(self, status):
        self.isAlive = status

    # Check exterior collision (If the player is leaving screen)
    def checkExteriorCollision(self, sprintScale):
        if self.getRect().midright[0] > self.screenWidth: # if the player's mid right x point is leaving the right side of the screen
            self.translate(-self.getVelocity() * sprintScale, 0) # translate him away by his velocity * sprint Scale
        if self.getRect().midleft[0] < 0: # if the player's mid left x is leaving the left side of the screen
            self.translate(self.getVelocity() * sprintScale, 0) # translate him away by his velocity * sprint Scale
        if self.getRect().midbottom[1] > self.screenHeight: # if the player's mid bottom y point is leaving the bottom of the screen
            self.translate(0, -self.getVelocity() * sprintScale) # translate him away by his velocity * sprint Scale
        if self.getRect().midtop[1] < 0: # if the player's mid top y point is leaving the top side of the screen
            self.translate(0, self.getVelocity() * sprintScale) # translate him away by his velocity * sprint Scale

    # Update code
    def update(self, mx, my):

        """ GET KEYPRESSED INPUT TO SMOOTHEN CHARACTER MOVEMENT """
        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_w]: self.setDY(-self.getVelocity())
        if keysPressed[pygame.K_s]: self.setDY(self.getVelocity())
        if keysPressed[pygame.K_w] and keysPressed[pygame.K_s]:
            self.setDY(0)
        if keysPressed[pygame.K_a]: self.setDX(-self.getVelocity())
        if keysPressed[pygame.K_d]: self.setDX(self.getVelocity())
        if keysPressed[pygame.K_a] and keysPressed[pygame.K_d]:
            self.setDX(0)

        if keysPressed[pygame.K_w] != True and keysPressed[pygame.K_s] != True:
            self.setDY(0)
        if keysPressed[pygame.K_a] != True and keysPressed[pygame.K_d] != True:
            self.setDX(0)
        """ GET KEYPRESSED INPUT TO SMOOTHEN CHARACTER MOVEMENT """

        self.playerRotateAngle = self.rotateToAngle(self.x, self.y, mx, my) # get the angle from player to mouse
        self.player = pygame.transform.rotate(self.image, self.playerRotateAngle) # rotate the player with the angle

        """ UPDATE PLAYER RECTANGLES """
        self.playerRect = self.player.get_rect(center=(self.x, self.y)) # reset the player rect so the player doesn't move as it rotates
        self.updateCollisionWalls() # Update collision rectangle as player rectangle changes
        """ UPDATE PLAYER RECTANGLES """

        """ CHECK IF THE PLAYER IS DEAD """
        if self.getHealth() <= 0:
            self.setLifeStatus(False)
        """ CHECK IF THE PLAYER IS DEAD """

        """ CHECK IF THE PLAYER IS RUNNING """
        ranThisFrame = False
        if self.getRunningStatus() == True and self.stamina > 0 and self.dx != 0:
            dx = self.dx * self.getAgility() # make a new instance of the variable so it doesn't keep adding
            self.addStamina(-2)
            ranThisFrame = True
        else:
            dx = self.dx
        if self.getRunningStatus() == True and self.stamina > 1 and self.dy != 0:
            dy = self.dy * self.getAgility() # make a new instance of the variable so it doesn't keep adding
            if ranThisFrame == False:
                self.addStamina(-2)
                ranThisFrame = True
        else:
            dy = self.dy
        if self.getStamina() < self.getMaxStamina() and self.getRunningStatus() == False:
            self.addStamina(1)
        """ CHECK IF THE PLAYER IS RUNNING """

        """ CHECK EXTERIOR COLLISION """
        if self.getRunningStatus() == True: # check if the player is running
            self.checkExteriorCollision(self.agility) # check if the player is going off screen, give the sprint scale
        else:
            self.checkExteriorCollision(1) # check if the player is going off screen, normal scale
        """ CHECK EXTERIOR COLLISION """

        """ CHECK WALL COLLISION """
        if self.getRunningStatus() == True:
            self.checkWallCollision(self.agility) # end directions of travel and adjust positions if he's colliding with a wall
        else:
            self.checkWallCollision(1) # end directions of travel and adjust positions but without the extended sprint velocity
        """ CHECK WALL COLLISION """

        self.translate(dx, dy) # translate the player by final displacement

    # Draw code
    def draw(self, canvas):
        canvas.blit(self.player, self.playerRect)
        if self.toggleNamePlate == True:
            canvas.blit(self.nameRender, (self.getX() - (self.nameRender.get_width() / 2),self.getY() - (self.originalHeight / 2) - self.nameRender.get_height()))
        if self.drawBounds == True: # Check if developer tools (draw collision box) is on
            boundColor = (25, 0, 255) # set a color for the box
            boundColor2 = (0, 255, 25) # set a color for main box
            pygame.draw.rect(canvas, boundColor2, self.playerRect, 1) # draw player rect
            pygame.draw.rect(canvas, boundColor, self.left_Rect, 1) # draw col box
            pygame.draw.rect(canvas, boundColor, self.right_Rect, 1) # draw col box
            pygame.draw.rect(canvas, boundColor, self.top_Rect, 1) # draw col box
            pygame.draw.rect(canvas, boundColor, self.bottom_Rect, 1) # draw col box
