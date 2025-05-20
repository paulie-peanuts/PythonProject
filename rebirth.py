# rebirth.py

import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = 50
PLAYER_COLOR = (0, 128, 255)
BG_COLOR = (30, 30, 30)
PLAYER_SPEED = 5

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebirth: The Beginning")
clock = pygame.time.Clock()

# Player setup
player_rect = pygame.Rect(WIDTH//2, HEIGHT//2, PLAYER_SIZE, PLAYER_SIZE)

# Game loop
def main():
    running = True
    while running:
        clock.tick(FPS)  # Control game speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += PLAYER_SPEED

        # Keep player on screen
        player_rect.clamp_ip(screen.get_rect())

        # Draw everything
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
