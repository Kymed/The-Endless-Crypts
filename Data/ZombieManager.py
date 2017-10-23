import pygame
from Zombie import Zombie
from BulletManager import BulletManager
from ExplosionManager import ExplosionManager

class ZombieManager(object):

    # Call Constructor:
    def __init__(self, screenWidth, screenHeight, zombieAttackDelay, image, drawBounds):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.zombieAttackDelay = zombieAttackDelay
        self.image = image
        self.drawBounds = drawBounds

        self.zombies = [] # Array of Zombie Objects
        self.zombies_am = 0 # Amount of Zombies

        self.explosionManager = ExplosionManager() # for explosion bullets

    # Spawn a zombie method:
    def addZombie(self, spawnx, spawny, vel, health):
        self.zombies.append(Zombie(self.screenWidth, self.screenWidth, spawnx, spawny, vel, health, self.image, self.drawBounds))
        self.zombies_am += 1

    # Return the array of zombie objects:
    def getZombies(self):
        return self.zombies

    # Get zombies killed
    def getZombiesKilled(self):
        zombiesKilled = 0
        for zombie in range(len(self.zombies)):
            if self.zombies[zombie].getLifeStatus() == False:
                zombiesKilled += 1
        return zombiesKilled

    # Temporary method for testing purposes """  DELETE ME  """
    def getLatestZombieVelocity(self):
        return self.zombies[len(self.zombies) - 1].getVelocity()

    # Update Zombie Logic:
    def update(self, player, game_Clock, zombieParticleManager, dOrb_Active, dOrb_Rect):
        self.explosionManager.update(self.getZombies(), player)
        for zombie in range(self.zombies_am): # Update for all Zombies
            if self.zombies[zombie].getLifeStatus() == True: # Check if the Zombie is currently Alive before you do any relevant Data with it
                if dOrb_Active == True: pathRect = dOrb_Rect
                else: pathRect = player.getRect()
                self.zombies[zombie].update(pathRect, game_Clock, zombieParticleManager) # Update Zombie Data, give relevant data
                for i in range(self.zombies_am): # Check rect of all zombies
                    if self.zombies[i].getLifeStatus() == True: # Check if the Zombie is currently Alive before you do any relevant Data with it
                        if zombie != i: # check if the zombie isn't checking it's own zombie
                            if self.zombies[zombie].getBlockCollisionWall(1).colliderect(self.zombies[i].getCollisionRect()) == True: # If the left wall of the first-current zombie (zombie) collides with any of the other zombies (i)
                                self.zombies[zombie].translate(self.zombies[zombie].getVelocity(), 0) # Translate the zombie to the right by it's own velocity
                            if self.zombies[zombie].getBlockCollisionWall(2).colliderect(self.zombies[i].getCollisionRect()) == True: # If the right wall of the first-current zombie (zombie) collides with any of the other zombies (i)
                                self.zombies[zombie].translate(-self.zombies[zombie].getVelocity(), 0) # Translate the zombie to the left by it's own velocity
                            if self.zombies[zombie].getBlockCollisionWall(3).colliderect(self.zombies[i].getCollisionRect()) == True: # If the top wall of the first-current zombie (zombie) collides with any of the other zombies (i)
                                self.zombies[zombie].translate(0, self.zombies[zombie].getVelocity()) # Translate the zombie to the bottom by it's own velocity
                            if self.zombies[zombie].getBlockCollisionWall(4).colliderect(self.zombies[i].getCollisionRect()) == True: # If the bottom wall of the first-current zombie (zombie) collies with any of the other zombies (i)
                                self.zombies[zombie].translate(0, -self.zombies[zombie].getVelocity()) # Translate the zombie to the top by it's own velocity

    # Check if the bullet collided with any of the zombies
    def checkBulletCollision(self, soundManager, bulletX, bulletY, bulletManager, player, bloodExplosionManager, fireTileManager, bulletType, game_Clock):
        bullets = len(bulletX) # Get amount of bullets currently existing
        for zombie in range(self.zombies_am): # Run code for all existing zombies
            if self.zombies[zombie].getLifeStatus() == True: # make sure the zombie is alive before all this penetration code
                for bullet in range (bullets): # Run code for all existing bullets
                    if bulletManager.getBulletActivity(bullet) == True: # Make sure bullet collision code only happens if the bullet is active
                        bx = bulletX[bullet] - int(bulletManager.getBulletRadius(bullet) / 2) # Set the bullet X as if it was a rectangle
                        by = bulletY[bullet] - int(bulletManager.getBulletRadius(bullet) / 2) # Set the bullet Y as if it was a rectangle
                        bl = bulletManager.getBulletRadius(bullet) * 2 # Set the Width & Height (Length) of the bullet as if it was a rectangle
                        bulletRect = pygame.Rect((bx, by),(bl, bl)) # Create the Rectangle with the created Data
                        if bulletRect.colliderect(self.zombies[zombie].getRect()) == True: # Check if the bullet rectangle is colliding with the current zombie
                            soundManager.playSound("dead") # play the zombie dying sound
                            self.zombies[zombie].changeHealth(-1) # reduce the zombie's health by 1
                            if bulletType == "explosive":
                                self.explosionManager.addExplosion(bulletX[bullet], bulletY[bullet])
                            if bulletType == "flame":
                                fireTileManager.addTile(bulletX[bullet], bulletY[bullet], game_Clock)
                            player.addScore(10) # give the player 10 score
                            bloodExplosionManager.addExplosion(bulletX[bullet], bulletY[bullet])
                            if bulletType == "explosive" or bulletType == "flame":
                                bulletManager.setBulletActivity(bullet, False)
                            else:
                                newBulletX = bulletX[bullet] + (bulletManager.getSpecificBulletVector(bullet)[0] * self.zombies[zombie].getWidth()) + (bulletManager.getSpecificBulletVector(bullet)[0] * 5) # set new bullet location x
                                newBulletY = bulletY[bullet] + (bulletManager.getSpecificBulletVector(bullet)[1] * self.zombies[zombie].getHeight()) + (bulletManager.getSpecificBulletVector(bullet)[1] * 5) # set new bullet locatin y
                                bulletManager.setSpecificBulletLocation(bullet, newBulletX, newBulletY)
                                if bulletManager.getBulletRadius(bullet) >= 3: # Only allow code to pass if the radius is larger than 3.
                                    bulletManager.setBulletRadius(bullet, bulletManager.getBulletRadius(bullet) - 1) # Reduce bullet radius
                                else:
                                    bulletManager.setBulletActivity(bullet, False)

    # Check if the zombies collided with the fire tiles
    def checkFireTileCollision(self, fireTileManager, game_Clock):
        for zombie in range(self.zombies_am): # run a for loop for all existing zombies
            if self.zombies[zombie].getLifeStatus() == True: # if the zombie is alive
                for tile in range(len(fireTileManager.getTiles())): # run a for loop for all fire tiles
                    if fireTileManager.getActive(tile) == True: # if the tile is active
                        if fireTileManager.getTiles()[tile].colliderect(self.zombies[zombie].getCollisionRect()) == True: # if the current fire tile collided with the zombie
                            self.zombies[zombie].setOnFire(game_Clock) # set the zombie on fire

    # Check if the zomibes collided with the fire tiles
    def checkIceTileCollision(self, iceTileManager, game_Clock):
        for zombie in range(self.zombies_am): # run a for loop for all existing zombies
            if self.zombies[zombie].getLifeStatus() == True: # if the zombie is alive
                for tile in range(len(iceTileManager.getTiles())): # run a for loop for all ice tiles
                    if iceTileManager.getActive(tile) == True: # if the current tile is active
                        if iceTileManager.getTiles()[tile].colliderect(self.zombies[zombie].getRect()) == True: # if the ice tile collided with zombie's rectangle
                            self.getZombies()[zombie].setFrozen(True, game_Clock.getElapsedSeconds()) # set the zombie frozen


    # Tell the zombie that it has attacked for it's timer
    def setZombieAttacked(self, zombie, game_Clock):
        self.zombies[zombie].setAttackAbility(False)
        self.zombies[zombie].setAttackTimer(self.zombieAttackDelay, game_Clock.getElapsedSeconds())

    # Update the zombie in neccessary ways after the level code:
    def finalUpdate(self, playerRect, game_Clock):
        for zombie in range(self.zombies_am): # run a for loop for all existing zombies
            if self.zombies[zombie].getLifeStatus() == True: # Run code if the zombie is alive
                self.zombies[zombie].finalUpdate(playerRect, game_Clock)

    # Draw Zombies:
    def draw(self, canvas):
        for zombie in range(self.zombies_am):
            if self.zombies[zombie].getLifeStatus() == True: # Check if the zombie is currently Alive before you do any relevant Data with it
                self.zombies[zombie].draw(canvas) # draw current zombie
        self.explosionManager.draw(canvas)

    # Dispose of zombie manager:
    def dispose(self):
        for zombie in range(self.zombies_am): # run a for loop for all zombies
            self.zombies[zombie].setLifeStatus(False) # kill all zombies
            self.zombies = [] # kill array
