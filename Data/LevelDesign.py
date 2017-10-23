
class LevelDesigns(object):

    # Call constructor:
    def __init__(self):
        self.level_am = 10 # am = amount
        self.levels = []

    def generateLevels(self):

        self.basicTemp = [
            "22222221000122222222",
            "22111111000111111122",
            "22100000000000000122",
            "22100000000000000122",
            "11100000000000000111",
            "00000000000000000000", # top mid
            "00000000000000000000", # bottom mid
            "11100000000000000111",
            "22100000000000000122",
            "22100000000000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level1 = [
            "22222221000122222222",
            "22111111000111111122",
            "22100000030000000122",
            "22100111000011100122",
            "11100100000000100111",
            "00003000003000030000", # top mid
            "00000000000000000000", # bottom mid
            "11100100000000100111",
            "22100111000011100122",
            "22100000000000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level2 = [
            "22222221000122222222",
            "21111111000111111122",
            "21100000000000000122",
            "21100110003001100122",
            "11100000011000000111",
            "00000000300000000000",
            "00000000000300000000",
            "11100000011000000111",
            "22100110030001100122",
            "22100000000000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level3 = [
            "22222221000122222222",
            "22111111000111111122",
            "22100000000000000122",
            "22110001111100011122",
            "11130000000000003111",
            "00000000010000000000", # top mid
            "00000000010000000000", # bottom mid
            "11130000000000003111",
            "22110001111100011122",
            "22100000000000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]
        
        self.level4 = [
            "22222221000122222222",
            "22111111000111111122",
            "22130000000000003122",
            "22100011000110000122",
            "11100001000100000111",
            "00000000010000000000", # top mid
            "00000000010000000000", # bottom mid
            "11100001000100000111",
            "22100011000110000122",
            "22130000000000003122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level5 = [
            "22222221000122222222",
            "22111111000111111122",
            "22110000030000001122",
            "22100111000011100122",
            "11100100000000100111",
            "00003000011000030000", # top mid
            "00000000011000000000", # bottom mid
            "11100100000000100111",
            "22100111000011100122",
            "22110000003000001122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level6 = [
            "22222221000122222222",
            "22111111000111111122",
            "22100000000000000122",
            "22100030000030000122",
            "11100010000010000111",
            "00000000010000000000", # top mid
            "00000000010000000000", # bottom mid
            "11100010000010000111",
            "22100030000030000122",
            "22100000000000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level7 = [
            "22222221000122222222",
            "22111111000111111122",
            "22100000010000000122",
            "22100031000130000122",
            "11101000000000100111",
            "00000001000100000000", # top mid
            "00001000000000100000", # bottom mid
            "11100031000130000111",
            "22100000010000000122",
            "22100000000000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level8 = [
            "22222221000122222222",
            "22111111000111111122",
            "22100000010000000122",
            "22100100030001000122",
            "11100100111001000111",
            "00000003000300000000", # top mid
            "00000100111001000000", # bottom mid
            "11100100030001000111",
            "22100000000000000122",
            "22100000010000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level9 = [
            "22222221000122222222",
            "22111111000111111122",
            "22100000000000000122",
            "22100011111111000122",
            "11103010000001030111",
            "00001000011000010000", # top mid
            "00001000011000010000", # bottom mid
            "11103010000001030111",
            "22100011111111000122",
            "22100000000000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]

        self.level10 = [
            "22222221000122222222",
            "22111111000111111122",
            "22100000000000000122",
            "22101100000000110122",
            "11101000010000010111",
            "00000010313010000000", # top mid
            "00000010313010000000", # bottom mid
            "11101000010000010111",
            "22101100000000110122",
            "22100000000000000122",
            "22111111000111111122",
            "22222221000122222222",
        ]

    def getLevelAmount(self):
        return self.level_am

    def getLevel1(self):
        return self.level1

    def getLevel2(self):
        return self.level2

    def getLevel3(self):
        return self.level3

    def getLevel4(self):
        return self.level4

    def getLevel5(self):
        return self.level5

    def getLevel6(self):
        return self.level6

    def getLevel7(self):
        return self.level7

    def getLevel8(self):
        return self.level8

    def getLevel9(self):
        return self.level9

    def getLevel10(self):
        return self.level10

    def getSpawnerAmount(self, level):
        return 4