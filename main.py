import pygame
import sys
import os
from settings import *
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebirth")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

high_score_file = "high_score.txt"

# Load high score from file
def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

# Save high score to file
def save_high_score(score):
    with open(high_score_file, "w") as f:
        f.write(str(score))

def draw_text_centered(text, y, color=(255, 255, 255)):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

def show_start_screen():
    screen.fill(BG_COLOR)
    draw_text_centered("REBIRTH", HEIGHT // 2 - 60, (0, 255, 255))
    draw_text_centered("Use Arrow Keys or A/D to move, Space to jump", HEIGHT // 2)
    draw_text_centered("Press any key to begin...", HEIGHT // 2 + 60)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def draw_score(score, high_score):
    score_text = font.render(f"Score: {score}  High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def main():
    global player

    # Show start screen once
    show_start_screen()

    high_score = load_high_score()
    player = Player()
    enemy = pygame.Rect(0, FLOOR_Y, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemy_speed = 3
    score = 0
    score_timer = 0
    game_over = False

    # Platforms
    platforms = [
        pygame.Rect(200, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
        pygame.Rect(400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),
        pygame.Rect(150, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    ]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not game_over:
            player.handle_input(event_list)
            player.apply_gravity(platforms)

            # Enemy movement
            if enemy.x < player.rect.x:
                enemy.x += enemy_speed
            elif enemy.x > player.rect.x:
                enemy.x -= enemy_speed

            if player.rect.colliderect(enemy):
                game_over = True
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)

            # Score timer
            score_timer += dt
            if score_timer >= 1:
                score += 1
                score_timer = 0
        else:
            if keys[pygame.K_r]:
                player = Player()
                enemy.x = 0
                score = 0
                score_timer = 0
                game_over = False

        # Draw
        screen.fill(BG_COLOR)
        player.draw(screen)
        pygame.draw.rect(screen, ENEMY_COLOR, enemy)

        for plat in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, plat)

        draw_score(score, high_score)

        if game_over:
            draw_text_centered("Game Over!", HEIGHT // 2, (255, 0, 0))
            draw_text_centered("Press R to Restart", HEIGHT // 2 + 40, (200, 200, 200))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
