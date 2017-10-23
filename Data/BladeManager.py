import pygame
from Clock import Clock
from Timer import Timer

class Blade(object):

    # Call constructor
    def __init__(self, rect, image, timeLength, secondsElapsed):
        self.Rect = rect
        
        self.image = image
        self.texture = self.image #self.texture is the transform of self.image
        
        self.rotation = 0
        self.rotationVel = 12

        self.active = True
        self.existenceTimer = Timer(timeLength, secondsElapsed)
        self.zombiesDamaged = []
        self.zombiesDamagedTimer = []

    # Get if the blade is active
    def getActive(self):
        return self.active

    # Set if the blade is active
    def setActive(self, activity):
        self.active = activity

    # Get the rectangle
    def getRect(self):
        return self.Rect

    # Set the rectangle
    def setRect(self, rect):
        self.Rect = rect

    # Check if you can attack a zombie
    def canAttack(self, zombie, secondsElapsed):
        for attackedZombie in range(len(self.zombiesDamaged)): # run a for loop for all attacked zombies
            if self.zombiesDamaged[attackedZombie] == zombie: # if the current attacked zombie is the current zombie
                for currentTimer in range(len(self.zombiesDamagedTimer)): # run a for loop for all zombie attack timers
                    timer = self.zombiesDamagedTimer[currentTimer] # unpack tuple
                    if timer[0] == zombie: # if the timer is assigned for this current zombie
                        break # end the timer for loop
                    timer = None # if it's reached this point than the zombie has no timer
                if timer != None: # if a timer was found
                    if timer[1].getAlert() == True: # if it's attack timer has finished
                        return True # say it can attack
                    else:
                        timer[1].update(secondsElapsed) # update the timer
                        return False # say it can't attack
        return True # if it's gotten to this point, it has no timer therefore can attack

    # Update the blade
    def update(self, zombies, player, game_Clock):
        if self.existenceTimer.getAlert() == True: # if the blade is finished
            self.setActive(False) # Set the blade inactive
        else: # UPDATE BLADE:
            self.existenceTimer.update(game_Clock.getElapsedSeconds()) # update existence timer
            # Rotate blade:
            self.rotation += self.rotationVel
            self.texture = pygame.transform.rotate(self.image, self.rotation)
            self.setRect(self.texture.get_rect(center=(self.getRect().center))) # Center blade
            
            # Check collision with zombies:
            for zombie in range(len(zombies)): # run a for loop for all zombies
                if zombies[zombie].getLifeStatus() == True: # check if the zombie is active
                    if self.Rect.colliderect(zombies[zombie].getRect()) == True and self.canAttack(zombie, game_Clock.getElapsedSeconds()) == True: # if the blade collides with the zombie and can attack it
                        zombies[zombie].changeHealth(-2)
                        player.addScore(2) # give the player 2 score
                        self.zombiesDamaged.append(zombie)
                        self.zombiesDamagedTimer.append((zombie, Timer(1, game_Clock.getElapsedSeconds()))) # set a timer for when the blade can attack the zombie again

    # Draw the blade
    def draw(self, canvas):
        canvas.blit(self.texture, self.getRect()) # draw blade with rotation
        

class BladeManager(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight, tileWidth, tileHeight, image):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.image = pygame.transform.scale(image, (self.tileWidth / 2, self.tileHeight / 2)) # scale to fit a tile

        self.blades = []

    # Add blade
    def addBlade(self, mousex, mousey, game_Clock):
        for i in range(int(self.screenHeight / self.tileHeight)): # run a for loop for all tiles on the y axis
            for z in range(int(self.screenWidth / self.tileWidth)): # run a for loop for all tiles on the x axis
                currentTile = pygame.Rect((z * self.tileWidth, i * self.tileHeight), (self.tileWidth, self.tileHeight)) # generate the current tile
                if currentTile.collidepoint(mousex, mousey) == True: # if the mouse point lands on the current tile
                    self.blades.append(Blade(currentTile, self.image, 8, game_Clock.getElapsedSeconds())) # add a new blade

    # Update blades
    def update(self, zombies, player, game_Clock):
        for blade in range(len(self.blades)): # run a for loop for all blades
            if self.blades[blade].getActive() == True: # if the blade is active
                self.blades[blade].update(zombies, player, game_Clock) # update the blade

    # Draw blades
    def draw(self, canvas):
        for blade in range(len(self.blades)): # run a for loop for all blades
            if self.blades[blade].getActive() == True: # if the blade is active
                self.blades[blade].draw(canvas) # draw
