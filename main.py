# This is the main file
import pygame
from pygame.locals import *
import os
import sprites
import LinkedList
import random
import pygame_menu
import time
pygame.font.init()

# Screen Variables
os.environ['SDL_VIDEO_CENTERED'] = '1'
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
SPEED = 5
SHARK_WIDTH, SHARK_HEIGHT = 100, 100
BOTTLE_WIDTH, BOTTLE_HEIGHT = 10, 10
COLLISION = pygame.USEREVENT + 1
SCREEN_COLOR = (150, 150, 255)


SHARK_IMAGE = pygame.image.load(os.path.join('assets', 'shark.png'))
BOTTLE_IMAGE = pygame.image.load(os.path.join('assets', 'water_bottle.png'))
OCEAN_IMAGE = pygame.image.load(os.path.join('assets', 'ocean.png'))



# 1 = Up, 2 = Right, 3 = Down, 4 = Left

BOTTLE_1 = BOTTLE_IMAGE
BOTTLE_2 = pygame.transform.rotate(BOTTLE_IMAGE, 90)
BOTTLE_3 = pygame.transform.rotate(BOTTLE_IMAGE, 180)
BOTTLE_4 = pygame.transform.rotate(BOTTLE_IMAGE, 270)
SHARK = pygame.transform.scale(SHARK_IMAGE, (100, 100))

bottle = [BOTTLE_1, BOTTLE_2, BOTTLE_3, BOTTLE_4]


def draw_window(list : LinkedList.LinkedList()):
    WIN.blit(OCEAN_IMAGE, (0, 0))

    curr = list.head

    while curr:
        WIN.blit(curr.data.image, (curr.data.get_x(), curr.data.get_y()))
        curr = curr.next

    pygame.display.update()

def handle_avatar_movement(sprite: sprites.Sprites, keys_pressed):
    if keys_pressed[pygame.K_UP] and sprite.get_y() > 0:  # UP
        sprite.set_y(-SPEED)

    if keys_pressed[pygame.K_DOWN] and sprite.get_y() + sprite.hitbox.height < HEIGHT:  # DOWN
        sprite.set_y(SPEED)

    if keys_pressed[pygame.K_LEFT] and sprite.get_x() > 0:  # LEFT
        sprite.set_x(-SPEED)
        
    if keys_pressed[pygame.K_RIGHT] and sprite.get_x() + sprite.hitbox.width < WIDTH:  # RIGHT
        sprite.set_x(SPEED)

def collision(shark, list):
    curr = list.head.next

    while curr:
        if shark.hitbox.colliderect(curr.data.hitbox):
            pygame.event.post(pygame.event.Event(COLLISION))
            print("Hit!")

        curr = curr.next

#button vars
# light shade of the button
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# stores the width of the
# screen into a variable
width = WIN.get_width()

# stores the height of the
# screen into a variable
height = WIN.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallfont.render('quit', True, color_dark)


def main():
    run = True
    main_menu = True
    shark_hp = 10
    clock = pygame.time.Clock()
    list = LinkedList.LinkedList()

    shark = sprites.Sprites(SHARK, pygame.Rect(10, 300, SHARK_WIDTH, SHARK_HEIGHT))
    trash = sprites.Sprites(bottle[random.randint(0, 3)], pygame.Rect(random.randint(10, 500), random.randint(10, 500), 10, 10))

    for i in range(10):
        list.push(sprites.Sprites(bottle[random.randint(0, 3)], pygame.Rect(random.randint(100, 900), random.randint(10, 600), 10, 10)))

    list.push(trash)
    list.push(shark)
    pygame.display.set_caption("PISTRIS")


    while run:
        clock.tick(FPS)
        while main_menu:
            # fills the screen with a color
            WIN.fill((37, 150, 190))
            pygame.draw.rect(WIN, color_light, [width / 2 - 75, height / 2 , 140, 40])
            WIN.blit(text, (width / 2 - 75, height / 2))

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                        main_menu = False
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == COLLISION:
                shark_hp -= 1
        if shark_hp <= 0:
            print("dead!")
            break

        keys_pressed = pygame.key.get_pressed()
        handle_avatar_movement(shark, keys_pressed)
        collision(shark, list)
        draw_window(list)


    pygame.QUIT()


if __name__ == "__main__":
    main()