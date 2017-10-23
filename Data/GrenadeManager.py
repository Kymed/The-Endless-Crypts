import pygame, math
from Vector import Vec2d

class Grenade(object):

    # Call constructor
    def __init__(self, x, y, width, height, vector, velocity, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.Rect = pygame.Rect((self.x, self.y),(self.width, self.height))

        self.vector = vector
        self.velocity = velocity
        self.rotateSpeed = 6
        self.rotation = 0

        if self.vector < 0: # if the grenade will be heading left
            self.rotateVel = -self.rotateSpeed # rotate counter clock wise
        else: # if it will be heading right
            self.rotateVel = self.rotateSpeed # rotate clock wise

        self.image = image
        self.texture = image # to use 'self.image' to rotate and save to self.texture, that way it doesn't move from rotation

    # Get rectangle
    def getRect(self):
        return self.Rect
    
    # Update
    def update(self):
        pos = self.x, self.y # pack position into a tuple
        pos += self.vector * self.velocity # use tuple to translate grenade
        self.x, self.y = pos # unpack tuple back into pos
        self.Rect = pygame.Rect((self.x, self.y),(self.width, self.height)) # reload rect with new pos
        self.rotation += self.rotateVel
        self.texture = pygame.transform.rotate(self.image, self.rotation) # rotate image

    # Draw
    def draw(self, canvas):
        canvas.blit(self.texture, self.Rect)

class GrenadeManager(object):

    # Call constructor
    def __init__(self, tileWidth, tileHeight, image):
        self.width = int(tileWidth / 3)
        self.height = int(tileHeight / 3)

        self.grenades = []
        self.activeGrenades = []
        self.image = pygame.transform.scale(image, (self.width, self.height)) # load image & scale to half a tile size

    # Add a grenade
    def addGrenade(self, x, y, mousex, mousey):
        # Create vector:
        posVector = Vec2d(x, y)
        mouseVector = Vec2d(mousex, mousey)
        vector = Vec2d(mouseVector - posVector)
        vector = vector.normalized()

        # Create grenade:
        self.activeGrenades.append(True)
        self.grenades.append(Grenade(x, y, self.width, self.height, vector, 6, self.image))

    # Explode the grenade and check what zombies it hit
    def explode(self, grenade, zombies, player):
        self.activeGrenades[grenade] = False # set the grenade inactive

        # Check collision with all zombies:
        grenadeMidX = self.grenades[grenade].getRect().center[0] # get grenade center x
        grenadeMidY = self.grenades[grenade].getRect().center[1] # get grenade center y
        grenadeRadius = self.width * 6 # explosion radius is 2 tiles in length ( width is 1/3 length of a tile )
        grenadeRadius = int(grenadeRadius) # cast to an int just incase a float was generated through division
        for zombie in range(len(zombies)): # run a for loop for all zombies
            if zombies[zombie].getLifeStatus() == True: # if the zombie is currently alive
                zombiex = zombies[zombie].getRect().center[0] # get zombie center x
                zombiey = zombies[zombie].getRect().center[1] # get zombie center y
                zombier = int((zombies[zombie].getRect().width + zombies[zombie].getRect().height) / 2) # get zombie avg length
                differencex = grenadeMidX - zombiex
                differencey = grenadeMidY - zombiey
                distance = math.sqrt((differencex * differencex) + (differencey * differencey))

                if distance < grenadeRadius + zombier: # if their distance is shorter than their combined radiuses
                    zombies[zombie].changeHealth(-3)
                    player.addScore(5) #  give the player 1 score

    # Update grenades
    def update(self, blocks, zombies, player):
        for grenade in range(len(self.grenades)): # run a for loop for all grenades
            if self.activeGrenades[grenade] == True: # if the grenade is active
                self.grenades[grenade].update() # Update grenade

                # Check collision with blocks
                for block in range(len(blocks)): # run a for loop for all blocks
                    if self.grenades[grenade].getRect().colliderect(blocks[block]) == True: # check if the current grenade collided with the current block
                        self.explode(grenade, zombies, player)
                        break # end loop

                # Check collision with zombies
                for zombie in range(len(zombies)):
                    if zombies[zombie].getLifeStatus() == True: # if the zombie is alive
                        if self.grenades[grenade].getRect().colliderect(zombies[zombie].getRect()) == True: # if the current grenade collided with the current zombie
                            self.explode(grenade, zombies, player)
                            break # end loop

    # Draw grenades
    def draw(self, canvas):
        for grenade in range(len(self.grenades)): # run a for loop for all grenades
            if self.activeGrenades[grenade] == True: # if the current grenade is active
                self.grenades[grenade].draw(canvas) # draw the grenade










            
        
