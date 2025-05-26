import pygame, sys
from settings import *
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebirth")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

player = Player()
enemy = pygame.Rect(0, FLOOR_Y, ENEMY_WIDTH, ENEMY_HEIGHT)
enemy_speed = 3
score = 0
score_timer = 0
game_over = False

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def main():
    global score, score_timer, game_over
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
            player.apply_gravity()

            # Enemy movement
            if enemy.x < player.rect.x:
                enemy.x += enemy_speed
            elif enemy.x > player.rect.x:
                enemy.x -= enemy_speed

            if player.rect.colliderect(enemy):
                game_over = True

            # Score
            score_timer += dt
            if score_timer >= 1:
                score += 1
                score_timer = 0
        else:
            if keys[pygame.K_r]:
                player.__init__()  # Reset player
                enemy.x = 0
                score = 0
                score_timer = 0
                game_over = False

        # Draw
        screen.fill(BG_COLOR)
        player.draw(screen)
        pygame.draw.rect(screen, ENEMY_COLOR, enemy)
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
