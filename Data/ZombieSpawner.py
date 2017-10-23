import pygame, random
from ZombieManager import ZombieManager
from Clock import Clock
from Timer import Timer

class ZombieSpawner(object):

    # Call Constructor
    def __init__(self, x, y, zombieManager, maxZombies, spawnTimeMin, spawnTimeMax, minVel, maxVel, hp):
        self.x = x
        self.y = y
        self.zombieManager = zombieManager

        self.maxZombies = maxZombies
        self.zombiesSpawned = 0

        self.spawnTimeMin = spawnTimeMin
        self.spawnTimeMax = spawnTimeMax

        self.minVel = minVel
        self.maxVel = maxVel
        self.hp = hp

        self.spawnZombie = False
        self.zombieSpawned = True

        self.firstZombieSpawned = False

        self.spawnerActive = True

    # Get spawner location x
    def getX(self):
        return self.x

    # Get spawner location y
    def getY(self):
        return self.y

    # Get activity
    def getActive(self):
        return self.spawnerActive
    
    # Get amount of zombies spawner has spawned:
    def getZombiesSpawned(self):
        return self.zombiesSpawned
    
    # Spawn Zombie
    def spawn(self):
        self.zombieSpawned = False # say the zombie hasnt spawned yet
        vel = random.randint(self.minVel, self.maxVel)
        self.zombieManager.addZombie(self.x, self.y, vel, self.hp)
        self.zombiesSpawned += 1
        self.zombieSpawned = True

    # Begin Timer
    def begin(self, game_clock):
        self.timeTillNextZombie = random.randint(self.spawnTimeMin, self.spawnTimeMax) # get the time till get a next zombie
        self.timer = Timer(self.timeTillNextZombie, game_clock.getElapsedSeconds()) # begin the timer, at the length of the var above and give the currents seconds elapsed
        
    # Manage Zombies
    def update(self, game_clock):
        if self.spawnerActive == True:
            if self.zombiesSpawned <= self.maxZombies:
                if self.firstZombieSpawned == False: # Check if the first zombie has spawned
                    self.firstZombieSpawned = True # Say that the first zombie has spawned
                    self.spawn() # spawn the first zombie
                if self.zombieSpawned == True: # check if a zombie has finished spawning
                    self.zombieSpawned = False # turn it off to reduce spam
                    self.begin(game_clock) # begin a timer for the next zombie
                self.timer.update(game_clock.getElapsedSeconds()) # Update the timer, give the elapsed seconds in the _internal.gameclock
                if self.timer.getAlert() == True: # check if the timer finished
                    self.spawn() # spawn a new zombie
            else:
                self.spawnerActive = False

    # Dispose of spawner
    def dispose(self):
        self.spawnerActive = False
        
        

        
        

        
        
        
