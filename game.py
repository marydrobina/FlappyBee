import pygame
import random

import config
import pics


class Bird:
    def __init__(
            self,
            first_position_y: int,
            speed: int,
            next_birds_appearance_latency: int):
        self.x = random.randrange(10, 700)
        self.y = first_position_y
        self.first_position_y = first_position_y
        self.speed = speed
        self.dest_y = self.speed * random.randrange(50, 70)
        self.wings_animation_iterator = 0
        self.next_birds_appearance_latency = next_birds_appearance_latency
        self.come_down = True
        self.go_away_up = False
        self.is_hit = False

    def wings_animation_process(self, display: pygame.Surface) -> None:
        if self.wings_animation_iterator == 4:
            self.wings_animation_iterator = 0
        if self.x > 350:
            display.blit(
                pics.BIRD_FLY_LEFT[self.wings_animation_iterator // 2]
                if not self.is_hit else
                pics.BIRD_HIT_LEFT[self.wings_animation_iterator // 2],
                (self.x, self.y)
            )
            self.wings_animation_iterator += 1
        else:
            display.blit(
                pics.BIRD_FLY_RIGHT[self.wings_animation_iterator // 2]
                if not self.is_hit else
                pics.BIRD_HIT_RIGHT[self.wings_animation_iterator // 2],
                (self.x, self.y)
            )
            self.wings_animation_iterator += 1

    def going_down(self) -> None:
        if self.y < self.dest_y:
            self.y += self.speed
        else:
            self.come_down = False
            self.go_away_up = True
            self.dest_y = self.first_position_y

    def going_up(self) -> None:
        if self.y > self.dest_y:
            self.y -= self.speed
        else:
            self.come_down = True
            self.go_away_up = False
            self.is_hit = False
            self.x = random.randrange(10, 700)
            self.dest_y = self.speed * random.randrange(50, 70)
            self.next_birds_appearance_latency = 50

    def draw(self, display: pygame.Surface) -> None:
        self.wings_animation_process(display)
        if self.come_down and self.next_birds_appearance_latency == 0:
            self.going_down()
        elif self.go_away_up:
            self.going_up()
        elif self.next_birds_appearance_latency > 0:
            self.next_birds_appearance_latency -= 1


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
        self.coordinates = {'x': 10, 'y': display_height - 70}
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
        self.score = 0
        self.font = pygame.font.SysFont("calibri", 32)

    def coordinates_tuple(self) -> tuple:
        return self.coordinates['x'], self.coordinates['y']

    def show_score(self, x: int, y: int) -> None:
        score = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.display.blit(score, (x, y))

    def usr_animation(self) -> None:
        if self.anim_count + 1 >= 30:
            self.anim_count = 0
        if self.directions['left']:
            self.display.blit(pics.WALK_LEFT[self.anim_count // 6], self.coordinates_tuple())
            self.anim_count += 4
        elif self.directions['right']:
            self.display.blit(pics.WALK_RIGHT[self.anim_count // 6], self.coordinates_tuple())
            self.anim_count += 4
        else:
            if self.last_move == "right":
                self.display.blit(pics.BEE_STAND1, self.coordinates_tuple())
            elif self.last_move == "left":
                self.display.blit(pics.BEE_STAND2, self.coordinates_tuple())

    def draw_window(self, birds: tuple) -> None:
        self.display.blit(pics.BG, (0, 0))
        bird1, bird2, bird3 = birds
        for bird in (bird1, bird2, bird3):
            bird.draw(display=self.display)
        self.usr_animation()
        for bullet in self.bullets:
            bullet.draw(self.display)
        self.collision(birds=[bird1, bird2, bird3])
        self.show_score(config.DISPLAY_WIDTH - 150, 10)
        pygame.display.update()

    def bullet_move(self) -> None:
        for bullet in self.bullets:
            if 800 > bullet.x > 0:
                bullet.x += bullet.vel
            else:
                self.bullets.pop(self.bullets.index(bullet))

    def get_bullet_direction(self) -> int:
        if self.last_move == "right":
            facing = 1
        else:
            facing = -1
        return facing

    def make_bullet(self) -> None:
        self.bullet_move()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            facing = self.get_bullet_direction()
            if len(self.bullets) < 10:
                self.bullets.append(
                    Honey(
                        x=round(self.coordinates['x'] + self.size['width'] // 2),
                        y=round(self.coordinates['y'] + self.size['width'] // 2),
                        radius=6,
                        color=(251, 236, 93),
                        facing=facing
                    )
                )

    def stop_game_btn_check(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def move_bee_left(self) -> None:
        self.coordinates['x'] -= self.speed
        self.directions['left'] = True
        self.directions['right'] = False
        self.standL = True
        self.standR = False
        self.last_move = "left"

    def move_bee_right(self) -> None:
        self.coordinates['x'] += self.speed
        self.directions['left'] = False
        self.directions['right'] = True
        self.standR = True
        self.standL = False
        self.last_move = "right"

    def game_state_setup(self) -> None:
        self.clock.tick(100)
        pygame.time.delay(22)
        self.stop_game_btn_check()

    def direction_moves(self, keys) -> None:
        if keys[pygame.K_LEFT] and self.coordinates['x'] > 5:
            self.move_bee_left()
        elif keys[pygame.K_RIGHT] and self.coordinates['x'] < 800 - self.size['width'] - 5:
            self.move_bee_right()

    def jump_move(self) -> None:
        if self.jump_count < 0:
            self.coordinates['y'] += (self.jump_count ** 2) // 2
        else:
            self.coordinates['y'] -= (self.jump_count ** 2) // 2
        self.jump_count -= 1

    def processing_jump(self) -> None:
        if self.jump_count >= -11:
            self.jump_move()
        else:
            self.is_jump = False
            self.jump_count = 11

    def all_moves(self):
        keys = pygame.key.get_pressed()
        self.make_bullet()
        self.direction_moves(keys)
        if not self.is_jump:
            if keys[pygame.K_SPACE]:
                self.is_jump = True
        else:
            self.processing_jump()

    def collision(self, birds: list) -> None:
        for bird in birds:
            for bullet in self.bullets:
                bird_left_border = bird.x - 47
                bird_right_border = bird.x + 47
                bird_top_border = bird.y - 40
                bird_bottom_border = bird.y + 40
                if bird_left_border < bullet.x < bird_right_border \
                        and bird_top_border < bullet.y < bird_bottom_border\
                        and not bird.is_hit:
                    self.bullets.pop(self.bullets.index(bullet))
                    bird.is_hit = True
                    self.score += 1

    def run_game(self) -> None:
        bird1 = Bird(-80, 5, 0)
        bird2 = Bird(-90, 6, 70)
        bird3 = Bird(-80, 5, 120)
        while self.run:
            self.game_state_setup()
            self.all_moves()
            self.draw_window((bird1, bird2, bird3))


def main():
    pygame.init()
    pygame.display.set_caption('Crazy Beeee')
    Game(
        display_width=config.DISPLAY_WIDTH,
        display_height=config.DISPLAY_HEIGHT
    ).run_game()
    pygame.quit()


if __name__ == '__main__':
    main()
