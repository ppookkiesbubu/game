import pygame

class UI:
    def __init__(self,surface):

        #setup
        self.display_surface = surface

        #health
        self.health_bar = pygame.image.load('../graphics/ui/healthbar.png')
        self.health_bar = pygame.transform.scale2x(self.health_bar)
        self.health_bar_topleft = (80,43)
        self.bar_max_width = 288
        self.bar_height = 4

        #coin
        self.coin = pygame.image.load('../graphics/ui/coin.png')
        self.coin = pygame.transform.scale(self.coin,(32,32))
        self.coin_rect = self.coin.get_rect(topleft = (50,61))
        self.font = pygame.font.Font('../graphics/ui/font.ttf',30)

    def show_health(self,current,full):
        self.display_surface.blit(self.health_bar,(50,35))
        current_health_ratio = current/full
        current_bar_width = self.bar_max_width * current_health_ratio 
        health_bar_rect = pygame.Rect((self.health_bar_topleft),(current_bar_width,self.bar_height))
        pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

    def show_coin(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right+4,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)

        



    # def show_gameover(self):
    #     game_over = self.font.render('GAME OVER',False,'#33323d')
    #     self.display_surface.blit(game_over)

        
    