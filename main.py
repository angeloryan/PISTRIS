# This is the main file
import pygame
import os

# Screen Variables
WIDTH, HEIGHT = 900, 500
FPS = 60
SPEED = 5
SCREEN_COLOR = (150, 150, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PISTRIS")

SHARK_IMAGE = pygame.image.load(os.path.join('assets', 'shark.png'))


def draw_window(avatar):
    WIN.fill(SCREEN_COLOR)
    WIN.blit(SHARK_IMAGE, (avatar.x,avatar.y))

    pygame.display.update()

def handle_avatar_movement(keys_pressed, avatar):
    if keys_pressed[pygame.K_UP] and avatar.y > 0:  # UP
        avatar.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and avatar.y + avatar.height < HEIGHT:  # DOWN
        avatar.y += SPEED
    if keys_pressed[pygame.K_LEFT] and avatar.x > 0:  # LEFT
        avatar.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and avatar.x + avatar.width < WIDTH:  # RIGHT
        avatar.x += SPEED

def main():
    clock = pygame.time.Clock()
    run = True

    avatar = pygame.Rect(200,300, 50, 50)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw_window(avatar)
        keys_pressed = pygame.key.get_pressed()
        handle_avatar_movement(keys_pressed, avatar)

    pygame.QUIT()


if __name__ == "__main__":
    main()