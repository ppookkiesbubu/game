from random import randint
import pygame
from support2 import import_csv_layout,import_cut_graphics
from setting2 import tile_size , screen_height ,screen_width
from tile2 import Tile,StaticTile,AnimatedTile,Coin
from enemy2 import Enemy
from player import Player
from particles import ParticleEffect
from ui import UI


class Level:
    def __init__(self,level_data,surface):
        self.display_surface = surface
        self.world_shift = 0

        #time
        self.clock = pygame.time.Clock()
        self.sec = 0
        self.sec_count = 0
        self.sec = self.clock.tick(60)/1000

        self.time_state = 0
        self.check_state = 0

        #audio
        self.coin_sound = pygame.mixer.Sound('../graphics/sound/coin.wav')
        self.coin_sound.set_volume(0.5)
        self.bomb_sound = pygame.mixer.Sound('../graphics/sound/item2.wav')
        self.collision_sound = pygame.mixer.Sound('../graphics/sound/collision3.wav')
        self.gameover_sound  = pygame.mixer.Sound('../graphics/sound/gameover2.wav')
        self.bombbomb_sound = pygame.mixer.Sound('../graphics/sound/bomb.wav')
        self.bg_sound = pygame.mixer.Sound('../graphics/sound/bgsound.wav')
        # self.bg_sound.play(-1)


        #health bar
        self.max_health = 100
        self.cur_health = 100
        self.coin = 175

        #ui
        self.ui = UI(pygame.display.set_mode((screen_width,screen_height)))
        self.font = pygame.font.Font('../graphics/ui/font.ttf',30)

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        #coin 
        coin_layout = import_csv_layout(level_data['coin'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coin')

        #bomb
        bomb_layout = import_csv_layout(level_data['bomb'])
        self.bomb_sprites = self.create_tile_group(bomb_layout,'bomb')
        self.get_bomb = 0
        self.time_slow = 300
        self.status_slow = 0

        #enemy
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemy')

        #box
        box_layout = import_csv_layout(level_data['box'])
        self.box_sprites = self.create_tile_group(box_layout,'box')

        #flower1
        flower1_layout = import_csv_layout(level_data['flower1'])
        self.flower1_sprites = self.create_tile_group(flower1_layout,'flower1')

        #flower2
        flower2_layout = import_csv_layout(level_data['flower2'])
        self.flower2_sprites = self.create_tile_group(flower2_layout,'flower2')

        #flower3
        flower3_layout = import_csv_layout(level_data['flower3'])
        self.flower3_sprites = self.create_tile_group(flower3_layout,'flower3')

        #mushroom
        mushroom_layout = import_csv_layout(level_data['mushroom'])
        self.mushroom_sprites = self.create_tile_group(mushroom_layout,'mushroom')

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    
                    if type == 'flower_green':
                        flower_tile_list = import_csv_layout('../graphics/item/flower_green.png')
                        flower_surface = flower_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,flower_surface)
                       
                    if type == 'coin':
                        sprite = Coin(tile_size,x,y,'../graphics/item/coin')
                        
                    if type == 'bomb':
                        bomb_tile_list = import_cut_graphics('../graphics/item/bomb.png')
                        bomb_surface = bomb_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,bomb_surface)

                    if type == 'flower1':
                        flower1_tile_list = import_cut_graphics('../graphics/item/flower1.png')
                        flower1_surface = flower1_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,flower1_surface)

                    if type == 'flower2':
                        flower2_tile_list = import_cut_graphics('../graphics/item/flower2.png')
                        flower2_surface = flower2_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,flower2_surface)

                    if type == 'flower3':
                        flower3_tile_list = import_cut_graphics('../graphics/item/flower3.png')
                        flower3_surface = flower3_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,flower3_surface)

                    if type == 'mushroom':
                        mushroom_tile_list = import_cut_graphics('../graphics/item/mushroom.png')
                        mushroom_surface = mushroom_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,mushroom_surface)

                    if type == 'enemy':
                        sprite = Enemy(tile_size,x,y)

                    if type == 'box':
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)
                   
        return sprite_group

    def player_setup(self,layout):
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite =Player((x,y),self.display_surface,self.create_jump_particles)
                    self.player.add(sprite)
                if val == '-1':
                    hat_surface = pygame.image.load('../graphics/item/setup_player.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.box_sprites,False):
                enemy.reverse()

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        # if self.check_state == 0:
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                    
    def vertical_movement_collision(self):
        # if self.check_state == 0:
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y >1:
            player.on_ground = False

    def scroll_x(self):
        # if self.check_state == 0:
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 2 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 2) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def change_coin(self,amount):
        self.coin -=  amount  

    def check_coin_collisions(self):
        # if self.check_state == 0:
        collided_coin = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        if collided_coin:
            self.coin_sound.play()
            for coin in collided_coin:
                self.change_coin(1)

    def check_enemy_collision(self):
        # if self.check_state == 0:
        enemy_collision = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

        if enemy_collision:
            self.collision_sound.play()
            for enemy in enemy_collision:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    self.cur_health -= 10
                else:
                    self.cur_health -= 1

    def check_bomb(self):   
        keys = pygame.key.get_pressed()
        if pygame.sprite.spritecollide(self.player.sprite,self.bomb_sprites,True):
            self.get_bomb += 1
            self.bomb_sound.play()
        if keys[pygame.K_SPACE] and self.get_bomb >= 1:
            self.bombbomb_sound.play()
            self.get_bomb -= 1
            for enemy in self.enemy_sprites:
                enemy.speed = 1
            self.status_slow = 1
        if self.status_slow == 1:
            self.time_slow -= 1
            if self.time_slow  <= 0 :
                self.time_slow = 300
                self.status_slow = 0
                for enemy in self.enemy_sprites:
                    enemy.speed = randint(3,5)

    def check_game_over(self):
      
        if self.cur_health <= 0 or self.player.sprite.direction.y >= 35:
            global game_status
            self.gameover_sound.play()
            self.collision_sound.stop()
            self.bg_sound.stop()
            self.cur_health = 0
            game_over = self.font.render('GAME OVER',False,'#33323d')
            self.display_surface.blit(game_over,(500,43))
            self.check_state = 1
            game_status = 0
            self.time_state = 1

    def check_win(self):
            if self.coin <= 0:
                game_win = self.font.render('YOU WIN!!!',False,'#33323d')
                self.display_surface.blit(game_win,(500,43))
                self.check_state = 1
                self.time_state = 1
                game_status = 0

    def time(self,sc):    
        # self.sec = self.clock.tick(30)/1000
        global time_count
        if self.check_state == 0:
            self.sec_count += self.sec 
            time_count = float("{:.2f}".format(self.sec_count))
            
    def show_time(self):
        if self.time_state == 0:
            self.time(1)
            sec_surf = self.font.render(str(time_count),False,'#33323d')
            # sec_rect = sec_surf.get_rect(midleft = (self.sec_rect.right+4,self.sec_rect.centery))
            self.display_surface.blit(sec_surf,(1075,20))


    def run(self):
        # #bg
        # self.bg = pygame.image.load('../graphics/sky/sky.png').convert()
        # self.bg_rect = self.bg.get_rect(topleft = (0,0))
        # self.display_surface.blit(self.bg, self.bg_rect)
        #run the entire game / level
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        #coin
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        #bomb
        self.bomb_sprites.draw(self.display_surface)
        self.bomb_sprites.update(self.world_shift)

        #flower1
        self.flower1_sprites.draw(self.display_surface)
        self.flower1_sprites.update(self.world_shift)

        #flower2
        self.flower2_sprites.draw(self.display_surface)
        self.flower2_sprites.update(self.world_shift)

        #flower3
        self.flower3_sprites.draw(self.display_surface)
        self.flower3_sprites.update(self.world_shift)

        #mushroom
        self.mushroom_sprites.draw(self.display_surface)
        self.mushroom_sprites.update(self.world_shift)


        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.box_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        #player sprites
        self.player.update()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.ui.show_health(self.cur_health,self.max_health)
        self.ui.show_coin(self.coin)
        self.show_time()
       

        self.check_coin_collisions()
        self.check_enemy_collision()
        self.check_game_over()
        self.check_win()
        self.check_bomb()

        if self.check_state == 0:
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.scroll_x()