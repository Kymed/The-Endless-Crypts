from __future__ import division
import pygame, math
from Zombie import Zombie

class Explosion(object):
    
    # Call constructor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 1
        self.a = True
        self.zombiesDamaged = []

    # Get activity
    def getActive(self):
        return self.a

    # Set activity
    def setActive(self, a):
        self.a = a

    # Get x
    def getX(self):
        return self.x

    # Get y
    def getY(self):
        return self.y

    # Get radius
    def getRadius(self):
        return self.r

    # Set radius
    def setRadius(self, r):
        self.r = r
            
    # Update
    def update(self, zombies, player):
        self.setRadius(self.getRadius() + 12) # increase radius by 3
        if self.getRadius() > 180: # if the radius reached it's maximum length
            self.setActive(False) # set it inactive
        for zombie in range(len(zombies)):
            if zombies[zombie].getLifeStatus() == True: # if the zombie is alive
                checkCollision = True
                for i in range(len(self.zombiesDamaged)):
                    if zombie == self.zombiesDamaged[i]:
                        checkCollision = False
                if checkCollision == True:
                    zombiex = zombies[zombie].getRect().center[0]
                    zombiey = zombies[zombie].getRect().center[1]
                    zombier = (zombies[zombie].getRect().width + zombies[zombie].getRect().height) / 2
                    differencex = self.getX() - zombiex
                    differencey = self.getY() - zombiey
                    distance = math.sqrt((differencex * differencex) + (differencey * differencey))

                    if distance < self.getRadius() + zombier: # if their distance is shorter than their combined radiuses
                        zombies[zombie].changeHealth(-1)
                        player.addScore(1) #  give the player 1 score
                        self.zombiesDamaged.append(zombie)
                   

    # Draw
    def draw(self, canvas):
        pygame.draw.circle(canvas, (255, 0, 0), (int(self.getX()), int(self.getY())), int(self.getRadius()), 1)
        

class ExplosionManager(object):

    # Call constructor
    def __init__(self):
        self.explosions = []

    # Add explosion
    def addExplosion(self, spawnx, spawny):
        self.explosions.append(Explosion(spawnx, spawny))

    # Update explosions
    def update(self, zombies, player):
        for explosion in range(len(self.explosions)):
            if self.explosions[explosion].getActive() == True:
                self.explosions[explosion].update(zombies, player)
                
    # Draw explosion
    def draw(self, canvas):
        for explosion in range(len(self.explosions)):
            if self.explosions[explosion].getActive() == True:
                self.explosions[explosion].draw(canvas)
