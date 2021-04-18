# This is the main file
import pygame
import os
import sprites
import LinkedList

# Screen Variables
WIDTH, HEIGHT = 900, 500
FPS = 60
SPEED = 5
BOTTLE_SPEED = 1
COLLISION = pygame.USEREVENT + 1
SCREEN_COLOR = (150, 150, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SHARK_IMAGE = pygame.image.load(os.path.join('assets', 'shark.png'))
BOTTLE_IMAGE = pygame.image.load(os.path.join('assets', 'water_bottle.png'))


def draw_window(list : LinkedList.LinkedList()):
    WIN.fill(SCREEN_COLOR)

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

def main():
    run = True
    shark_hp = 10
    clock = pygame.time.Clock()
    list = LinkedList.LinkedList()

    shark = sprites.Sprites(SHARK_IMAGE, pygame.Rect(200,300, 50, 50))
    trash = sprites.Sprites(BOTTLE_IMAGE, pygame.Rect(100, 100, 10, 10))

    list.push(trash)
    list.push(shark)
    pygame.display.set_caption("PISTRIS")

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == COLLISION:
                shark_hp -= 1
        if shark_hp <= 0:
            print("working!")
            break
        
        keys_pressed = pygame.key.get_pressed()
        handle_avatar_movement(shark, keys_pressed)
        collision(shark, list)
        draw_window(list)

    pygame.QUIT()


if __name__ == "__main__":
    main()