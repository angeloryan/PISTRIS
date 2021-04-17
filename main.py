# This is the main file
import pygame
import os

# Screen Variables
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PISTRIS")
SCREEN_COLOR = (255, 255, 255)  # White
FPS = 60  # Frames Per Second
SPEED = 5


SHARK_IMAGE = pygame.image.load(os.path.join('assets', 'shark.png'))


def draw_window(avatar):
    WIN.fill(SCREEN_COLOR)
    WIN.blit(SHARK_IMAGE, (avatar.x, avatar.y))

    pygame.display.update()

def handle_avatar_movement(keys_pressed, avatar):
    if keys_pressed[pygame.K_a] :  # LEFT
        avatar.x -= SPEED
    if keys_pressed[pygame.K_d] :  # RIGHT
        avatar.x += SPEED
    if keys_pressed[pygame.K_w] :  # UP
        avatar.y -= SPEED
    if keys_pressed[pygame.K_s] :  # DOWN
        avatar.y += SPEED

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

    pygame.Quit()


if __name__ == "__main__":
    main()