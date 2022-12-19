# SOURCES: w3schools.com, Mr. Cozorts Library, Chris BRadfiel KidsCanCode YouTube videos

# OVERVIEW
# # In this game, the player will move up through a maze of platforms to get a prize. 

# LIBRARIES
# changes name of pygame to pg in python
import pygame as pg
# from Class folder imports Mob class
from Class import Mob
# from Class folder imports Player class
from Class import Player
# from Class folder imports Platform class
from Class import Platform
# Imports spirties, so bascially grouping of classes, into my code.
from pygame.sprite import Sprite

from pygame.locals import *


# I am trying to make a game that allows for a player to move around the screen over platforms to "eat" a mob

# goal of the game: navigate player to eat the mob at the top of the map
# rules of the game: move the player using the controls and try to get the mobs
# feedback of the game: tells the player it won when it ate the game


# provides directiom
vec = pg.math.Vector2



# # game settings 
WIDTH = 1200
HEIGHT = 800
FPS = 60
mpos = (0,0)

# defines both width and height as the window of the game
window = WIDTH, HEIGHT

# # player settings
PLAYER_GRAV = .5

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

# starts pygame and creates a window
pg.init()
pg.mixer.init()
# sets the screen as my width and height
screen = pg.display.set_mode((WIDTH, HEIGHT))
# creates a clock for my game to start
clock = pg.time.Clock()

# calls classes
# calls player and turns into a variable from Class folder
player = Player()
# calls Platform class, 
# uses platform class to actually create the platform seen in game
plat = Platform(0, 650, 5000, 35)
plat1 = Platform(0, 50, 1140, 35)
plat2 = Platform(60, 200, 1140, 35)
plat3 = Platform(0, 500, 200, 35)
plat4 = Platform(150, 375, 150, 35)
plat5 = Platform(700, 180, 30, 45)
plat6 = Platform(700, 350, 35, 330)
plat7 = Platform(300, 200, 35, 330)
# uses mob class to actually creat the mob seen in game
mob = Mob(200, 30, 15, 15, GREEN,)


# creates groups for each class and makes them sprites
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()



# add the variables assigned to classes to groups
all_sprites.add(player, plat, plat1, 
plat2, plat3, plat4, 
plat5, plat6, plat7, 
mob)
all_plats.add(plat, plat1, plat2, 
plat3, plat4, plat5,
 plat6, plat7)
mobs.add(mob)



############################# Game loop ###########################################
# starts timer of the clock
start_ticks = pg.time.get_ticks()


# if the game is running, everything is runinng
running = True
# loop that makes the game run
while running:
    # makes sure the game is running
    for event in pg.event.get():
        # cif window is not running, game isn't running.
        if event.type == pg.QUIT:

            running = False
# establishes what hits actually is and what variables are assigned to hits
    hits = pg.sprite.spritecollide(player, all_plats, False)
#    tells the mob to disapear from the window when the player collides with the mob
    mobhits = pg.sprite.spritecollide(player, mobs, True)
   

#  makes sure all sprites are updating every 1/60 of a second
    all_sprites.update()
    # the collision code, stops the player from going through the bottom and tops of the platofrm supposedly

    # means this code is always checking when the player has any velocity going up/down
    if player.vel.y > 0:
        # checks to see if the player collides with any of the platforms
        hits = pg.sprite.spritecollide(player, all_plats, False)
        # if the player hits ...
        if hits:
            # ... the bottom of the player on the top of a platform, player always is pushed up 10 pixels
            if player.rect.bottom <= hits[0].rect.top + 10:
                # print(True)
                player.pos.y = hits[0].rect.top
                player.vel.y = 0
        hits = pg.sprite.spritecollide(player, all_plats, False)
        if hits:
            # ... the top of the player its the bottom of a platform, player is pushed down 10 pixels.
            if player.rect.bottom >= hits[0].rect.top - 10:
                player.rect.top = hits[0].rect.bottom
                player.acc.y = 5
                player.vel.y = 0


    # colors the screen in black
    screen.fill(BLACK)
    # established the FPS clock
    delta = clock.tick(FPS)

    # gives the player color
    player.image.fill((player.r,player.g,player.b))

    # draw all sprites on the screen
    all_sprites.draw(screen)
    all_sprites.update()

    # buffer - after drawing everything, flip display
    pg.display.flip()
# stops the program
pg.quit()