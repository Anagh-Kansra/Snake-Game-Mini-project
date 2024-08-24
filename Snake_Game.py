import pygame
import random
import os
pygame.init()

#COLORS
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
dark_green = (144,255,144)

#SCREEN VARIABLES
screen_width = 800
screen_height = 600

#INITIALIZE SCREEN
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#BACKGROUND IMAGE
bgimg = pygame.image.load("Snake.jpeg")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()
grass = pygame.image.load("grass.jpg")
grass = pygame.transform.scale(grass,(screen_width,screen_height)).convert_alpha()

#SETTING GAME TITLE
pygame.display.set_caption("The Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(bgimg,(0,0))
        text_screen("Welcome To 'The Snake Game'",(0,0,0),130,180)
        text_screen("Press SPACE BAR to play",(0,0,0),190,230)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()
        pygame.display.update()
        clock.tick(60)

#STARTING GAME LOOP
def gameloop():

    #GAME SPECIFIC VARIABLES
    exit_game = False
    gameover = False

    snake_x = 45
    snake_y = 55
    snake_size = 30

    fps = 60

    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(100,screen_width-50)
    food_y = random.randint(120,screen_height-50)
    food_size = snake_size

    init_velocity = 5
    score = 0

    snk_list = []
    snk_length = 1

    snk_list_1 = []

    #check if hiscore value exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")

    #open the hiscore file
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()
    
    #GAME LOGIC
    while not exit_game:

        if gameover:
            
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            text_screen("Game Over",red,150,250)

            gameWindow.fill(white)
            text_screen("Game Over. Press Enter To Continue", red, 80, 250)
            text_screen("Press SPACE BAR to Restart", red, 80, 290)

            for event_inner in pygame.event.get():
                if event_inner.type == pygame.QUIT:
                    exit_game = True
                if event_inner.type == pygame.KEYDOWN:
                    if event_inner.key == pygame.K_RETURN:
                        welcome()
                    if event_inner.key == pygame.K_SPACE:
                        gameloop()
                     
        else:

            for event in pygame.event.get():
                #EXIT CONDITION
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    #CHEAT CODE
                    if event.key == pygame.K_q:
                        score += 50

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x)<30 and abs(snake_y - food_y)<30:
                score +=10
                food_x = random.randint(50,screen_width-50)
                food_y = random.randint(50,screen_height-50)
                snk_length += 5
                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill(green)
            gameWindow.blit(grass,(0,0))
            border_thickness = 5
            pygame.draw.rect(gameWindow, black, (0, 40, screen_width, border_thickness))  # Top border
            pygame.draw.rect(gameWindow, black, (0, 40, border_thickness, screen_height))  # Left border
            pygame.draw.rect(gameWindow, black, (0, screen_height - border_thickness, screen_width, border_thickness))  # Bottom border
            pygame.draw.rect(gameWindow, black, (screen_width - border_thickness, 40, border_thickness, screen_height))  # Right border
            text_screen("Score: "+ str(score) + "  Highest Score: "+ str(hiscore),black,5,5)

            if snake_x< 0 or snake_y < 40 or snake_x > screen_width-10 or snake_y > screen_height-10:
                gameover = True

            plot_snake(gameWindow, black, snk_list, snake_size)
            plot_snake(gameWindow,dark_green,snk_list_1,snake_size-20)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            head_1 = []
            head_1.append(snake_x+10)
            head_1.append(snake_y+10)
            snk_list_1.append(head_1)


            if len(snk_list) > snk_length:
                del snk_list[0]

            if len(snk_list_1) > snk_length:
                del snk_list_1[0]

            if head in snk_list[:-1]:
                gameover = True

            pygame.draw.rect(gameWindow, red, [food_x,food_y, food_size, food_size])
            pygame.draw.line(gameWindow, black, [food_x + 15, food_y - 1], [food_x + 15, food_y - 10], 3)

        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()
welcome()