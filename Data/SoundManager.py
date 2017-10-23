import pygame,random

class SoundManager(object):

    # Call constructor
    def __init__(self):
        pygame.mixer.music.load("Data/sounds/music.wav")
        self.intro = pygame.mixer.Sound("Data/sounds/intro.wav")
        self.dankhorn = pygame.mixer.Sound("Data/sounds/dankhorn.wav")
        self.bang = pygame.mixer.Sound("Data/sounds/bang.wav")
        self.attack = pygame.mixer.Sound("Data/sounds/attack.wav")
        self.reload = pygame.mixer.Sound("Data/sounds/reload.wav")
        self.dead = pygame.mixer.Sound("Data/sounds/die.wav")
        self.dead2 = pygame.mixer.Sound("Data/sounds/die2.wav")
        self.dead3 = pygame.mixer.Sound("Data/sounds/die3.wav")
        self.active = True

    # Set active
    def setActive(self, isActive):
        self.active = isActive

    # Get active
    def getActive(self):
        return self.active
    
    # Function to play a sound
    def playSound(self, sound):
        if self.getActive() == True:
            if sound == "intro": # if the sound was intro
                self.intro.play()
            elif sound == "dankhorn": # if the sound was dank horn
                self.dankhorn.play()
            elif sound == "bang": # if the sound was bang
                self.bang.play() # play the bang sound
            elif sound == "attack": # if the sound was attack
                self.attack.play() # play the attack sound
            elif sound == "reload": # if the sound was reload
                self.reload.play()
            elif sound == "dead":
                track = random.randint(1, 3)
                if track == 1: # if randomizer chose track 1
                    self.dead.play() # play zombie dying sound 1
                elif track == 2: # if randomizer chose track 2
                    self.dead2.play() # play zombie dying sound 2
                elif track == 3: # if randomizer chose track 3
                    self.dead3.play() # play zombie dying sound 3

    # Play music
    def playMusic(self):
        if self.getActive() == True:
            pygame.mixer.music.play(-1)

    # Pause music
    def pauseMusic(self):
        pygame.mixer.pause()

    # Unpause music
    def unpauseMusic(self):
        pygame.mixer.unpause()

    # End mixer
    def endMusic(self):
        pygame.mixer.music.stop()
    
    # Stop music
    def stopMusic(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
