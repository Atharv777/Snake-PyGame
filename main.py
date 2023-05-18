import pygame
import random
import os

pygame.mixer.init()


pygame.init()


# color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (35, 180, 80)
blue = (0, 0, 255)
yellow = (225, 225, 0)
orange = (225, 130, 40)

# create window
SCREEN_HIEGHT = 1200
SCREEN_WIDTH = 600
gameWindow = pygame.display.set_mode((SCREEN_HIEGHT, SCREEN_WIDTH))

# Game title
pygame.display.set_caption("SNAKE AND APPLES")
pygame.display.update()
CLOCK = pygame.time.Clock()

def text_onScreen(text, color, bold, size, x, y):
    FONT = pygame.font.SysFont(None, size, bold)
    screen_text = FONT.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def plot_btn(text, color, bold, x, y, width, height, btncolor = white):
    pygame.draw.rect(gameWindow, btncolor, [x, y, width, height])
    text_onScreen(text, color, bold, 55, x + 15, y+10)


def game_loop():

    # game specific variables
    EXIT_GAME = False
    GAME_OVER = False
    SNAKE_X = 580
    SNAKE_Y = 280
    VELOCITY_X = 0
    VELOCITY_Y = 0
    SNK_LIST = []
    SNK_LENGHT = 1
    score = 0

    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    if(not os.path.exists("money.txt")):
        with open("money.txt", "w") as f:
            f.write("0")

    with open("money.txt", "r") as f:
        money = f.read()

    FOOD_X = random.randint(60, SCREEN_WIDTH/2)
    FOOD_Y = random.randint(60, SCREEN_HIEGHT/2)
    score = 0
    SNAKE_SIZE = 20
    FPS = 30
    snk_direction = ""
    moneyy = 0

    while not EXIT_GAME:
        if GAME_OVER:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            with open("money.txt", "w") as f:
                f.write(str(moneyy))

            gameWindow.fill(yellow)
            text_onScreen("The snake got hurt!", red, False, 55, 380, 200)
            text_onScreen("Press Enter To Continue.",  blue, False, 55, 340, 250)
            text_onScreen(" You scored: " + str(score), green, False, 55, 440, 300)
            text_onScreen(" You earned: $" + str(moneyy), green, False, 55, 440, 350)
            plot_btn("HOME", orange, False, 500, 400, 145, 50, red)
            mouse_POS = pygame.mouse.get_pos()

            if mouse_POS[0] > 500 and mouse_POS[0] < 645 and mouse_POS[1] > 400 and mouse_POS[1] < 450:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        EXIT_GAME = True
                        home()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load("Sprites/audio/back.mp3")
                        pygame.mixer.music.play()
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        GAME_OVER = True

                    if event.key == pygame.K_RIGHT:
                        if snk_direction == "left":
                            VELOCITY_X = -10
                            VELOCITY_Y = 0
                        else:
                            snk_direction = "right"
                            VELOCITY_X = 10
                            VELOCITY_Y = 0

                    if event.key == pygame.K_LEFT:
                        if snk_direction == "right":
                            VELOCITY_X = 10
                            VELOCITY_Y = 0
                        else:
                            snk_direction = "left"
                            VELOCITY_X = -10
                            VELOCITY_Y = 0

                    if event.key == pygame.K_UP:
                        if snk_direction == "down":
                            VELOCITY_X = 0
                            VELOCITY_Y = 10
                        else:
                            snk_direction = "up"
                            VELOCITY_Y = -10
                            VELOCITY_X = 0

                    if event.key == pygame.K_DOWN:
                        if snk_direction == "up":
                            VELOCITY_X = 0
                            VELOCITY_Y = -10
                        else:
                            snk_direction = "down"
                            VELOCITY_Y = 10
                            VELOCITY_X = 0

                    if event.key == pygame.K_KP1:
                        FPS += 5

                    if event.key == pygame.K_KP0:
                        FPS = FPS-5

                    if event.key == pygame.K_RCTRL:
                        score += 2

            SNAKE_X = SNAKE_X + VELOCITY_X
            SNAKE_Y = SNAKE_Y + VELOCITY_Y

            if abs(SNAKE_X - FOOD_X)<19 and abs(SNAKE_Y - FOOD_Y)<19:
                pygame.mixer.music.load("Sprites/audio/point.wav")
                pygame.mixer.music.play()
                score = score+1
                moneyy += 0.25
                FOOD_X = random.randint(10, 1150)
                FOOD_Y = random.randint(10, 550)
                SNK_LENGHT = SNK_LENGHT + 3
                FPS += 1
                if score>int(hiscore):
                    hiscore = score
            # money += moneyy

            gameWindow.fill(white)
            text_onScreen('Score: ', green, False, 55, 5, 5)
            text_onScreen('Hiscore: ', green, False, 55, 5, 40)
            text_onScreen(str(score), red, False, 55, 130, 8)
            text_onScreen(str(hiscore), red, False, 55, 160, 43)
            
            

            pygame.draw.rect(gameWindow, red, [FOOD_X, FOOD_Y, SNAKE_SIZE, SNAKE_SIZE])

            head = []
            head.append(SNAKE_X)
            head.append(SNAKE_Y)
            SNK_LIST.append(head)

            if len(SNK_LIST)>SNK_LENGHT :
                del SNK_LIST[0]

            if head in SNK_LIST[:-1]:
                GAME_OVER = True
                pygame.mixer.music.load("Sprites/audio/death.wav")
                pygame.mixer.music.play()

            if SNAKE_X<0 or SNAKE_X>SCREEN_HIEGHT or SNAKE_Y<0 or SNAKE_Y>SCREEN_WIDTH:
                GAME_OVER = True
                pygame.mixer.music.load("Sprites/audio/death.wav")
                pygame.mixer.music.play()

            plot_snake(gameWindow, black,  SNK_LIST, SNAKE_SIZE)
        pygame.display.update()
        CLOCK.tick(FPS)

    pygame.quit()
    quit()

def settings():
    EXIT_GAME = False
    FPS = 30
    while not EXIT_GAME:
        gameWindow.fill(green)
        text_onScreen('Settings', white, False, 120, 450, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME = True

        pygame.display.update()
        CLOCK.tick(FPS)

def about():
    EXIT_GAME = False
    FPS = 30
    while not EXIT_GAME:
        gameWindow.fill(green)
        text_onScreen('ABOUT PAGE', white, False, 120, 450, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME = True

        pygame.display.update()
        CLOCK.tick(FPS)

def play_load():
    EXIT_GAME = False
    FPS = 30
    while not EXIT_GAME:
        gameWindow.fill(green)
        text_onScreen('Loading...', white, False, 120, 450, 250)
        text_onScreen('Press RCTRL to increase score by 2', white, True, 12, 550, 580)

        pygame.time.wait(500)
        EXIT_GAME = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME = True

        pygame.display.update()
        CLOCK.tick(FPS)

def settings_load():
    EXIT_GAME = False
    FPS = 30
    while not EXIT_GAME:
        gameWindow.fill(green)
        text_onScreen('Loading...', white, False, 120, 450, 250)
        text_onScreen('Press Num 0 to slow down speed of snake', white, True, 12, 550, 580)

        pygame.time.wait(500)
        EXIT_GAME = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME = True

        pygame.display.update()
        CLOCK.tick(FPS)

def about_load():
    EXIT_GAME = False
    FPS = 30
    while not EXIT_GAME:
        gameWindow.fill(green)
        text_onScreen('Loading...', white, False, 120, 450, 250)
        text_onScreen('Press 1 to make snake faster', white, True, 12, 550, 580)

        pygame.time.wait(500)
        EXIT_GAME = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME = True

        pygame.display.update()
        CLOCK.tick(FPS)

def home():
    EXIT_GAME = False
    FPS = 30
    while not EXIT_GAME:
        mouse_POS = pygame.mouse.get_pos()

        gameWindow.fill(black)
        text_onScreen('SNAKE AND APPLES', white, False, 120, 200, 150)

        plot_btn("Play", black, True, 365, 330, 120, 50)
        plot_btn("Settings", black, True, 515, 330, 200, 50)
        plot_btn("About", black, True, 740, 330, 150, 50)
        
        # if mouse_POS[0] > 0 and mouse_POS[0] < 1200 and mouse_POS[1] > 0 and mouse_POS[1] < 600:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_p:
        #             MSG = "play pressed"
        #             print(MSG)
        #             play_load()
        #             pygame.time.wait(5000)
        #             pygame.mixer.music.load("back.mp3")
        #             pygame.mixer.music.play()
        #             game_loop()

        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_s:
        #             MSG = "settings pressed"
        #             print(MSG)
        #             settings_load()
        #             pygame.time.wait(5000)
        #             settings()

        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_a:
        #             MSG = "about pressed"
        #             print(MSG)
        #             about_load()
        #             pygame.time.wait(5000)
        #             about()

        if mouse_POS[0] > 365 and mouse_POS[0] < 485 and mouse_POS[1] > 330 and mouse_POS[1] < 378:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    MSG = "play pressed"
                    print(MSG)
                    play_load()
                    pygame.time.wait(5000)
                    # pygame.mixer.music.load("back.mp3")
                    # pygame.mixer.music.play()
                    game_loop()

        if mouse_POS[0] > 515 and mouse_POS[0] < 715 and mouse_POS[1] > 330 and mouse_POS[1] < 378:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    MSG = "settings pressed"
                    print(MSG)
                    settings_load()
                    pygame.time.wait(5000)
                    settings()

        if mouse_POS[0] > 740 and mouse_POS[0] < 875 and mouse_POS[1] > 330 and mouse_POS[1] < 378:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    MSG = "about pressed"
                    print(MSG)
                    about_load()
                    pygame.time.wait(5000)
                    about()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME = True

        pygame.display.update()
        CLOCK.tick(FPS)

home()