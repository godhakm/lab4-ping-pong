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

def show_replay_menu():
    font = pygame.font.SysFont("Arial", 40)
    sub_font = pygame.font.SysFont("Arial", 30)
    waiting = True
    selected = None

    while waiting:
        SCREEN.fill(BLACK)
        title = font.render("Play Again?", True, (255, 255, 255))
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        options = [
            ("Press 3 for Best of 3", pygame.K_3, 3),
            ("Press 5 for Best of 5", pygame.K_5, 5),
            ("Press 7 for Best of 7", pygame.K_7, 7),
            ("Press ESC to Exit", pygame.K_ESCAPE, None)
        ]

        for i, (text, _, _) in enumerate(options):
            opt_surface = sub_font.render(text, True, (200, 200, 200))
            SCREEN.blit(opt_surface, (WIDTH // 2 - opt_surface.get_width() // 2, HEIGHT // 2 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                for _, key, value in options:
                    if event.key == key:
                        selected = value
                        waiting = False
                        break

        clock.tick(30)

    return selected

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

        if engine.game_over:
            pygame.time.wait(2000)  # show winner message
            choice = show_replay_menu()
            if choice is None:
                running = False
            else:
                engine.winning_score = choice
                engine.reset_game()

    pygame.quit()

if __name__ == "__main__":
    main()
