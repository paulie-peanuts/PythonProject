import pygame
import sys
from settings import *
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebirth")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

player = Player()
ground_enemies = []
flying_enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = 2  # seconds
score = 0
score_timer = 0
high_score = 0
game_over = False
start_screen = True

# Platforms
platforms = [
    pygame.Rect(200, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(150, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
]

def draw_score(score, high_score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (200, 200, 200))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

def draw_health_bar(health):
    bar_width = 200
    bar_height = 20
    bar_x = WIDTH - bar_width - 10
    bar_y = 10
    fill_width = (health / 100) * bar_width
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

def spawn_enemy():
    from random import choice
    if choice([True, False]):
        rect = pygame.Rect(0, FLOOR_Y, ENEMY_WIDTH, ENEMY_HEIGHT)
        flying = False
    else:
        rect = pygame.Rect(0, 100, ENEMY_WIDTH, ENEMY_HEIGHT)
        flying = True
    return {"rect": rect, "health": 2, "flying": flying}

def reset_game():
    global ground_enemies, flying_enemies, score, score_timer, game_over
    player.__init__()
    ground_enemies = []
    flying_enemies = []
    score = 0
    score_timer = 0
    game_over = False

def main():
    global score, score_timer, high_score, game_over, enemy_spawn_timer, start_screen

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if start_screen:
            screen.fill(BG_COLOR)
            title = font.render("REBIRTH", True, (255, 255, 255))
            controls = font.render("Arrow Keys / A-D to move, W/Space to jump, F to shoot", True, (200, 200, 200))
            start = font.render("Press Enter to Start", True, (150, 150, 255))
            screen.blit(title, (WIDTH // 2 - 60, HEIGHT // 2 - 80))
            screen.blit(controls, (WIDTH // 2 - 220, HEIGHT // 2 - 20))
            screen.blit(start, (WIDTH // 2 - 140, HEIGHT // 2 + 40))
            pygame.display.flip()

            if keys[pygame.K_RETURN]:
                start_screen = False
            continue

        if not game_over:
            player.handle_input(event_list)
            player.apply_gravity(platforms)
            player.update_projectiles()

            enemy_spawn_timer += dt
            if enemy_spawn_timer >= enemy_spawn_delay:
                new_enemy = spawn_enemy()
                if new_enemy["flying"]:
                    flying_enemies.append(new_enemy)
                else:
                    ground_enemies.append(new_enemy)
                enemy_spawn_timer = 0

            # Enemy movement
            for enemy_list in [ground_enemies, flying_enemies]:
                for enemy in enemy_list:
                    if enemy["rect"].x < player.rect.x:
                        enemy["rect"].x += ENEMY_SPEED
                    else:
                        enemy["rect"].x -= ENEMY_SPEED

                    # Check collision with player
                    if player.rect.colliderect(enemy["rect"]):
                        player.health -= 1
                        if player.health <= 0:
                            game_over = True

            # Projectile collision
            for proj, _ in player.projectiles[:]:
                for enemy_list in [ground_enemies, flying_enemies]:
                    for enemy in enemy_list:
                        if proj.colliderect(enemy["rect"]):
                            enemy["health"] -= 1
                            if enemy["health"] == 1:
                                enemy["hit_once"] = True
                            elif enemy["health"] <= 0:
                                enemy_list.remove(enemy)
                                score += 10
                            if (proj, _) in player.projectiles:
                                player.projectiles.remove((proj, _))

            # Score timer
            score_timer += dt
            if score_timer >= 1:
                score += 1
                score_timer = 0

        else:
            if keys[pygame.K_r]:
                if score > high_score:
                    high_score = score
                reset_game()

        # Drawing
        screen.fill(BG_COLOR)
        player.draw(screen)

        for proj, _ in player.projectiles:
            pygame.draw.rect(screen, PROJECTILE_COLOR, proj)

        for enemy_list in [ground_enemies, flying_enemies]:
            for enemy in enemy_list:
                color = ENEMY_COLOR if enemy.get("health", 2) == 2 else ENEMY_HIT_COLOR
                pygame.draw.rect(screen, color, enemy["rect"])

        for plat in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, plat)

        draw_score(score, high_score)
        draw_health_bar(player.health)

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
