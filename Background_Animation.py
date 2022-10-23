import pygame
import random

class animation():
    def __init__(self):
        self.x = random.randint(0, 550)
        self.y = random.randint(-500, 0)
        self.width = random.randint(0, 120)
        self.height = random.randint(0, 120)
        self.border = random.randint(1, 2)
        self.vel = random.randint(1, 2)

    def draw(self, screen):
        pygame.draw.rect(screen, (173, 216, 230), (self.x, self.y, self.width, self.height), self.border, border_radius=5)

    def update(self):
        self.y += self.vel/2
        if self.y > 810:
            self.x = random.randint(0, 550)
            self.y = random.randint(-500, 0)
            self.width = random.randint(0, 120)
            self.height = random.randint(0, 120)
            self.border = random.randint(1, 2)
            self.vel = random.randint(2, 3)