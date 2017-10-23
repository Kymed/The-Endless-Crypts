import pygame,random

class ZombieParticleManager(object):

    # Call constructor
    def __init__(self):
        self.x = []
        self.y = []
        self.active = []
        self.color = []

        self.maxDistance = []
        self.originY = []
        self.velocity = []

    
    # Add particles
    def addParticles(self, x, y, color, distX, distY):
        particles = random.randint(3, 8)
        for particle in range(particles): # run a for loop creating the amount of particles
            _x = random.randint(int(x - distX), int(x + distX)) # randomize x spawn
            self.x.append(_x)
            _y = random.randint(int(y - distY), int(y + distY)) # randomize y spawn
            self.y.append(_y)
            
            self.color.append(color)
            self.active.append(True)
            self.originY.append(y)

            maxDistance = random.randint(int(distY), int(distY + 30)) # randomize max distance between distance given
            self.maxDistance.append(maxDistance)

            velocity = random.randint(1, 3) # randomize velocity
            self.velocity.append(velocity) # they typically fly up though

            

    # Update particles
    def update(self):
        for particle in range(len(self.x)): # run a for loop for all existing particles
            if self.active[particle] == True: # if the particle is active
                # Calculate distance reached and check if maxed:
                distance = self.originY[particle] - self.y[particle]
                if distance >= self.maxDistance[particle]: # if the particle has reached it's max distance
                    self.active[particle] = False # set the particle inactive
                else:
                    # Translate particle upwards by it's velocity:
                    self.y[particle] -= self.velocity[particle]
    
    # Draw particles
    def draw(self, canvas):
        for particle in range(len(self.x)): # run a for loop for all existing particles
            if self.active[particle] == True: # if the particle is active
                pygame.draw.rect(canvas, self.color[particle], (self.x[particle], self.y[particle], 2, 2), 0) # draw the particle
    
    # Dispose of Arrays
    def dispose(self):
        self.x = []
        self.y = []
        self.active = []
        self.color = []

        self.maxDistance = []
        self.originY = []
        self.velocity = []
        
