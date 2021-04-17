# This is the main file
import pygame

# Screen Variables
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PISTRIS")
SCREEN_COLOR = (255, 255, 255)  # White
FPS = 60  # Frames Per Second


def draw_window():
    WIN.fill(SCREEN_COLOR)
    pygame.display.update()
  

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()


if __name__ == "__main__":
    main()



