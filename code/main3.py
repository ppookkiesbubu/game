import pygame,sys
from setting2 import *
from level2 import Level
from game_data2 import level_0

#pygame setup
pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height)) 
clock = pygame.time.Clock()
level = Level(level_0,screen)
font = pygame.font.Font('../graphics/ui/font.ttf',30)

def game():
    while True:
        print("GAME RUN")
        level.run()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
        pygame.display.update()
        clock.tick(60)

def menu():
    while True :
        screen.fill((255,255,255))
        play_button = pygame.Rect((screen_width/2,screen_height/2),(150,60))
        pygame.draw.rect(screen,(0,0,0),play_button)
        for event in pygame.event.get():
            # print(event.type,pygame.QUIT)
            if event.type == pygame.QUIT:
                print("exit")
                pygame.quit()
                sys.exit()            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if play_button.collidepoint((mx,my)):
                    game()
                    print('click')

        pygame.display.update()
        clock.tick(60)

menu()