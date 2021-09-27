import pygame
import random

import pics

pygame.init()

display_width = 800
display_height = 532

display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Crazy Beeee')

x = 10
y = 532 - 70
width = 70
height = 70
speed = 5

is_jump = False
jump_count = 11

standL = False
standR = False
left = False
right = False

anim_count = 0
lastMove = "right"

clock = pygame.time.Clock()

run = True
bullets = []


class Bird:
    def __init__(self, away_y, speed, cd_hide):
        self.x = random.randrange(10, 700)
        self.y = away_y
        self.ay = away_y
        self.speed = speed
        self.dest_y = self.speed * random.randrange(50, 70)
        self.img_cnt = 0
        self.cd_hide = cd_hide
        self.come = True
        self.go_away = False

    def draw(self):
        if self.img_cnt == 4:
            self.img_cnt = 0
        if self.x > 350:
            display.blit(pics.BIRD_FLY_LEFT[self.img_cnt // 2], (self.x, self.y))
            self.img_cnt += 1
        else:
            display.blit(pics.BIRD_FLY_RIGHT[self.img_cnt // 2], (self.x, self.y))
            self.img_cnt += 1

        if self.come and self.cd_hide == 0:
            if self.y < self.dest_y:
                self.y += self.speed
            else:
                self.come = False
                self.go_away = True
                self.dest_y = self.ay
        elif self.go_away:
            if self.y > self.dest_y:
                self.y -= self.speed
            else:
                self.come = True
                self.go_away = False
                self.x = random.randrange(10, 700)
                self.dest_y = self.speed * random.randrange(50, 70)
                self.cd_hide = 50
        elif self.cd_hide > 0:
            self.cd_hide -= 1


class Honey:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def usr_animation():
    global anim_count

    if anim_count + 1 >= 30:
        anim_count = 0

    if left:
        display.blit(pics.WALK_LEFT[anim_count // 6], (x, y))
        anim_count += 4

    elif right:
        display.blit(pics.WALK_RIGHT[anim_count // 6], (x, y))
        anim_count += 4

    else:
        if lastMove == "right":
            display.blit(pics.BEE_STAND1, (x, y))

        elif lastMove == "left":
            display.blit(pics.BEE_STAND2, (x, y))


def draw_window():
    display.blit(pics.BG, (0, 0))
    bird1.draw()
    bird2.draw()
    bird3.draw()

    usr_animation()

    for bullet in bullets:
        bullet.draw(display)

    pygame.display.update()


def make_bullet(x, y, width):
    for bullet in bullets:
        if 800 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_f]:
        if lastMove == "right":
            facing = 1
        else:
            facing = -1

        if len(bullets) < 10:
            bullets.append(Honey(round(x + width // 2), round(y + width // 2),
                                 6, (251, 236, 93), facing))


bird1 = Bird(-80, 5, 0)
bird2 = Bird(-90, 6, 70)
bird3 = Bird(-80, 5, 120)

while run:

    clock.tick(100)
    pygame.time.delay(22)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    make_bullet(x, y, width)

    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        standL = True
        standR = False
        lastMove = "left"
    elif keys[pygame.K_RIGHT] and x < 800 - width - 5:
        x += speed
        left = False
        right = True
        standR = True
        standL = False
        lastMove = "right"

    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= - 11:
            if jump_count < 0:
                y += (jump_count ** 2) // 2
            else:
                y -= (jump_count ** 2) // 2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 11

    draw_window()

pygame.quit()
