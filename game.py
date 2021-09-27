import pygame
import random

import pics


class Bird:
    def __init__(
            self,
            away_y: int,
            speed: int,
            cd_hide: int):
        self.x = random.randrange(10, 700)
        self.y = away_y
        self.ay = away_y
        self.speed = speed
        self.dest_y = self.speed * random.randrange(50, 70)
        self.img_cnt = 0
        self.cd_hide = cd_hide
        self.come = True
        self.go_away = False

    def draw(self, display: pygame.Surface):
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
    def __init__(
            self,
            x: int,
            y: int,
            radius: int,
            color: tuple,
            facing: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Game:

    def __init__(self, display_width: int, display_height: int):
        self.display = pygame.display.set_mode((display_width, display_height))
        self.coordinates = (10, display_height - 70)
        self.size = {'width': 70, 'height': 70}
        self.directions = {'left': False, 'right': False}
        self.speed = 5
        self.is_jump = False
        self.jump_count = 11
        self.standL = False
        self.standR = False
        self.anim_count = 0
        self.last_move = "right"
        self.clock = pygame.time.Clock()
        self.run = True
        self.bullets = list()

    def usr_animation(self):
        if self.anim_count + 1 >= 30:
            self.anim_count = 0
        if self.directions['left']:
            self.display.blit(pics.WALK_LEFT[self.anim_count // 6], self.coordinates)
            self.anim_count += 4
        elif self.directions['right']:
            self.display.blit(pics.WALK_RIGHT[self.anim_count // 6], self.coordinates)
            self.anim_count += 4
        else:
            if self.last_move == "right":
                self.display.blit(pics.BEE_STAND1, self.coordinates)

            elif self.last_move == "left":
                self.display.blit(pics.BEE_STAND2, self.coordinates)

    def draw_window(self, birds: tuple):
        self.display.blit(pics.BG, (0, 0))
        bird1, bird2, bird3 = birds
        bird1.draw()
        bird2.draw()
        bird3.draw()

        self.usr_animation()

        for bullet in self.bullets:
            bullet.draw(self.display)

        pygame.display.update()

    def make_bullet(self):
        for bullet in self.bullets:
            if 800 > bullet.x > 0:
                bullet.x += bullet.vel
            else:
                self.bullets.pop(self.bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_f]:
            if self.last_move == "right":
                facing = 1
            else:
                facing = -1

            if len(self.bullets) < 10:
                x = self.coordinates[0]
                y = self.coordinates[1]
                self.bullets.append(
                    Honey(
                        round(x + self.size['width'] // 2),
                        round(y + self.size['width'] // 2),
                        6,
                        (251, 236, 93),
                        facing))

    def run_game(self):
        bird1 = Bird(-80, 5, 0)
        bird2 = Bird(-90, 6, 70)
        bird3 = Bird(-80, 5, 120)

        while self.run:

            self.clock.tick(100)
            pygame.time.delay(22)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            self.make_bullet()
            x = self.coordinates[0]

            if keys[pygame.K_LEFT] and x > 5:
                x -= self.speed
                self.directions['left'] = True
                self.directions['right'] = False
                self.standL = True
                self.standR = False
                self.last_move = "left"
            elif keys[pygame.K_RIGHT] and x < 800 - self.size['width'] - 5:
                x += self.speed
                self.directions['left'] = False
                self.directions['right'] = True
                self.standR = True
                self.standL = False
                self.last_move = "right"

            if not self.is_jump:
                if keys[pygame.K_SPACE]:
                    self.is_jump = True
            else:
                y = self.coordinates[1]
                if self.jump_count >= - 11:
                    if self.jump_count < 0:
                        y += (self.jump_count ** 2) // 2
                    else:
                        y -= (self.jump_count ** 2) // 2
                    self.jump_count -= 1
                else:
                    self.is_jump = False
                    self.jump_count = 11

            self.draw_window((bird1, bird2, bird3))


def main():
    pygame.init()
    pygame.display.set_caption('Crazy Beeee')
    display_width = 800
    display_height = 532
    game = Game(
        display_width=display_width,
        display_height=display_height)
    game.run_game()
    pygame.quit()


if __name__ == '__main__':
    main()
