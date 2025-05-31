import pygame, sys, random
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

# Create floating platforms
platforms = [
    pygame.Rect(200, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(150, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
]

# Flying enemy class
class FlyingEnemy:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - ENEMY_WIDTH),
            random.randint(100, 300),
            ENEMY_WIDTH,
            ENEMY_HEIGHT
        )
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-1.5, 1.5])
        self.direction_y = 1

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y * self.direction_y

        # Bounce vertically
        if self.rect.top <= 50 or self.rect.bottom >= 350:
            self.direction_y *= -1

        # Wrap around screen horizontally
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 100, 100), self.rect)

# Track high score
def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

high_score = load_high_score()

def draw_score(score, high_score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    screen.blit(high_score_text, (10, 40))

def main():
    global score, score_timer, game_over, high_score
    running = True
    flying_enemies = [FlyingEnemy() for _ in range(2)]

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

            # Flying enemies
            for f_enemy in flying_enemies:
                f_enemy.update()
                if player.rect.colliderect(f_enemy.rect):
                    game_over = True
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)

            # Score
            score_timer += dt
            if score_timer >= 1:
                score += 1
                score_timer = 0
        else:
            if keys[pygame.K_r]:
                player.__init__()
                enemy.x = 0
                score = 0
                score_timer = 0
                game_over = False
                flying_enemies = [FlyingEnemy() for _ in range(2)]

        # Draw
        screen.fill(BG_COLOR)
        player.draw(screen)
        pygame.draw.rect(screen, ENEMY_COLOR, enemy)

        for plat in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, plat)

        for f_enemy in flying_enemies:
            f_enemy.draw(screen)

        draw_score(score, high_score)

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
