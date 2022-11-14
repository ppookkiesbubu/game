import pygame
from support2 import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -18
        self.collision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))
        self.jump_sound = pygame.mixer.Sound('../graphics/sound/jump.wav')

        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False


    def import_character_assets(self):
        character_path = '../graphics/player_resize/'
        self.animations = {'idle' : [],'run': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder()

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame_index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        # #set the rect
        # if self.on_ground and self.on_right:
        #     self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        # elif self.on_ground and self.on_left:
        #     self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        # elif self.on_ground:
        #     self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # elif self.on_ceiling and self.on_right:
        #     self.rect = self.image.get_rect(topright = self.rect.topright)
        # elif self.on_ceiling and self.on_left:
        #     self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # elif self.on_ceiling:
        #     self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys[pygame.K_w] and self.on_ground:
           self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
        if self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'
        

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.jump_sound.play()
        self.direction.y = self.jump_speed

    

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        
