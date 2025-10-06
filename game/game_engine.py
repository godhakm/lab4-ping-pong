import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize mixer and load sounds
pygame.mixer.init()
PADDLE_HIT_SOUND = pygame.mixer.Sound("sounds/paddle_hit.wav")
WALL_BOUNCE_SOUND = pygame.mixer.Sound("sounds/wall_bounce.wav")
SCORE_SOUND = pygame.mixer.Sound("sounds/score.wav")

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)

        self.game_over = False
        self.winner_text = ""
        self.winning_score = 5  # default

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        # Store previous velocities
        prev_velocity_x = self.ball.velocity_x
        prev_velocity_y = self.ball.velocity_y

        # Move the ball
        self.ball.move()

        # Paddle collisions
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width
            self.ball.velocity_x = abs(self.ball.velocity_x)
            PADDLE_HIT_SOUND.play()
        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width
            self.ball.velocity_x = -abs(self.ball.velocity_x)
            PADDLE_HIT_SOUND.play()

        # Wall collisions
        if self.ball.y <= 0 or self.ball.y + self.ball.height >= self.height:
            WALL_BOUNCE_SOUND.play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            SCORE_SOUND.play()
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            SCORE_SOUND.play()
            self.ball.reset()

        # AI movement
        self.ai.auto_track(self.ball, self.height)
        self.check_game_over()

    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.game_over:
            text = self.large_font.render(self.winner_text, True, WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text, text_rect)

    def check_game_over(self):
        if self.player_score >= self.winning_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        self.winner_text = ""
