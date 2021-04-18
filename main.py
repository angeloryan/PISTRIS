import pygame
from pygame.locals import *
import os
import sprites
import LinkedList
import random
import pygame
import time
pygame.font.init()

# Screen Variables
os.environ['SDL_VIDEO_CENTERED'] = '1'
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BACKGROUND_SPEED = 3
PLAYER_SPEED = 5
SHARK_WIDTH, SHARK_HEIGHT = 100, 100
BOTTLE_WIDTH, BOTTLE_HEIGHT = 10, 10
COLLISION = pygame.USEREVENT + 1
SCREEN_COLOR = (150, 150, 255)
WHITE = (255, 255, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
HEALTH_FONT = pygame.font.SysFont('timesnewroman', 40)

SHARK_IMAGE = pygame.image.load(os.path.join('assets', 'shark.png'))
BOTTLE_IMAGE = pygame.image.load(os.path.join('assets', 'water_bottle.png'))
OCEAN_IMAGE = pygame.image.load(os.path.join('assets', 'ocean.png'))
SPLASH_IMAGE = [pygame.image.load(os.path.join('assets', 'splash_0.png')), pygame.image.load(os.path.join('assets', 'splash_1.png')), 
                pygame.image.load(os.path.join('assets', 'splash_2.png')), pygame.image.load(os.path.join('assets', 'splash_3.png'))]

SHARK = pygame.transform.scale(SHARK_IMAGE, (100, 100))
BOTTLES = [BOTTLE_IMAGE, pygame.transform.rotate(BOTTLE_IMAGE, 90), pygame.transform.rotate(BOTTLE_IMAGE, 180), pygame.transform.rotate(BOTTLE_IMAGE, 270)]
OCEAN = [0, 900 , 1800]
SPLASH = [pygame.transform.scale(SPLASH_IMAGE[0], (100, 100)), pygame.transform.scale(SPLASH_IMAGE[1], (100, 100)), 
          pygame.transform.scale(SPLASH_IMAGE[2], (100, 100)), pygame.transform.scale(SPLASH_IMAGE[3], (100, 100))]

splash_stage = 0

def draw_window(list : LinkedList.LinkedList(), shark, count, bob, shark_hp):
    global splash_stage

    for i in range(3):
        WIN.blit(OCEAN_IMAGE, (OCEAN[i], 0))

    curr = list.head

    while curr:
        WIN.blit(curr.data.image, (curr.data.get_x(), curr.data.get_y()))
        curr.data.set_x(-BACKGROUND_SPEED)

        if curr.data.get_x() < -10:
            curr.data.set_x(random.randint(10, 910) + WIDTH)
            curr.data.hitbox.y = (random.randint(10, 450))

        if count % 10 == 0:
            if bob:
                curr.data.set_y(-5)
                bob = False
            else:
                curr.data.set_y(5)
                bob = True
        curr = curr.next

    WIN.blit(shark.image, (shark.get_x(), shark.get_y()))
    WIN.blit(SPLASH[splash_stage // 7], (shark.get_x() - 55, shark.get_y()))

    if splash_stage == 24:
        splash_stage = 0
    else:
        splash_stage += 1

    SHOW_AVATAR_HEALTH = HEALTH_FONT.render("Health: " + str(shark_hp),1,WHITE)
    WIN.blit(SHOW_AVATAR_HEALTH, (10,10))

    pygame.display.update()

def handle_avatar_movement(sprite: sprites.Sprites, keys_pressed):
    if keys_pressed[pygame.K_UP] and sprite.get_y() > 0:  # UP
        sprite.set_y(-PLAYER_SPEED)

    if keys_pressed[pygame.K_DOWN] and sprite.get_y() + sprite.hitbox.height < HEIGHT:  # DOWN
        sprite.set_y(PLAYER_SPEED)

    if keys_pressed[pygame.K_LEFT] and sprite.get_x() > 0:  # LEFT
        sprite.set_x(-PLAYER_SPEED)
        
    if keys_pressed[pygame.K_RIGHT] and sprite.get_x() + sprite.hitbox.width < WIDTH:  # RIGHT
        sprite.set_x(PLAYER_SPEED)

def collision(shark, list, vulnerable):
    curr = list.head.next

    while curr and vulnerable:
        if shark.hitbox.colliderect(curr.data.hitbox):
            pygame.event.post(pygame.event.Event(COLLISION))
            print("Hit!")
            vulnerable = False

        curr = curr.next

# button vars
# light shade of the button
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallfont.render('quit', True, color_dark)


def main():
    run = True
    main_menu = True
    shark_hp = 10
    time = 0
    count = 0
    bob = False
    counter = 0
    clock = pygame.time.Clock()
    list = LinkedList.LinkedList()
    vulnerable = True
    
    


    shark = sprites.Sprites(SHARK, pygame.Rect(10, 300, SHARK_WIDTH, SHARK_HEIGHT))

    for i in range(10):
        list.push(sprites.Sprites(BOTTLES[random.randint(0, 3)], pygame.Rect(random.randint(300, 900), random.randint(10, 500), 10, 10)))

    pygame.display.set_caption("PISTRIS")


    while run:
        clock.tick(FPS)
        time += 1
        count += 1

        if vulnerable is False:
            counter += 1
        if counter % 30 == 0:
            vulnerable = True
        


        # Scrolling background, resets background ahead if background hits fully offscreen
        for i in range(3):
            OCEAN[i] -= BACKGROUND_SPEED

            if OCEAN[i] == -900:
                OCEAN[i] = 1800
        while main_menu:
            # fills the screen with a color
            WIN.fill((37, 150, 190))
            pygame.draw.rect(WIN, color_light, [WIDTH / 2 - 75, HEIGHT / 2 , 140, 40])
            WIN.blit(text, (WIDTH / 2 - 75, HEIGHT / 2))

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
                        main_menu = False
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == COLLISION:
                shark_hp -= 1
                vulnerable = False
        if shark_hp <= 0:
            break

        keys_pressed = pygame.key.get_pressed()
        handle_avatar_movement(shark, keys_pressed)
        collision(shark, list, vulnerable)
        draw_window(list, shark, count, bob, shark_hp)

    pygame.QUIT()


if __name__ == "__main__":
    main()