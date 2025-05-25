import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_COLOR = (0, 128, 255)
ENEMY_COLOR = (255, 0, 0)
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 40
BG_COLOR = (30, 30, 30)

GRAVITY = 0.5
JUMP_STRENGTH = -10
FLOOR_Y = HEIGHT - PLAYER_HEIGHT

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebirth: Gravity Mode")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 28)

# Player setup
player_rect = pygame.Rect(WIDTH // 2, FLOOR_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
player_velocity_y = 0
on_ground = True

# Enemy setup
enemy_rect = pygame.Rect(0, FLOOR_Y, ENEMY_WIDTH, ENEMY_HEIGHT)
enemy_speed = 3

# Score system
score = 0
score_timer = 0
game_over = False

# Function to draw score
def draw_score(score):
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

def main():
    global player_velocity_y, on_ground, score, score_timer, game_over

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not game_over:
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

            # Move enemy toward player
            if enemy_rect.x < player_rect.x:
                enemy_rect.x += enemy_speed
            elif enemy_rect.x > player_rect.x:
                enemy_rect.x -= enemy_speed

            # Collision detection
            if player_rect.colliderect(enemy_rect):
                game_over = True

            # Score update
            score_timer += dt
            if score_timer >= 1:
                score += 1
                score_timer = 0

        else:
            # Restart game if R is pressed
            if keys[pygame.K_r]:
                player_rect.x = WIDTH // 2
                player_rect.y = FLOOR_Y
                enemy_rect.x = 0
                enemy_rect.y = FLOOR_Y
                player_velocity_y = 0
                score = 0
                score_timer = 0
                game_over = False
                on_ground = True

        # Drawing
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        pygame.draw.rect(screen, ENEMY_COLOR, enemy_rect)
        draw_score(score)

        if game_over:
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            restart_text = font.render("Press R to Restart", True, (200, 200, 200))
            screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 40))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
