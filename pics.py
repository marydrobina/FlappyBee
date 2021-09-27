"""pics.py module"""


import pygame

WALK_RIGHT = [pygame.image.load('fpics/r1.png'), pygame.image.load('fpics/r2.png'),
              pygame.image.load('fpics/r3.png'), pygame.image.load('fpics/r4.png'),
              pygame.image.load('fpics/r5.png'), pygame.image.load('fpics/r6.png')]
WALK_LEFT = [pygame.image.load('fpics/l1.png'), pygame.image.load('fpics/l2.png'),
             pygame.image.load('fpics/l3.png'), pygame.image.load('fpics/l4.png'),
             pygame.image.load('fpics/l5.png'), pygame.image.load('fpics/l6.png')]

BIRD_FLY_RIGHT = [pygame.image.load('fpics/f1r.png'), pygame.image.load('fpics/f2r.png')]
BIRD_FLY_LEFT = [pygame.image.load('fpics/f1l.png'), pygame.image.load('fpics/f2l.png')]

BIRD_HIT_RIGHT = [pygame.image.load('fpics/gh1r.png'), pygame.image.load('fpics/gh2r.png')]
BIRD_HIT_LEFT = [pygame.image.load('fpics/gh1l.png'), pygame.image.load('fpics/gh2l.png')]

BG = pygame.image.load('fpics/bg.jpg')
BEE_STAND1 = pygame.image.load('fpics/r1.png')
BEE_STAND2 = pygame.image.load('fpics/l1.png')
