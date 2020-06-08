import random
import sys
import pygame
import time

clock = pygame.time.Clock()
fps = 30
dim = (800, 600)
caption = 'Slither'

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)

pygame.init()
gameDisplay = pygame.display.set_mode(dim)
pygame.display.set_caption(caption)



img = pygame.image.load('snake_head2.png')

apple_img = pygame.image.load('apple.png')

direction = 'right'

smallfont = pygame.font.SysFont("comicsansms", 20, False, False)
medfont = pygame.font.SysFont("comicsansms", 40, False, False)
largefont = pygame.font.SysFont("comicsansms", 80, False, False)

def score(score):
    text = smallfont.render("Score: "+str(score), True, blue)
    gameDisplay.blit(text, (0,0))

def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
        textRect = textSurface.get_rect()
        return textSurface, textRect
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
        textRect = textSurface.get_rect()
        return textSurface, textRect
    elif size == 'large':
        textSurface = largefont.render(text, True, color)
        textRect = textSurface.get_rect()
        return textSurface, textRect

def message_to_screen(msg, color,y_displace=0, size= 'small'):
    textSurface, textRect = text_objects(msg, color,size)
    textRect.center = dim[0] / 2, dim[1] / 2 + y_displace
    gameDisplay.blit(textSurface, textRect)
    pygame.display.update()

def snake(snakeList, width, height):
    if direction == 'right':
        head_img = pygame.transform.rotate(img, 270)


    elif direction == 'left':
        head_img = pygame.transform.rotate(img, 90)

    elif direction == 'down':
        head_img = pygame.transform.rotate(img, 180)


    elif direction == 'up':
        head_img = img

    gameDisplay.blit(head_img, snakeList[-1])
    for XnY in snakeList[1:-1]:
        pygame.draw.rect(gameDisplay, black, [XnY[0], XnY[1], width, height])

def start_screen():
    gameIntro = True
    gameDisplay.fill(white)
    while gameIntro:

        message_to_screen("Welcome to Slither!",(0,155,0),-50,'large')
        message_to_screen("The objective of the game is to eat as many apples as possible", black,30)
        message_to_screen("Use the arrow keys to move around",black, 60)
        message_to_screen("You will die if  you run into the edges or yourself", black, 90)
        message_to_screen("Press C to Play, P to Pause or Q to quit...",red, 120)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameIntro = False
                    pygame.quit()
                    quit()

                if event.key == pygame.K_c:
                    GameLoop()
                    gameIntro = False

            if event.type == pygame.QUIT:
                gameIntro = False
                pygame.quit()
                quit()
    clock.tick(5)

def pause():
    paused  = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    for i in range(3,0,-1):
                        pause_countdown(i)
                    paused = False
                elif event.key == pygame.K_q:
                    paused = False
                    pygame.quit()
                    quit()

        message_to_screen("Paused", blue,-200, 'large')
        message_to_screen("Press C to continue or Q to exit...", blue, 50)

        clock.tick(5)

def pause_countdown(sec):
    message_to_screen("Resuming in " + str(sec) + "...", blue, 100 + 20*(3-sec))
    time.sleep((1))

def GameLoop():
    global direction
    global fps
    direction = 'right'
    lead_x = dim[0] // 2
    lead_y = dim[1] // 2
    width = 20
    height = 20

    initial_vel = 0

    AppleSize = 30

    lead_x_change = 10
    lead_y_change = 0

    randAppleX = random.randrange(20, dim[0] - width - 10)
    randAppleY = random.randrange(20, dim[1] - height - 10)

    GameExit = False
    GameOver = False

    snakeList = []
    snakeLenth = 1

    crash_edge = False
    crash_self = False

    while not GameExit:

        while GameOver:
            message_to_screen("GAME OVER", (120,0,0), -50, 'large' )

            if crash_self:
                message_to_screen("You crashed into yourself!", black,50,)
            elif crash_edge:
                message_to_screen("You crashed into the edge!", black, 50, )

            message_to_screen("Press C to restart or Q to quit", blue, 100, 'medium')

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        GameExit = True
                        GameOver = False
                        sys.exit()

                    if event.key == pygame.K_c:
                        GameLoop()

                if event.type == pygame.QUIT:
                    GameExit = True
                    GameOver = False
                    sys.exit()

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                crash_self = True
                GameOver = True

        for event in pygame.event.get():

            print(event)

            if event.type == pygame.QUIT:
                GameExit = True
                sys.exit()

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT and lead_x_change != width -initial_vel:
                    lead_x_change = -width + initial_vel
                    lead_y_change = 0
                    direction = 'left'

                if event.key == pygame.K_RIGHT and lead_x_change != -width + initial_vel:
                    lead_x_change = width -initial_vel
                    lead_y_change = 0
                    direction = 'right'
                if event.key == pygame.K_UP and lead_y_change != height - initial_vel:
                    lead_y_change = -height + initial_vel
                    lead_x_change = 0
                    direction = 'up'
                if event.key == pygame.K_DOWN and lead_y_change != -height +initial_vel:
                    lead_y_change = height -initial_vel
                    lead_x_change = 0
                    direction = 'down'
                elif event.key == pygame.K_p:
                    pause()


        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x + width > dim[0] or lead_x < 0 or lead_y + height > dim[1] or lead_y < 0:
            crash_edge = True
            GameOver = True


            """if event.type == pygame.KEYUP: # Move until the key is held
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    lead_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    lead_y_change = 0"""

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        gameDisplay.fill((0, 255, 0))
        gameDisplay.blit(apple_img, [randAppleX, randAppleY])

        snake(snakeList, width, height)

        if len(snakeList) > snakeLenth:
            del snakeList[0]

        score(snakeLenth-1)

        pygame.display.update()

        if (lead_x >= randAppleX and lead_x <= randAppleX + AppleSize) or (
                lead_x + width >= randAppleX and lead_x + width <= randAppleX + AppleSize) or (
                lead_x <= randAppleX and lead_x + width >= randAppleX + AppleSize):
            if (lead_y >= randAppleY and lead_y <= randAppleY + AppleSize) or (
                    lead_y + height >= randAppleY and lead_y + height <= randAppleY + AppleSize) or (
                    lead_y <= randAppleY and lead_y + height >= randAppleY + AppleSize):
                randAppleX = random.randrange(20, dim[0] - width - 10)
                randAppleY = random.randrange(20, dim[1] - height - 10)
                snakeLenth += 1

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                crash_self = True
                GameOver = True

        clock.tick(fps)

start_screen()
GameLoop()

pygame.quit()
quit()
