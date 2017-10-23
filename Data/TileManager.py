import pygame
from Clock import Clock
from Timer import Timer

class TileManager(object):
    # Call constructor
    def __init__(self, screenWidth, screenHeight, tileWidth, tileHeight, tileImage, tileType):
        self.tiles = []
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        if tileType == "fire":
            self.tileTimeLength = 5
        elif tileType == "ice":
            self.tileTimeLength = 10

        self.tileImage = tileImage
        self.tileImage = pygame.transform.scale(self.tileImage, (self.tileWidth, self.tileHeight)) # resize the image to fit the tile

        self.active = []
        self.activeTimer = []
        

    # Get tiles
    def getTiles(self):
        return self.tiles

    # Turn on/off
    def setActive(self, tile, activity):
        self.active[tile] = activity

    # Get tile activity
    def getActive(self, tile):
        return self.active[tile]

    # Add a tile
    def addTile(self, x, y, game_Clock):
        for i in range(int(self.screenHeight / self.tileHeight)): # run a for loop for the amount of tiles on the y axis
            for z in range(int(self.screenWidth / self.tileWidth)): # run a for loop for the amount of tiles on the x axis
                tileRect = pygame.Rect((z * self.tileWidth, i * self.tileHeight),(self.tileWidth, self.tileHeight)) # generate the tile as a pygame rectangle
                if tileRect.collidepoint(x, y) == True: # check if the point lands on the tile
                    createTile = True
                    for tile in range(len(self.tiles)): # run a for loop for all existing tiles
                        if self.tiles[tile].center[0] == tileRect.center[0] and self.tiles[tile].center[1] == tileRect.center[1]: # if there isn't already a tile in that location
                            createTile = False # don't create the tile
                    if createTile == True: # if the  tile doesn't already exist
                        self.tiles.append(tileRect) # create the tile on that tile
                        self.active.append(True) # Set the Tile Active
                        self.activeTimer.append(Timer(self.tileTimeLength, game_Clock.getElapsedSeconds())) # create a 10 second timer to set the tile inactive

    # Update Fire tiles
    def update(self, game_Clock):
        for tile in range(len(self.tiles)): # run a for loop for all tiles
            if self.active[tile] == True: # if the tile is active
                if self.activeTimer[tile].getAlert() == True: # if the tile reached it's timer's limit
                    self.active[tile] = False # set the tile inactive
                else: # if not
                    self.activeTimer[tile].update(game_Clock.getElapsedSeconds()) # update the off timer

    # Draw tiles
    def draw(self, canvas):
        for tile in range(len(self.tiles)): # run a for loop for all existing tiles
            if self.active[tile] == True: # if the tile is active
                canvas.blit(self.tileImage, self.tiles[tile]) # draw the tile
    
class FireTileManager(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight, tileWidth, tileHeight):
        self.flameTile = pygame.image.load("Data/images/flame.png") # load flame image
        self.tileManager = TileManager(screenWidth, screenHeight, tileWidth, tileHeight, self.flameTile, "fire")
        

    # Get tiles
    def getTiles(self):
        return self.tileManager.getTiles()

    # Set tile activity
    def setActive(self, tile, activity):
        self.tileManager.setActive(tile, activity)

    # Get tile activity
    def getActive(self, tile):
        return self.tileManager.getActive(tile)

    # Add a tile
    def addTile(self, x, y, game_Clock):
        self.tileManager.addTile(x, y, game_Clock)

    # Update Fire tiles
    def update(self, game_Clock):
        self.tileManager.update(game_Clock)

    # Draw tiles
    def draw(self, canvas):
        self.tileManager.draw(canvas)

class IceTileManager(object):

    # Call constructor
    def __init__(self, screenWidth, screenHeight, tileWidth, tileHeight):
        self.iceTile = pygame.image.load("Data/images/icetile.jpg").convert() # load ice tile, convert it
        self.tileManager = TileManager(screenWidth, screenHeight, tileWidth, tileHeight, self.iceTile, "ice")

    # Get tiles
    def getTiles(self):
        return self.tileManager.getTiles()

    # Set tile activity
    def setActive(self, tile, activity):
        self.tileManager.setActive(tile, activity)
        
    # Get tile activity
    def getActive(self, tile):
        return self.tileManager.getActive(tile)

    # Add a tile
    def addTile(self, x, y, game_Clock):
        self.tileManager.addTile(x, y, game_Clock)

    # Update Fire tiles
    def update(self, game_Clock):
        self.tileManager.update(game_Clock)

    # Draw tiles
    def draw(self, canvas):
        self.tileManager.draw(canvas)

    
                
        
