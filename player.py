import pygame
from settings import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, FLOOR_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_y = 0
        self.on_ground = True

    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.y >= FLOOR_Y:
            self.rect.y = FLOOR_Y
            self.velocity_y = 0
            self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
