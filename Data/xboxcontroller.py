######################################################################
#
#   XBOX 360 CONTROLLER - SCRIPT
#   BY: ELISON
#   SCRIPT: PUBLIC
#
######################################################################


import pygame
pygame.init()
end = False
clock = pygame.time.Clock()

screenSize = [425,300]
screen = pygame.display.set_mode(screenSize)
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
font = pygame.font.SysFont('Consolas', 15)

pygame.joystick.init()
count = pygame.joystick.get_count()
buttonName = ['A Button','B Button','X Button','Y Button','Left Bumper','Right Bumper', 'Back', 'Start', 'Left Thumbstick', 'Right Thumbstick']

# -- Raw data --
buttonList = [0,0,0,0,0,0,0,0,0,0]
axesList = [0,0,0,0,0]
hatList = [(0,0)]
# -- Raw data --

def check():
    global count
    if count == 0:
        print('Controller.py could not find a connected controller!')
        print('Please connect a controller...')
        while count == 0:
            pygame.joystick.init()
            count = pygame.joystick.get_count()
            pygame.joystick.quit()
        pygame.joystick.init()

    if count != 0:
        print('Controllers Connected : ' + str(count))

def controllerData():
    global count
    for i in range(count):
        # Joystick
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # Name
        name = joystick.get_name()
        nameTxt = font.render(name, True, (255,255,255))
        screen.blit(nameTxt, (5, 5))

        # Axes
        axes = joystick.get_numaxes()
        for i in range( axes ):
            axis = joystick.get_axis( i )
            axesList[i] = axis

        leftStickCoords = (round(axesList[0], 2)), (round(axesList[1], 2))
        leftTxt = font.render('Left Thumbstick - [' + str(leftStickCoords[0]) + ', ' + str(leftStickCoords[1]) + ']', True, (255,255,255))
        screen.blit(leftTxt, (5,25))

        rightStickCoords = (round(axesList[3], 2)), (round(axesList[4], 2))
        rightTxt = font.render('Right Thumbstick - [' + str(rightStickCoords[0]) + ', ' + str(rightStickCoords[1]) + ']', True, (255,255,255))
        screen.blit(rightTxt, (5,40))

        axesList[2] = round(axesList[2], 3)
        if axesList[2] > 0:
            leftTrigger = font.render('Left Trigger - ' + str(axesList[2]),True, (255,255,255))
            rightTrigger = font.render('Right Trigger - 0', True, (255,255,255))
        elif axesList[2] < 0:
            leftTrigger = font.render('Left Trigger - 0',True, (255,255,255))
            rightTrigger = font.render('Right Trigger - ' + str(abs(axesList[2])), True, (255,255,255))
        else:
            leftTrigger = font.render('Left Trigger - 0',True, (255,255,255))
            rightTrigger = font.render('Right Trigger - 0', True, (255,255,255))

        screen.blit(leftTrigger, (5,55 + 15))
        screen.blit(rightTrigger, (5,70 + 15))

        # Buttons
        buttons = joystick.get_numbuttons()
        for i in range( buttons ):
            button = joystick.get_button( i )
            buttonList[i] = button

        # Hats
        hats = joystick.get_numhats()
        for i in range( hats ):
            hat = joystick.get_hat( i )
            hatList[i] = hat
        print(hatList)
        
        x = 100 + 45
        for i in range(len(buttonName)):
            buttonTxt = font.render(buttonName[i] + ' - ' + str(buttonList[i]), True, (255,255,255))
            screen.blit(buttonTxt, (5, x))
            x += 15
        hatTxt = font.render('Hat Position - [' + str(hat[0]) + ', ' + str(hat[1]) + ']', True, (255,255,255))
        screen.blit(hatTxt, (5, 115))

        '''
        raw data
        print(hats)
        '''


check()

end = False

while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
    screen.blit(background, (0, 0))
    controllerData()

    pygame.display.update()
    clock.tick(20)

pygame.quit()
