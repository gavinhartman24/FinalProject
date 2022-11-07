# Cited: Mr. Cozorts library 

# I am trying to make a game that allows for a player to move around the screen over platforms to "eat" mobs

# goal of the game: navigate player to eat the mob at the top of the map
# rules of the game: move the player using the controls and try to get the mobs
# feedback of the game: tells the player it won when it ate the ga,e


# import libraries and modules
# from platform import platform
import pygame as pg
# import settings
# from settings import *
from pygame.sprite import Sprite
import random
from random import randint

# provides directiom
vec = pg.math.Vector2


# # game settings 
WIDTH = 360
HEIGHT = 480
FPS = 30
mpos = (0,0)

# # player settings
PLAYER_GRAV = 0.5
PLAYER_FRIC = 0.1
SCORE = 0

# # define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# puts text on the screen to give scores
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# adds color to mobs
def colorbyte():
    return random.randint(0,255)

# sprites..
# This player needs to be able to be on the screen. move around the screen, updates itself by... 
# taking input from the person using the controls and collide with mobs to eat the mobs
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
        self.pos = vec(WIDTH, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    # controls of the game, how the player moves and takes input from person and... 
    # ... then displays that input as feedback on the screen
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.acc.y = -.5
        if keys[pg.K_a]:
            self.acc.x = -.5
        if keys[pg.K_s]:
            self.acc.y = .5
        if keys[pg.K_d]:
            self.acc.x = .5
    # allows the player tp jump up and around blocks.
    def jump(self):
        self.rect.x += .5
        self.rect.x += -.5
    # tells the person where it is on the screen 
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        # setting up for next method where player collides with platforms
        self.collide_with_walls('x')
        self.rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.pos
        self.hitx = self.hitx
        self.hity = self.hity
    # if the player collides with a platform, it does not go through the platform
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_plats, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                self.vel.x = 0
                self.centerx = self.pos.x
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_plats, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                

                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                self.vel.y = 0
                self.centery = self.pos.y
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False
 

# this class is for the platform the player will be moving around on and moving through the "maze"
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

     
# establishes the class of the Mob, what the player is trying to get to.
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
 
   

# starts pygame and creates a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# calls classes
player = Player()
# uses platform class to actually create the platform seen in game
plat = Platform(0, 350, 5000, 35)
plat1 = Platform(100, 50, 2400, 35)
plat2 = Platform(0, 200, 200, 35)
# uses mob class to actually creat the mob seen in game
mob = Mob(200, 30, 15, 15, GREEN,)


# creates groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()



# add things to groups
all_sprites.add(player, plat, plat1, plat2, mob)
all_plats.add(plat, plat1, plat2)
mobs.add(mob)



############################# Game loop ###########################################
# starts timer...
start_ticks = pg.time.get_ticks()

# if the game is running, everything is runinng
running = True
while running:
    # makes sure the game is running
    for event in pg.event.get():

        # check for closed window

        if event.type == pg.QUIT:

            running = False
# establishes what hapens when the play collides with the mob
    hits = pg.sprite.spritecollide(player, all_plats, False)
#    tells the mob to disapear from the window when the player collides with the mob
    mobhits = pg.sprite.spritecollide(player, mobs, True)

#  makes sure all sprites are updating every 1/30of a second
    all_sprites.update()
    #colors the screen 
    screen.fill(BLACK)
#    established the FPS clock
    delta = clock.tick(FPS)

    # draws the fps clock seen in game
   

    if mobhits:
        draw_text("You Win", 40, RED, 80, HEIGHT / 24)
        
   

    
    # gives the player color
    player.image.fill((player.r,player.g,player.b))

    
    # draw all sprites on the screen
    all_sprites.draw(screen)
    all_sprites.update()

    # buffer - after drawing everything, flip display
    pg.display.flip()
# stops the program
pg.quit()
