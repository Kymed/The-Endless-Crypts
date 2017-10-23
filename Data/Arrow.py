import pygame, math

class Arrow(object):

    # Call Constructor
    def __init__(self, image, centerx, centery, rotation, bounceDirection, bounceLength):
        self.image = pygame.transform.rotate(image, rotation)
        self.x = centerx
        self.y = centery
        self.initialy = self.y
        self.initialx = self.x
        self.bounceDirection = bounceDirection # 1 = up & down, # 2 and left and right
        self.bounceLength = bounceLength
        self.rect = self.image.get_rect(center=(self.x, self.y))

    # Update the arrow
    def update(self, elapsedFrames):
        if self.bounceDirection == 1:
            self.y = self.initialy + (self.bounceLength * math.sin(elapsedFrames * 0.1)) # set the y on the same spot but moving up & down at the speed of a sine wave slowed by 10% with the amplitude of the given bounce length
        else:
            self.x = self.initialx + (self.bounceLength * math.sin(elapsedFrames * 0.1)) # set the x on the same spot but moving left & right at the speed of a sine wave slowed by 10% with the amplitude of the given bounce length
        
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y))) # position the rect with the new y
    
    # Draw the arrow
    def draw(self, canvas):
        canvas.blit(self.image, self.rect)
