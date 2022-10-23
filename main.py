#Total 482 Lines Of Code
#<link rel="stylesheet" href="Downloads/pyscript-main/pyscriptjs/src/styles/pyscript_base.css" />
#<script defer src="Downloads/pyscript-main/pyscriptjs/src/pyscript.js"></script>

#Imports
import sys
import pygame
from pygame import *
import time
from win32api import GetSystemMetrics
import Line
import Dot
import Line_Animation
from pygame import mixer
import Background_Animation
import sparks_game
import math
import random
import Red_Line

#Screen Dimensions
#screen_width = GetSystemMetrics(0)
#screen_height = GetSystemMetrics(1)

#screen_width = 550
screen_width = 550
screen_height = 800

#Colors
green = 150, 200, 20
blue = 67, 84, 255
orange = 255, 165, 0
red = 250, 0, 0
purple = 172, 79, 198
gray = 128, 128, 128
white = 255, 255, 255
black = 0, 0, 0

#Mouse Variables
cx, cy = (0, 0)
mx, my = (0, 0)

#Lines Variables
x, y = screen_width/2, screen_height
x2, y2 = 0, 0

#Ball Variables
bx, by = screen_width/2, screen_height/2

#Collision Variables
collide = False

#Velocity For Ball
opp_rec_glob = 0
bx_vel = 0
by_vel = 0
gravity = 3
up = 0

#Game Event Variables
game_start = False
end = False

#Point Variables
points = 0
high_score = 0

#Lists
line_list = []
dot_list = []
animation_list = []
sparks = []
red_list = []

#Background Variables
background_darkness = 35
dark_amount = 0
b_animation_list = []
background_set = False

#Start Screen Variables
start_screen = True

#Sound Variables
sound = True

#Death Animation Variables
max_size = 2000
size = 10
width = 1

#Logo
Logo = pygame.image.load("Logo_LineaBall.png")

#Delta Time
last_time = time.time()
dt = 0

#Red Line
red_collide = False

#Ball Effect
def circle_surf(radius, color):
    surf = pygame.Surface((radius *2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

#Draw Background
def draw_background():
    global background_set
    global b_animation_list

    s_2 = pygame.Surface((550, 800), pygame.SRCALPHA)

    if background_set == False:
        background_set = True
        for i in range(0, 10):
            b_animation_list.append(Background_Animation.animation())
    for animation_obj in b_animation_list:
        animation_obj.draw(s_2)
        animation_obj.update()
        screen.blit(circle_surf(animation_obj.width, (10, 10, 10)), (animation_obj.x - animation_obj.width + animation_obj.width/2, animation_obj.y - animation_obj.width + animation_obj.height/2), special_flags=BLEND_RGB_ADD)

    s_2.set_alpha(128)
    screen.blit(s_2, (0, 0))

#Death Animation Function
def death_animation():
    global max_size
    global size
    global width

    pygame.draw.circle(screen, red, (bx, by), size, width)
    pygame.draw.circle(screen, red, (bx, by), size/2, width)
    if size < max_size:
        size += width
        width += 1
    if size < max_size/10:
        sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(120, 360)), random.randint(3, 6), red, 1))
    if width < 3:
        pygame.mixer.Sound.play(death_sound)

#Title Screen
def draw_title():
    global sound
    global start_screen

    width = 300
    height = 100

    offset_x = 0
    offset_y = 0

    if 426 > mx > 126:
        if 700 > my > 600:
            if sound:
                sound = False
                pygame.mixer.Sound.play(click_sound)
            width = 320
            height = 120
            offset_x = 10
            offset_y = 10
        else:
            sound = True
    else:
        sound = True

    if 426 > cx > 126:
        if 700 > cy > 600:
                start_screen = False

    s = pygame.Surface((550, 800), pygame.SRCALPHA)

    pygame.draw.rect(s, (173, 216, 230), (0, 0, 400, 100), border_radius=40)
    pygame.draw.rect(s, (173, 216, 230), (50 - offset_x, 500 - offset_y, width, height), border_radius=40)
    s.set_alpha(128)
    screen.blit(s, (screen_width/2 - 200, 100))

    font = pygame.font.SysFont("Bahnschrift", 75)

    title_text = font.render("Lineaball", bool(1), (173, 216, 230))
    screen.blit(title_text, (screen_width/2 - title_text.get_width()/2, 115))

    name = font_small.render("Rohan Saxena", bool(1), (173, 216, 230))
    screen.blit(name, (screen_width / 2 - name.get_width() / 2, 200))

    play_button = font.render("Play", bool(1), (173, 216, 230))
    screen.blit(play_button, (screen_width / 2 - play_button.get_width() / 2, 615))

#Collision Detection Between The Ball and The Red Line
def check_red(a, b, c):
    global game_start
    global  end

    slope_1 = 0
    slope_2 = 0

    if (b[0] - a[0]) != 0:
        slope_1 = (b[1] - a[1])/(b[0] - a[0])
        slope_2 = (b[1] - c[1])/(b[0]-c[0])

    if (b[0] - a[0]) == 0:
        return False

    if abs(slope_2-slope_1) <= 0.1:
        if a[0] < b[0]:
            if c[0] > a[0]:
                if c[0] < b[0]:
                    game_start = False
                    end = True
                    return True
                else:
                    return False
            else:
                return False
        elif b[0] < a[0]:
            if c[0] > b[0] :
                if c[0] < a[0]:
                    game_start = False
                    end = True
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False

#Collision Detection Between The Ball and The Lines
def check_collision(a, b, c):
    global points

    slope_1 = 0
    slope_2 = 0

    if (b[0] - a[0]) != 0:
        slope_1 = (b[1] - a[1])/(b[0] - a[0])
        slope_2 = (b[1] - c[1])/(b[0]-c[0])

    if (b[0] - a[0]) == 0:
        return False, opp_rec_glob

    if abs(slope_2-slope_1) <= 0.1:
        if a[0] < b[0]:
            if c[0] > a[0]:
                if c[0] < b[0]:
                    points += 1
                    pygame.mixer.Sound.play(ball_sound)
                    for i in range(0, 15):
                        #animation_list.append(Line_Animation.dot_anim(bx, by, (67, 84, 255), 0.01, 14))
                        sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(0, 360)), random.randint(3, 6), blue, 2))
                    return True, opp_rec_glob + (slope_1 * 6)
                else:
                    return False, opp_rec_glob
            else:
                return False, opp_rec_glob
        elif b[0] < a[0]:
            if c[0] > b[0] :
                if c[0] < a[0]:
                    points += 1
                    pygame.mixer.Sound.play(ball_sound)
                    for i in range(0, 15):
                        #animation_list.append(Line_Animation.dot_anim(bx, by, (67, 84, 255), 0.01, 14))
                        sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(0, 360)), random.randint(3, 6), blue, 2))
                    return True, opp_rec_glob + (slope_1 * 6)
                else:
                    return False, opp_rec_glob
            else:
                return False, opp_rec_glob
    else:
        return False, opp_rec_glob

#Usual Pygame Stuff
mixer.init()
pygame.init()
pygame.display.set_caption('LineaBall')
pygame.display.set_icon(Logo)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

#Cursor
pygame.mouse.set_visible(False)

#Main Music
#Music: Downtown Glow by Ghostrifter Official
mixer.music.load("lineaball_music_1.mp3")
mixer.music.set_volume(1)

ball_sound = pygame.mixer.Sound("ball_tap.wav")
click_sound = pygame.mixer.Sound("click.wav")
restart_sound = pygame.mixer.Sound("restart.wav")
death_sound = pygame.mixer.Sound("death_sound.mp3")

pygame.mixer.Sound.set_volume(ball_sound, 1)
pygame.mixer.Sound.set_volume(click_sound, 0.5)
pygame.mixer.Sound.set_volume(restart_sound, 0.2)
pygame.mixer.Sound.set_volume(death_sound, 1)

mixer.music.play(-1)

#Red Line
for i in range(0, 3):
    red_list.append(Red_Line.RED_LINE(screen_width, -2000))

#Event Loop
while True:

    #Delta Time
    dt = time.time() - last_time
    dt *= 130
    last_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cx, cy = pygame.mouse.get_pos()
            # print(cx, cy)
            if start_screen == False:
                if end == False:
                    pygame.mixer.Sound.play(click_sound)
                    game_start = True
                    if (x, y) == (0, 0):
                        (x, y) = (cx, cy)
                    else:
                        (x2, y2) = (cx, cy)
                        line_list.append(Line.LINE((x, y), (x2, y2)))
                        (x, y) = (x2, y2)

        mx, my = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    #Restart
    if keys[pygame.K_r]:
        if end:
            pygame.mixer.Sound.play(restart_sound)
            line_list.clear()
            dot_list.clear()
            animation_list.clear()
            points = 0
            x, y = screen_width / 2, screen_height
            x2, y2 = 0, 0
            bx, by = screen_width / 2, screen_height / 2
            bx_vel = 0
            by_vel = 0
            end = False
            opp_rec_glob = 0
            for line_obj in line_list:
                line_obj.restart()
            game_start = False
            max_size = 2000
            size = 10
            width = 1
            for red_line_obj in red_list:
                red_line_obj.reset()
            red_collide = False

    #Background
    screen.fill((0, 4, background_darkness - dark_amount))
    draw_background()

    #Fonts
    font = pygame.font.SysFont("twcencondensedextra", 60)
    font_small = pygame.font.SysFont("twcencondensedextra", 20)

    #Decoration
    #sparks.append(sparks_game.Spark([screen_width/2, -100], math.radians(random.randint(0, 360)), random.randint(3, 6), gray, 2))

    #Main Game Calculations
    if game_start:
        y += (Line.vel * dt)
        by += (gravity * dt)
        bx += (bx_vel * dt)
        by += (by_vel * dt)

        if collide:
            up = 9

        if up > 0:
            up -= 0.1

        by -= up * dt

        dot_list.append(Dot.PATH(bx, by))

        for dot in dot_list:
            dot.draw(screen)
            dot.update()
            if dot.width < 1:
                dot_list.remove(dot)

        for line_obj in line_list:
            line_obj.draw(screen)
            line_obj.update(screen, dt)
            #sparks.append(sparks_game.Spark([line_obj.second_x, line_obj.second_y], math.radians(random.randint(0, 360)), random.randint(1, 2), white, 1))
            screen.blit(circle_surf(12, (20, 20, 20)), (line_obj.second_x - 12, line_obj.second_y - 12), special_flags=BLEND_RGB_ADD)
            screen.blit(circle_surf(15, (20, 20, 20)), (line_obj.second_x - 15, line_obj.second_y - 15), special_flags=BLEND_RGB_ADD)
            screen.blit(circle_surf(18, (20, 20, 20)), (line_obj.second_x - 18, line_obj.second_y - 18), special_flags=BLEND_RGB_ADD)
            screen.blit(circle_surf(21, (20, 20, 20)), (line_obj.second_x - 21, line_obj.second_y - 21), special_flags=BLEND_RGB_ADD)
            screen.blit(circle_surf(24, (20, 20, 20)), (line_obj.second_x - 24, line_obj.second_y - 24), special_flags=BLEND_RGB_ADD)
            screen.blit(circle_surf(27, (20, 20, 20)), (line_obj.second_x - 27, line_obj.second_y - 27), special_flags=BLEND_RGB_ADD)
            screen.blit(circle_surf(30, (20, 20, 20)), (line_obj.second_x - 30, line_obj.second_y - 30), special_flags=BLEND_RGB_ADD)

            #screen.blit(circle_surf(33, (20, 20, 20)), (line_obj.second_x - 33, line_obj.second_y - 33), special_flags=BLEND_RGB_ADD)
            #screen.blit(circle_surf(36, (20, 20, 20)), (line_obj.second_x - 36, line_obj.second_y - 36), special_flags=BLEND_RGB_ADD)
            #screen.blit(circle_surf(39, (20, 20, 20)), (line_obj.second_x - 39, line_obj.second_y - 39), special_flags=BLEND_RGB_ADD)
            #screen.blit(circle_surf(42, (20, 20, 20)), (line_obj.second_x - 42, line_obj.second_y - 42), special_flags=BLEND_RGB_ADD)
            #screen.blit(circle_surf(55, (20, 20, 20)), (line_obj.second_x - 55, line_obj.second_y - 55), special_flags=BLEND_RGB_ADD)
            #screen.blit(circle_surf(80, (20, 20, 20)), (line_obj.second_x - 80, line_obj.second_y - 80), special_flags=BLEND_RGB_ADD)

            collide, opp_rec_glob = check_collision((line_obj.first_x, line_obj.first_y), (line_obj.second_x, line_obj.second_y), (bx, by))
            if int(line_obj.first_y) > screen_height & int(line_obj.second_y) > screen_height:
                line_list.remove(line_obj)

            bx_vel = opp_rec_glob

            # Draw Red Line As Enemy
        for red_line_obj in red_list:
            red_line_obj.draw(screen)
            red_line_obj.update(screen_height, dt)
            if red_collide == False:
                red_collide = check_red((red_line_obj.x, red_line_obj.y), (red_line_obj.x + 100, red_line_obj.y + 100), (bx, by))

        for animation in animation_list:
            animation.draw(screen)
            animation.update()
            if animation.width < 1:
                animation_list.remove(animation)

    for i, spark in sorted(enumerate(sparks), reverse=True):
        spark.move(1)
        spark.draw(screen)
        if spark.color == gray:
            screen.blit(circle_surf(10, (20, 20, 20)), (spark.loc[0] - 10, spark.loc[1] - 10), special_flags=BLEND_RGB_ADD)
        if not spark.alive:
            sparks.pop(i)

    #Draw Main Circle
    pygame.draw.circle(screen, blue, (bx, by), 10)
    screen.blit(circle_surf(12, (20, 20, 20)), (bx-12, by - 12), special_flags=BLEND_RGB_ADD)
    screen.blit(circle_surf(15, (20, 20, 20)), (bx - 15, by - 15), special_flags=BLEND_RGB_ADD)
    screen.blit(circle_surf(18, (20, 20, 20)), (bx - 18, by - 18), special_flags=BLEND_RGB_ADD)
    screen.blit(circle_surf(21, (20, 20, 20)), (bx - 21, by - 21), special_flags=BLEND_RGB_ADD)
    #screen.blit(circle_surf(24, (20, 20, 20)), (bx - 24, by - 24), special_flags=BLEND_RGB_ADD)
    #screen.blit(circle_surf(27, (20, 20, 20)), (bx - 27, by - 27), special_flags=BLEND_RGB_ADD)
    #screen.blit(circle_surf(30, (20, 20, 20)), (bx - 30, by - 30), special_flags=BLEND_RGB_ADD)
    #screen.blit(circle_surf(33, (20, 20, 20)), (bx - 33, by - 33), special_flags=BLEND_RGB_ADD)
    #screen.blit(circle_surf(35, (20, 20, 20)), (bx - 35, by - 35), special_flags=BLEND_RGB_ADD)

    #If Death Occurs
    score_shader = font.render(str(points), True, (173, 216, 230))
    screen.blit(score_shader, (screen_width / 2 - (score_shader.get_width() / 2) + 1, screen_height / 10))

    score = font.render(str(points), True, (67, 84, 255))
    screen.blit(score, (screen_width / 2 - (score.get_width() / 2) - 1, screen_height / 10))

    restart = font.render("Click 'R' to restart", True, (67, 84, 255))
    final_score = font.render(f"High Score: {high_score}", True, (67, 84, 255))

    restart_shader = font.render("Click 'R' to restart", True, (173, 216, 230))
    final_score_shader = font.render(f"High Score: {high_score}", True, (173, 216, 230))

    if end:
        screen.blit(restart_shader, (screen_width / 2 - (restart.get_width() / 2) + 1, screen_height / 5 + 50))
        screen.blit(final_score_shader, (screen_width / 2 - (final_score.get_width() / 2) + 1, screen_height / 3))

        screen.blit(restart, (screen_width / 2 - (restart.get_width() / 2) - 1, screen_height / 5 + 50))
        screen.blit(final_score, (screen_width / 2 - (final_score.get_width() / 2) - 1, screen_height / 3))

    #Check Death
    if bx < 0:
        game_start = False
        end = True
        death_animation()
    elif bx > screen_width:
        game_start = False
        end = True
        death_animation()
    elif by > screen_height:
        game_start = False
        end = True
        death_animation()
    elif red_collide:
        death_animation()

    #Points
    if points < 34:
        dark_amount = points
    else:
        dark_amount = 35

    if points > high_score:
        high_score = points

    #Cursor Hover
    pygame.draw.line(screen, (150, 150, 150), (x, y), (mx, my), 2)
    pygame.draw.circle(screen, (150, 150, 150), (mx, my), 10)
    pygame.draw.circle(screen, (150, 150, 150), (mx, my), 20, 1)

    #Start Screen
    if start_screen:
        screen.fill((0, 4, 35))
        pygame.draw.circle(screen, (150, 150, 150), (mx, my), 7)
        pygame.draw.circle(screen, (150, 150, 150), (mx, my), 10, 1)
        draw_title()

    #FPS and DT
    fps = font_small.render(f"FPS: {round(clock.get_fps())}", True, (173, 216, 230))
    dt = font_small.render(f"DT: {round(dt, 4)}", True, (173, 216, 230))
    screen.blit(fps, (3, 0))
    screen.blit(dt, (3, 20))
    pygame.display.update()
    clock.tick(130)
