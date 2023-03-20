import pygame
import os
import math

pygame.init()
WIDTH, HEIGHT = 800 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("BricKs Game -by Binary Bandits ")
LIVES_FONT = pygame.font.SysFont("comicsans", 40)
FPS = 60
VEL = 9
rows = 6
cols = 8
brick_width = WIDTH // cols -2
brick_height = 35
BALL_VEL = 10
BALL_VEL_Y = 10
BALL_VEL_X = 0
BAR_WIDTH , BAR_HEIGHT = 200 , 40
BALL_RADIUS = 15
ball_y_direc = "up"
ball_x_direc = "right"
KEY = "right"
BAR_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','bar.png')), (BAR_WIDTH,BAR_HEIGHT))
Ball_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','ball.png')), (BALL_RADIUS *2,BALL_RADIUS * 2))
Red_brick_image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','red_brick.png')), (brick_width,brick_height))
green_brick_image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','green_brick.png')), (brick_width,brick_height))
blue_brick_image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','blue_brick.png')), (brick_width,brick_height))
Background_image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background.jpg')), (WIDTH , HEIGHT))
class bricks:
    def __init__(self , x, y, width, height, health, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.image = image

    def draw(self,win):
        WIN.blit(self.image, (self.x,self.y))

    def collide(self,ball):
        if not (ball.x <= self.x + self.width and ball.x >= self.x):
            return False
        if not (ball.y <= self.y+ self.height and ball.y >= self.y):
            return False
        self.hit()
        global ball_y_direc
        ball_y_direc = "down"
        return True

    def hit(self):
        self.health -= 1
        if(self.health == 2):
            self.image = green_brick_image
        elif(self.health == 1):
            self.image = blue_brick_image


def draw_window(bar,ball,Bricks,lives):
    WIN.blit(Background_image , (0,0))
    WIN.blit(BAR_IMAGE, (bar.x,bar.y))
    WIN.blit(Ball_IMAGE, (ball.x,ball.y))

    for brick in Bricks:
        brick.draw(WIN)

    lives_text = LIVES_FONT.render(f"lives: {lives}", 1, "white")
    WIN.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))
    pygame.display.update()

def bar_movement(keys_pressed , bar):
    global KEY
    if keys_pressed[pygame.K_LEFT] and bar.x - VEL > -15 :
        KEY = "left"
        bar.x -= VEL
    elif keys_pressed[pygame.K_RIGHT] and bar.x + VEL < WIDTH - BAR_WIDTH + 15:
        KEY = "right"
        bar.x += VEL

def ball_bar_collision(ball,bar):
    global ball_y_direc
    global ball_x_direc
    global BALL_VEL_Y
    global BALL_VEL_X
    if not (ball.x <= bar.x + BAR_WIDTH and ball.x >= bar.x):
        return
    if not (ball.y + BALL_RADIUS*2 >= bar.y):
        return
    bar_center = bar.x + BAR_WIDTH/2
    distance_to_center = ball.x - bar_center
    
    percent_width = abs(distance_to_center) / BAR_WIDTH
    angle = percent_width * 90
    angle_radian = math.radians(angle)

    BALL_VEL_X = math.sin(angle_radian) * BALL_VEL
    BALL_VEL_Y = math.cos(angle_radian) * BALL_VEL
    if(distance_to_center >0):
        ball_x_direc = "right"
    else:
        ball_x_direc = "left"
    ball_y_direc = "up"


def ball_movement(ball,bar):
    global ball_y_direc
    global ball_x_direc
    global BALL_VEL_X
    global BALL_VEL_Y
    if (ball_y_direc == "up") and (ball.y > 0 ):
        ball.y -= BALL_VEL_Y
    elif (ball_y_direc == "up") and (ball.y <= 0) :
        ball_y_direc = "down"
    elif (ball_y_direc == "down") :
        ball_bar_collision(ball,bar)
        if (ball.y == HEIGHT):
            pygame.quit()
        ball.y += BALL_VEL_Y
    if (ball_x_direc == "right") and (ball.x + BALL_RADIUS*2 <WIDTH):
        ball.x += BALL_VEL_X
    elif (ball_x_direc == "right") and (ball.x + BALL_RADIUS*2 >=WIDTH):
        ball_x_direc = "left"
    elif (ball_x_direc == "left") and (ball.x >0):
        ball.x -= BALL_VEL_X
    elif (ball_x_direc == "left") and (ball.x <=0):
        ball_x_direc = "right"
    
def generate_bricks(rows , cols):
    gap = 2
    Bricks = []
    for row in range(rows):
        for col in range(cols):
            brick = bricks(col * brick_width + gap*col , row* brick_height +gap, brick_width , brick_height, 3 , Red_brick_image)
            Bricks.append(brick)
    return Bricks

def main():
    lives =3
    bar = pygame.Rect(WIDTH/2 - BAR_WIDTH/2 , 550,BAR_WIDTH, BAR_HEIGHT)
    ball = pygame.Rect(WIDTH/2 - BALL_RADIUS , bar.y -BALL_RADIUS *2 , BALL_RADIUS *2, BALL_RADIUS*2)
    clock = pygame.time.Clock()
    Bricks = generate_bricks(rows, cols)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys_pressed = pygame.key.get_pressed()
        bar_movement(keys_pressed , bar)
        ball_movement(ball,bar)

        for brick in Bricks[:]:
            brick.collide(ball)
            if brick.health <= 0:
                Bricks.remove(brick)

        draw_window(bar,ball,Bricks,lives)

        if ball.y + BALL_RADIUS >= HEIGHT :
            global BALL_VEL_Y
            global BALL_VEL_X
            global ball_y_direc 
            lives -= 1
            ball.x = bar.x + BAR_WIDTH/2
            ball.y = bar.y - BALL_RADIUS*2
            BALL_VEL_X = 0
            BALL_VEL_Y = 10
            ball_y_direc = "up"

        if len(Bricks) ==0 :
            win_text = LIVES_FONT.render(" Chaap diya ", 1 , "white")
            WIN.blit(win_text , (WIDTH /2 -win_text.get_width()/2 , HEIGHT/2 -win_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()

        if lives <= 0:
            lives =3
            bar = pygame.Rect(300 , 550,BAR_WIDTH, BAR_HEIGHT)
            ball = pygame.Rect(350, 450,BALL_RADIUS *2, BALL_RADIUS*2)
            clock = pygame.time.Clock()
            Bricks = generate_bricks(rows, cols)

            lost_text = LIVES_FONT.render("HAAG DIYA \n TRY AGAIN !!! \n wait for 8sec", 1 , "white")
            WIN.blit(lost_text , (WIDTH /2 -lost_text.get_width()/2 , HEIGHT/2 -lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(8000)


    pygame.quit()

if __name__ == "__main__":
    main()