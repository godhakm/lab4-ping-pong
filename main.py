import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

        # --- Handle Game Over Delay ---
        if engine.game_over:
            pygame.display.flip()  # Ensure text is drawn
            pygame.time.wait(4000)  # Keep it on screen for 4 seconds
            running = False  # Exit after delay

    pygame.quit()

if __name__ == "__main__":
    main()
