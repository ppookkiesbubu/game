import pygame,sys
from setting2 import *
from level2 import Level
from game_data2 import level_0

#pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height)) 
clock = pygame.time.Clock()
level = Level(level_0,screen)
intro_screen = True


while intro_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro_screen = False
            pygame.quit() 
            sys.exit()


    screen.fill('grey')
    level.run()
        
    pygame.display.update()
    clock.tick(60)

    