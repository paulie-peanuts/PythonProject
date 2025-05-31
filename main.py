import pygame, sys
from settings import *
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebirth")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

player = Player()
# Ground enemy
ground_enemy = {"rect": pygame.Rect(0, FLOOR_Y, ENEMY_WIDTH, ENEMY_HEIGHT), "hit_count": 0, "hit_color_timer": 0}
# Flying enemy - moves horizontally and vertically in a small range
flying_enemy = {
    "rect": pygame.Rect(600, 150, ENEMY_WIDTH, ENEMY_HEIGHT),
    "hit_count": 0,
    "hit_color_timer": 0,
    "vel_x": 2,
    "vel_y": 2,
    "start_x": 600,
    "start_y": 150,
    "range_x": 100,
    "range_y": 60,
}

enemy_speed = 3
score = 0
score_timer = 0
game_over = False
start_screen = True

# Create floating platforms
platforms = [
    pygame.Rect(200, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(150, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
]

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def draw_start_screen():
    screen.fill(BG_COLOR)
    title_text = font.render("Rebirth", True, (255, 255, 255))
    instructions = [
        "Controls:",
        "Move Left/Right: A/D or Left/Right arrows",
        "Jump: Space, W, or Up arrow (double jump)",
        "Aim with mouse",
        "Shoot: F key",
        "Avoid enemies!",
        "Press Enter to Start"
    ]
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    for i, line in enumerate(instructions):
        line_surf = small_font.render(line, True, (200, 200, 200))
        screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, 180 + i * 30))
    pygame.display.flip()

def main():
    global score, score_timer, game_over, enemy_speed, start_screen
    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if start_screen:
            draw_start_screen()
            for event in event_list:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    start_screen = False
            continue

        if not game_over:
            player.handle_input(event_list)
            player.apply_gravity(platforms)
            player.update_projectiles()

            # Ground enemy movement (follows player x)
            if ground_enemy["rect"].x < player.rect.x:
                ground_enemy["rect"].x += enemy_speed
            elif ground_enemy["rect"].x > player.rect.x:
                ground_enemy["rect"].x -= enemy_speed

            # Flying enemy movement (moves in a rectangle)
            flying_enemy["rect"].x += flying_enemy["vel_x"]
            flying_enemy["rect"].y += flying_enemy["vel_y"]
            if abs(flying_enemy["rect"].x - flying_enemy["start_x"]) > flying_enemy["range_x"]:
                flying_enemy["vel_x"] *= -1
            if abs(flying_enemy["rect"].y - flying_enemy["start_y"]) > flying_enemy["range_y"]:
                flying_enemy["vel_y"] *= -1

            # Enemy hit color timers decrement
            for enemy in (ground_enemy, flying_enemy):
                if enemy["hit_color_timer"] > 0:
                    enemy["hit_color_timer"] -= dt
                else:
                    enemy["hit_color_timer"] = 0

            # Check projectile collisions for both enemies
            for projectile in player.projectiles[:]:
                for enemy in (ground_enemy, flying_enemy):
                    if projectile["rect"].colliderect(enemy["rect"]):
                        player.projectiles.remove(projectile)
                        enemy["hit_count"] += 1
                        enemy["hit_color_timer"] = 0.5  # half second highlight
                        if enemy["hit_count"] >= 2:
                            # Respawn enemy
                            if enemy is ground_enemy:
                                enemy["rect"].x = 0
                            else:
                                enemy["rect"].x = enemy["start_x"]
                                enemy["rect"].y = enemy["start_y"]
                            enemy["hit_count"] = 0

            # Check collision with player
            if player.rect.colliderect(ground_enemy["rect"]) or player.rect.colliderect(flying_enemy["rect"]):
                game_over = True

            # Score increase
            score_timer += dt
            if score_timer >= 1:
                score += 1
                score_timer = 0

        else:
            if keys[pygame.K_r]:
                player.__init__()
                ground_enemy["rect"].x = 0
                ground_enemy["hit_count"] = 0
                ground_enemy["hit_color_timer"] = 0
                flying_enemy["rect"].x = flying_enemy["start_x"]
                flying_enemy["rect"].y = flying_enemy["start_y"]
                flying_enemy["hit_count"] = 0
                flying_enemy["hit_color_timer"] = 0
                score = 0
                score_timer = 0
                game_over = False

        # Draw everything
        screen.fill(BG_COLOR)
        player.draw(screen)

        # Draw enemies with hit color
        for enemy in (ground_enemy, flying_enemy):
            color = (255, 255, 0) if enemy["hit_color_timer"] > 0 else ENEMY_COLOR
            pygame.draw.rect(screen, color, enemy["rect"])

        for plat in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, plat)

        # Draw projectiles
        for projectile in player.projectiles:
            pygame.draw.rect(screen, (255, 255, 255), projectile["rect"])

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
