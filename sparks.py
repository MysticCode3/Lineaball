import pygame
import sys
import math
import random

screen_width = 500
screen_height = 500

green = 150, 200, 20
blue = 67, 84, 255
orange = 255, 165, 0
red = 250, 0, 0
purple = 172, 79, 198
gray = 128, 128, 128
white = 255, 255, 255

cx, cy = 0, 0
mx, my = 0, 0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

sparks = []

speed = 0.1

class Spark():
    def __init__(self, loc, angle, speed, color, scale=1):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def points_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sign = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])

    def move(self, dt):
        global speed
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        #self.points_towards(math.pi / 2, 0.02)
        self.velocity_adjust(0.975, 0.2, 8, dt)
        self.angle += 0.05

        self.speed -= speed

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf, offset=[0, 0]):
        if self.alive:
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale, self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3]
            ]
            pygame.draw.polygon(surf, self.color, points)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cx, cy = pygame.mouse.get_pos()
            print(cx, cy)

    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        pass
    if keys[pygame.K_RIGHT]:
        pass
    if keys[pygame.K_UP]:
        speed -= 0.01
    if keys[pygame.K_DOWN]:
        speed += 0.01
    if keys[pygame.K_1]:
        pygame.quit()

    screen.fill((30, 30, 30))
    font = pygame.font.SysFont("comicsansms", 30)

    for i, spark in sorted(enumerate(sparks), reverse=True):
        spark.move(1)
        spark.draw(screen)
        if not spark.alive:
            sparks.pop(i)

    for i in range(0, 2):
        sparks.append(Spark([mx, my], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))

    fps = font.render(f"FPS: {round(clock.get_fps())}", True, (173, 216, 230))
    screen.blit(fps, (3, 0))
    pygame.display.update()
    clock.tick(120)
