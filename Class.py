import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
from pygame.locals import *
vec = pg.math.Vector2

WIDTH = 1200
HEIGHT = 800
PLAYER_GRAV = .5

# # define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(Sprite):
    # basic elements of the player
    def __init__(self):
        Sprite.__init__(self)
        # puts the player on the screen and gives it size and color
        self.image = pg.Surface((50, 50))
        self.r = 120
        self.g = 30
        self.b = 80
        self.hitx = 0
        self.hity = 0
        self.colliding = False
        self.image.fill((self.r,self.g,self.b))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.rect.center = (1150, 450)
        self.pos = vec(WIDTH, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.grav = PLAYER_GRAV
    # controls of the game, how the player moves and takes input from person and... 
    # ... then displays that input as feedback on the screen
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.acc.y = -.1
        if keys[pg.K_a]:
            self.acc.x = -.1
        if keys[pg.K_s]:
            self.acc.y = .2
        if keys[pg.K_d]:
            self.acc.x = .2
    # allows the player tp jump up and around blocks.
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, mobs, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -20
    # tells the person where it is on the screen 
    def update(self):
        self.acc = vec(0)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # important for collision code
        self.rect.midbottom = self.pos

class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.initialized = False
# making the platform class customizable so different sizes of it can be made and placed on the screen
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()