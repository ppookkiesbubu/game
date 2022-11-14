import pygame,sys
from setting2 import *
from level2 import Level
from game_data2 import level_0

#pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height)) 
clock = pygame.time.Clock()
level = Level(level_0,screen)

class Button():
    def __init__(self,x,y,width,height,fg,bg,content,fontsize):
        self.font = pygame.font.Font('../graphics/ui/font.ttf',30)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content,True,self.fg)
        self.text_rect = self.text.get_rect(center = (self.width/2,self.height/2))
        self.image.blit(self.text,self.text_rect)

    def is_pressed(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

player_button = Button(10,50,100,50,(255,255,255),(0,0,0),'Play',32)
intro_screen = True
while intro_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro_screen = False
            pygame.quit() 
            sys.exit()

    mouse_pos = pygame.mouse.get_pos()
    mouse_preesed = pygame.mouse.get_pressed()
    if player_button.is_pressed(mouse_pos,mouse_preesed):
        intro_screen = False

while not intro_screen:
    level.run()

    screen.fill('grey')
    screen.blit(player_button.image,player_button.rect)
        
    pygame.display.update()
    clock.tick(60)
    