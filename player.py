import pygame
from settings import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, FLOOR_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_y = 0
        self.on_ground = True
        self.max_jumps = 2
        self.jumps_left = self.max_jumps

    def handle_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    if self.jumps_left > 0:
                        self.velocity_y = JUMP_STRENGTH
                        self.jumps_left -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= FLOOR_Y:
            self.rect.y = FLOOR_Y
            self.velocity_y = 0
            self.on_ground = True
            self.jumps_left = self.max_jumps
        else:
            self.on_ground = False

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
