import pygame, random

pygame.init()

display_width = 800
display_height = 532

display = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Crazy Beeee')

walkRight = [pygame.image.load('r1.png'), pygame.image.load('r2.png'),
             pygame.image.load('r3.png'), pygame.image.load('r4.png'),
             pygame.image.load('r5.png'), pygame.image.load('r6.png')]
walkLeft = [pygame.image.load('l1.png'), pygame.image.load('l2.png'),
            pygame.image.load('l3.png'), pygame.image.load('l4.png'),
            pygame.image.load('l5.png'), pygame.image.load('l6.png')]

birdFlyRight = [pygame.image.load('f1r.png'), pygame.image.load('f2r.png')]
birdFlyLeft = [pygame.image.load('f1l.png'), pygame.image.load('f2l.png')]

birdHitRight = [pygame.image.load('gh1r.png'), pygame.image.load('gh2r.png')]
birdHitLeft = [pygame.image.load('gh1l.png'), pygame.image.load('gh2l.png')]

bg = pygame.image.load('bg.jpg')
beeStand1 = pygame.image.load('r1.png')
beeStand2 = pygame.image.load('l1.png')

x = 10
y = 532 - 70
width = 70
height = 70
speed = 5

isJump = False
jumpcount = 11

standL = False
standR = False
left = False
right = False

animcount = 0
lastMove = "right"

clock = pygame.time.Clock()

run = True
bullets = []


class Bird():
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
            display.blit(birdFlyLeft[self.img_cnt // 2], (self.x, self.y))
            self.img_cnt += 1
        else:
            display.blit(birdFlyRight[self.img_cnt // 2], (self.x, self.y))
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


class honey():
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
    global animcount

    if animcount + 1 >= 30:
        animcount = 0

    if left:
        display.blit(walkLeft[animcount // 6], (x, y))
        animcount += 4

    elif right:
        display.blit(walkRight[animcount // 6], (x, y))
        animcount += 4

    else:
        if lastMove == "right":
            display.blit(beeStand1, (x, y))

        elif lastMove == "left":
            display.blit(beeStand2, (x, y))


def drawWindow():
    display.blit(bg, (0, 0))
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
            bullets.append(honey(round(x + width // 2), round(y + width // 2),
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

    if not (isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpcount >= - 11:
            if jumpcount < 0:
                y += (jumpcount ** 2) // 2
            else:
                y -= (jumpcount ** 2) // 2
            jumpcount -= 1
        else:
            isJump = False
            jumpcount = 11

    drawWindow()

pygame.quit()
