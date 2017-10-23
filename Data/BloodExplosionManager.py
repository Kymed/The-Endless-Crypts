import pygame, random
from Vector import Vec2d

class BloodExplosionManager(object):

    # Call Consturctor:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        
        self.x = []
        self.y = []
        self.active = []

        self.vector = []
        self.velocity = []
        self.maxLength = []
        self.length = []
        self.red = []

    # Get number of particles
    def getLength(self):
        return len(self.x)
    
    # Get X array
    def getX(self, particle):
        return self.x[particle]

    # Get Y array
    def getY(self, particle):
        return self.y[particle]

    # Get particle active
    def getParticleActive(self, particle):
        return self.active[particle]

    # Set particle active
    def setParticleActive(self, particle, status):
        self.active[particle] = status
    
    # Add blood explosion:
    def addExplosion(self, x, y):
        chanceForHugeExplosion = random.randint(1, 30)
        if chanceForHugeExplosion == 1: # 3%(roughly) chance for a huge particle explosion
            bloodParticles = 100 # spawn 200 blood particles
        else: # failed the 5 % chance, normal amounts of particles
            bloodParticles = random.randint(6, 16) # randomize how many blood particles spawn
        for i in range(bloodParticles):
            self.x.append(int(x)) # Pass X
            self.y.append(int(y)) # Pass Y
            self.active.append(True) # start the explosion as active
            
            x2 = random.randint(0, self.screenWidth) # random x for vector
            y2 = random.randint(0, self.screenHeight) # random y for vector
            dv = Vec2d(x2,y2) # set random point as a vector
            pv = Vec2d(x,y) # set the vector of current pos

            v = Vec2d(dv - pv) # create the vector
            v = v.normalized() # normalize the vector
            self.vector.append(v) # add the new vector

            vel = random.randint(1, 10) # randomize velocity
            self.velocity.append(vel) # append the new velocity

            maxLength = random.randint(17 * vel, 36 * vel) # randomize how long they will travel
            self.maxLength.append(maxLength) # append the new length max
            self.length.append(0) # append the new length traveled
            
            red = random.randint(50, 190) # random dark red for the explosion
            red = (red, 0, 0)
            self.red.append(red) # add the new red

    # Update blood explosions:
    def update(self):
        for particle in range(len(self.vector)): # run a for loop for all particles
            if self.active[particle] == True and self.length[particle] < self.maxLength[particle]: # if the particle is active
                self.length[particle] += self.velocity[particle] # add to the length
                vector = self.vector[particle] # unpack tuple vector from the array
                self.x[particle] += vector[0] * self.velocity[particle] # translate the x pos by the vector * it's velocity
                self.y[particle] += vector[1] * self.velocity[particle] # translate the y pos by the vector * it's velocity
                self.x[particle] = int(self.x[particle]) # cast to an int just in case that the multiplication produced a float point num
                self.y[particle] = int(self.y[particle]) # cast to an int just in case that the multiplication produced a float point num
            else:
                self.active[particle] = False

    # Draw blood explosions:
    def draw(self, canvas):
        for particle in range(len(self.vector)): # run a for loop for all explosions
            if self.active[particle] == True: # if the explosion is active
                pygame.draw.circle(canvas, self.red[particle], (self.x[particle], self.y[particle]), 2, 0)

    # Dispose of all arrays:
    def dispose(self):
        self.x = []
        self.y = []
        self.active = []
        self.length = []
        self.vector = []
        self.velocity = []
        self.maxLength = []
        self.red = []
