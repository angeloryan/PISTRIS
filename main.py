import os
import sprites
import LinkedList
import random
import pygame
import time
import pygame
from pygame.locals import *
from pygame import mixer

pygame.font.init()
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
SHARK_WIDTH, SHARK_HEIGHT = 80, 80
BOTTLE_WIDTH, BOTTLE_HEIGHT = 10, 10
WIDTH, HEIGHT = 900, 500
SCREEN_COLOR = (150, 150, 255)
WHITE = (255, 255, 255)
BACKGROUND_SPEED = 4
PLAYER_SPEED = 5
FPS = 60

COLLISION = pygame.USEREVENT + 1
FONT = pygame.font.SysFont('timesnewroman', 40)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SHARK_IMAGE = pygame.image.load(os.path.join('assets', 'shark.png'))
CLAM_IMAGE = pygame.image.load(os.path.join('assets', 'clam.png'))
CRAB_IMAGE = pygame.image.load(os.path.join('assets', 'crab.png'))
BOTTLE_IMAGE = pygame.image.load(os.path.join('assets', 'water_bottle.png'))
OCEAN_IMAGE = pygame.image.load(os.path.join('assets', 'ocean.png'))
HEART_IMAGE = pygame.image.load(os.path.join('assets', 'heart.png'))
WRAPPER_IMAGE = pygame.image.load(os.path.join('assets', 'food_wrapper_0.png'))
BAG_IMAGE = [pygame.image.load(os.path.join('assets', 'plastic_bag.png')), pygame.image.load(os.path.join('assets', 'plastic_bag_1.png')), 
             pygame.image.load(os.path.join('assets', 'plastic_bag_2.png')),]
SPLASH_IMAGE = [pygame.image.load(os.path.join('assets', 'splash_0.png')), pygame.image.load(os.path.join('assets', 'splash_1.png')), 
                pygame.image.load(os.path.join('assets', 'splash_2.png')), pygame.image.load(os.path.join('assets', 'splash_3.png'))]

OCEAN = [0, 900 , 1800]
HEARTS = [10, 60, 110, 160, 210,]
CRAB = pygame.transform.scale(CRAB_IMAGE, (300, 300))
SHARK = pygame.transform.scale(SHARK_IMAGE, (100, 100))
BOTTLES = [BOTTLE_IMAGE, pygame.transform.rotate(BOTTLE_IMAGE, 90), pygame.transform.rotate(BOTTLE_IMAGE, 180), pygame.transform.rotate(BOTTLE_IMAGE, 270)]
WRAPPERS = [WRAPPER_IMAGE, pygame.transform.rotate(WRAPPER_IMAGE, 90), pygame.transform.rotate(WRAPPER_IMAGE, 180), pygame.transform.rotate(WRAPPER_IMAGE, 270)]
BAGS = [BAG_IMAGE[0], pygame.transform.rotate(BAG_IMAGE[0], 90), pygame.transform.rotate(BAG_IMAGE[0], 180), pygame.transform.rotate(BAG_IMAGE[0], 270),
        BAG_IMAGE[1], pygame.transform.rotate(BAG_IMAGE[1], 90), pygame.transform.rotate(BAG_IMAGE[1], 180), pygame.transform.rotate(BAG_IMAGE[1], 270),
        BAG_IMAGE[2], pygame.transform.rotate(BAG_IMAGE[2], 90), pygame.transform.rotate(BAG_IMAGE[2], 180), pygame.transform.rotate(BAG_IMAGE[2], 270)]
SPLASH = [pygame.transform.scale(SPLASH_IMAGE[0], (100, 100)), pygame.transform.scale(SPLASH_IMAGE[1], (100, 100)), 
          pygame.transform.scale(SPLASH_IMAGE[2], (100, 100)), pygame.transform.scale(SPLASH_IMAGE[3], (100, 100))]

splash_stage = 0

# button vars
# light shade of the button
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallfont.render('play', True, color_dark)
text_end_quit = smallfont.render('exit', True, color_dark)
text_end_play_again = smallfont.render('again', True, color_dark)


def draw_window(list : LinkedList.LinkedList(), shark, count, bob, shark_hp, score):
    global splash_stage
    curr = list.head

    for i in range(3):
        WIN.blit(OCEAN_IMAGE, (OCEAN[i], 0))

    for i in range(shark_hp):
        WIN.blit(HEART_IMAGE, (HEARTS[i], 10))

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

    # SHOW_AVATAR_HEALTH = FONT.render("Health: " + str(shark_hp), 1, WHITE)
    # WIN.blit(SHOW_AVATAR_HEALTH, (10,10))
    SHOW_SCORE = FONT.render("Score: " + str(score), 1, WHITE)
    WIN.blit(SHOW_SCORE, (700, 10))

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

def main():
    run = True
    main_menu = True
    end_menu = False
    vulnerable = True
    start = True
    bob = False
    time = 0
    count = 0
    counter = 0
    score = 0
    shark_hp = 5
    trash_list = LinkedList.LinkedList()
    clock = pygame.time.Clock()
    
    shark = sprites.Sprites(SHARK, pygame.Rect(10, 300, SHARK_WIDTH, SHARK_HEIGHT))

    for i in range(5):
        trash_list.push(sprites.Sprites(BAGS[random.randint(0, 11)], pygame.Rect(random.randint(600, 1800), random.randint(10, 500), 50, 50)))
        trash_list.push(sprites.Sprites(BOTTLES[random.randint(0, 3)], pygame.Rect(random.randint(600, 1800), random.randint(10, 500), 10, 10)))
        trash_list.push(sprites.Sprites(WRAPPERS[random.randint(0, 3)], pygame.Rect(random.randint(600, 1800), random.randint(10, 500), 10, 10)))
        

    pygame.display.set_caption("PISTRIS")

    while main_menu:
            WIN.blit(OCEAN_IMAGE, (0, 0))
            WIN.blit(CLAM_IMAGE, (WIDTH/2 - 25, HEIGHT / 2 - 80))
            pygame.draw.rect(WIN, color_light, [WIDTH / 2 - 70, HEIGHT / 2 - 45/2 , 140, 40])
            WIN.blit(text, (WIDTH / 2 - 70/2 + 1, HEIGHT / 2 - 45/2))

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if WIDTH / 2 - 70 <= mouse[0] <= WIDTH / 2 + 70 and HEIGHT / 2 - 45/2 <= mouse[1] <= HEIGHT / 2 + 45/2:
                        main_menu = False
                pygame.display.update()

    while run:
        clock.tick(FPS)
        time += 1
        count += 1

        if start:
            mixer.music.load('Da_Music.mp3')
            mixer.music.play(-1)
            start = False

        if vulnerable is False:
            counter += 1
        if counter % 30 == 0:
            vulnerable = True

        if time % 25 == 0:
            score += 1


        # Scrolling background, resets background ahead if background hits fully offscreen
        for i in range(3):
            OCEAN[i] -= BACKGROUND_SPEED

            if OCEAN[i] == -900:
                OCEAN[i] = 1800

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == COLLISION:
                shark_hp -= 1
                vulnerable = False
        if shark_hp <= 0:
            end_menu = True

        keys_pressed = pygame.key.get_pressed()
        handle_avatar_movement(shark, keys_pressed)
        collision(shark, trash_list, vulnerable)
        draw_window(trash_list, shark, count, bob, shark_hp, score)

        while end_menu:
            # fills the screen with a color
            WIN.blit(OCEAN_IMAGE, (0, 0))
            pygame.draw.rect(WIN, color_light, [WIDTH / 2 + 40, HEIGHT / 2 - 45/2 , 140, 40])
            pygame.draw.rect(WIN, color_light, [WIDTH / 2 - 180, HEIGHT / 2 - 45/2 , 140, 40])
            WIN.blit(text_end_quit, (WIDTH / 2 + 40 + 75/2 + 5, HEIGHT / 2 - 45/2))
            WIN.blit(text_end_play_again, (WIDTH / 2 - 180 + 75/2 - 5, HEIGHT / 2 - 45/2))

            WIN.blit(CRAB, (WIDTH/2 - 150, HEIGHT / 2 - 25))

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if WIDTH / 2 + 40 <= mouse[0] <= WIDTH / 2 + 180 and HEIGHT / 2 - 45/2 <= mouse[1] <= HEIGHT / 2 + 45 / 2:
                        pygame.QUIT()
                    if WIDTH / 2 - 180 <= mouse[0] <= WIDTH / 2 - 40 and HEIGHT / 2 - 45/2 <= mouse[1] <= HEIGHT / 2 + 45 / 2:
                        main()
                pygame.display.update()

    pygame.QUIT()


if __name__ == "__main__":
    main()