# rebirth.py

import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_COLOR = (0, 128, 255)
BG_COLOR = (30, 30, 30)

GRAVITY = 0.5
JUMP_STRENGTH = -10
FLOOR_Y = HEIGHT - PLAYER_HEIGHT

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebirth: Gravity Mode")
clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont("Arial", 28)

# Player setup
player_rect = pygame.Rect(WIDTH // 2, FLOOR_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
player_velocity_y = 0
on_ground = True

# Score
score = 0
score_timer = 0  # keeps track of time passed for score update

def draw_score(score):
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

def main():
    global player_velocity_y, on_ground, score, score_timer

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Time in seconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += 5

        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and on_ground:
            player_velocity_y = JUMP_STRENGTH
            on_ground = False

        # Gravity
        player_velocity_y += GRAVITY
        player_rect.y += player_velocity_y

        # Floor collision
        if player_rect.y >= FLOOR_Y:
            player_rect.y = FLOOR_Y
            player_velocity_y = 0
            on_ground = True

        # Update score every 1 second
        score_timer += dt
        if score_timer >= 1:
            score += 1
            score_timer = 0

        # Draw everything
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        draw_score(score)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
