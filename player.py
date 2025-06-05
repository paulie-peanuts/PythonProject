import pygame
import math
from settings import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, FLOOR_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_y = 0
        self.on_ground = True
        self.max_jumps = 2
        self.jumps_left = self.max_jumps
        self.projectiles = []
        self.health = MAX_HEALTH

    def handle_input(self, event_list):
        keys = pygame.key.get_pressed()

        # Left/Right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED

        # Jumping and shooting on keydown
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    if self.jumps_left > 0:
                        self.velocity_y = -JUMP_STRENGTH
                        self.jumps_left -= 1
                if event.key == pygame.K_f:
                    # Shoot toward mouse
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    start_x = self.rect.centerx
                    start_y = self.rect.centery
                    dx = mouse_x - start_x
                    dy = mouse_y - start_y
                    distance = math.hypot(dx, dy)
                    if distance == 0:
                        distance = 1
                    dx /= distance
                    dy /= distance
                    velocity = (dx * PROJECTILE_SPEED, dy * PROJECTILE_SPEED)
                    proj_rect = pygame.Rect(start_x, start_y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                    self.projectiles.append((proj_rect, velocity))  # Store as (Rect, velocity)

    def apply_gravity(self, platforms):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        landed = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.velocity_y > 0 and self.rect.bottom - self.velocity_y <= plat.top:
                    self.rect.bottom = plat.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumps_left = self.max_jumps
                    landed = True

        # Ground check
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.on_ground = True
            self.jumps_left = self.max_jumps
            landed = True

        if not landed:
            self.on_ground = False

    def update_projectiles(self):
        for proj, velocity in self.projectiles[:]:
            proj.x += velocity[0]
            proj.y += velocity[1]
            if proj.right < 0 or proj.left > WIDTH or proj.bottom < 0 or proj.top > HEIGHT:
                self.projectiles.remove((proj, velocity))

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
        for proj, _ in self.projectiles:
            pygame.draw.rect(screen, PROJECTILE_COLOR, proj)
