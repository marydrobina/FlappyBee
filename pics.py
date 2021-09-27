"""pics.py module"""


import pygame

WALK_RIGHT = [pygame.image.load('assets/r1.png'), pygame.image.load('assets/r2.png'),
              pygame.image.load('assets/r3.png'), pygame.image.load('assets/r4.png'),
              pygame.image.load('assets/r5.png'), pygame.image.load('assets/r6.png')]
WALK_LEFT = [pygame.image.load('assets/l1.png'), pygame.image.load('assets/l2.png'),
             pygame.image.load('assets/l3.png'), pygame.image.load('assets/l4.png'),
             pygame.image.load('assets/l5.png'), pygame.image.load('assets/l6.png')]

BIRD_FLY_RIGHT = [pygame.image.load('assets/f1r.png'), pygame.image.load('assets/f2r.png')]
BIRD_FLY_LEFT = [pygame.image.load('assets/f1l.png'), pygame.image.load('assets/f2l.png')]

BIRD_HIT_RIGHT = [pygame.image.load('assets/gh1r.png'), pygame.image.load('assets/gh2r.png')]
BIRD_HIT_LEFT = [pygame.image.load('assets/gh1l.png'), pygame.image.load('assets/gh2l.png')]

BG = pygame.image.load('assets/bg.jpg')
BEE_STAND1 = pygame.image.load('assets/r1.png')
BEE_STAND2 = pygame.image.load('assets/l1.png')
