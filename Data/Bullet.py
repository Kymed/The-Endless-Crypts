import pygame

class Bullet(object):

    # Initalize a bullet
    def __init__(self, spawnx, spawny, radius):
        self.x = spawnx
        self.y = spawny
        self.radius = radius

    def update(self, displacement):
        self.x += displacement[0]
        self.y += displacement[1]

    def draw(self, canvas, color):
        pygame.draw.circle(canvas, color, (self.x, self.y), self.radius, 0)
    
