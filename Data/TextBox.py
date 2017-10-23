
class TextBox(object): # worst class in the whole game

    # Call constructor
    def __init__(self, originx, originy, padding, font):
        self.x = originx
        self.y = originy
        self.font = font

        self.padding = padding

        self.width = 0
        self.height = 0

        self.texts = []

        self.textX = []
        self.textY = []

        
    
