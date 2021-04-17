# This is the main file
import pygame
import os

# Screen Variables
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PISTRIS")
SCREEN_COLOR = (255, 255, 255)  # White
FPS = 60  # Frames Per Second
BORDER = pygame.Rect(WIDTH - 5, 0, 10, HEIGHT)
SPEED = 5

SHARK_IMAGE = pygame.image.load(os.path.join('assets', 'shark.png'))
BOTTLE_IMAGE = pygame.image.load(os.path.join('assets', 'water_bottle.png'))

def draw_window(avatar, bottle):
    WIN.fill(SCREEN_COLOR)
    WIN.blit(SHARK_IMAGE, (avatar.x, avatar.y))
    WIN.blit(BOTTLE_IMAGE, (100, 0))

    pygame.display.update()

def handle_avatar_movement(keys_pressed, avatar):
    if keys_pressed[pygame.K_LEFT] and avatar.x - SPEED > 0:  # LEFT
        avatar.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and avatar.x + SPEED + avatar.width < BORDER.x:  # RIGHT
        avatar.x += SPEED
    if keys_pressed[pygame.K_UP] and avatar.y - SPEED > 0:  # UP
        avatar.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and avatar.y + SPEED + avatar.height < HEIGHT - 15:  # DOWN
        avatar.y += SPEED

def main():
    clock = pygame.time.Clock()
    run = True

    avatar = pygame.Rect(200, 300, 50, 50)
    bottle = pygame.Rect(100, 100, 10, 10)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(avatar, bottle)
        keys_pressed = pygame.key.get_pressed()
        handle_avatar_movement(keys_pressed, avatar)

    pygame.QUIT()



if __name__ == "__main__":
    main()