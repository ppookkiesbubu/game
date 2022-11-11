import pygame
from support2 import import_csv_layout,import_cut_graphics
from setting2 import tile_size , screen_height ,screen_width
from tile2 import Tile,StaticTile,AnimatedTile,Coin
from enemy2 import Enemy
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self,level_data,surface):
        self.display_surface = surface
        self.world_shift = 0

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

        #enemy
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemy')

        #box
        box_layout = import_csv_layout(level_data['box'])
        self.box_sprites = self.create_tile_group(box_layout,'box')

        # #flower_green
        # flower_layout = import_csv_layout(level_data['flower_green'])
        # self.flower_sprites = self.create_tile_group(flower_layout,'flower_green')

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
                    
                    # if type == 'flower_green':
                    #     flower_tile_list = import_csv_layout('../graphics/item/flower_green.png')
                    #     tile_surface = flower_tile_list[int(val)]
                    #     sprite = StaticTile(tile_size,x,y,tile_surface)
                       
                    if type == 'coin':
                        sprite = Coin(tile_size,x,y,'../graphics/item/coin')

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
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False
                
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y >1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8


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

        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.box_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        #player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)


        # #flower
        # self.flower_sprites.update(self.world_shift)
        # self.flower_sprites.draw(self.display_surface)
