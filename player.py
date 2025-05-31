import pygame
from settings import *
import math

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, FLOOR_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_y = 0
        self.on_ground = True
        self.max_jumps = 2
        self.jumps_left = self.max_jumps
        self.projectiles = []

    def handle_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    if self.jumps_left > 0:
                        self.velocity_y = JUMP_STRENGTH
                        self.jumps_left -= 1
                if event.key == pygame.K_f:
                    # Shoot projectile aiming towards mouse position
                    mx, my = pygame.mouse.get_pos()
                    px = self.rect.centerx
                    py = self.rect.centery
                    dx = mx - px
                    dy = my - py
                    dist = math.hypot(dx, dy)
                    if dist == 0:
                        dist = 1
                    dx /= dist
                    dy /= dist
                    speed = 10
                    vel_x = dx * speed
                    vel_y = dy * speed
                    # Create projectile rect and velocity tuple
                    projectile = {"rect": pygame.Rect(px, py, 10, 5), "vel": (vel_x, vel_y)}
                    self.projectiles.append(projectile)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5

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
        for projectile in self.projectiles[:]:
            rect = projectile["rect"]
            vel_x, vel_y = projectile["vel"]
            rect.x += vel_x
            rect.y += vel_y

            # Remove if off-screen
            if rect.right < 0 or rect.left > WIDTH or rect.bottom < 0 or rect.top > HEIGHT:
                self.projectiles.remove(projectile)

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
