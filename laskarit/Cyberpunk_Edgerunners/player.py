import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.in_air = True
        self.flip = False

        self.animation_list = []
        self.index = 0
        # order for animations
        # rest_pistol, rest_shotgun, rest_hmg, shoot_pistol, shoot_shotgun, shoot_hmg, jump_pistol, jump_shotgun, jump_hmg
        self.animation_steps = [9,9,9,5,6,5,9,9,9]
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        self.frame = 0
        self.black = (0,0,0)

        self.current_time = pygame.time.get_ticks()

        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                self.img = pygame.image.load(f'Resources/img/{self.char_type}_sprite.png')
                temp_img_list.append(self.img(self.index, 125, 125, 1, self.black))
                self.index  += 1
            self.animation_list.append(temp_img_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        #update animation
        animation_cooldown = 100
        #update image depending on current frame
        image = self.animation_list[self.action][self.index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        #if the animation has run out the reset back to the start
        if self.index >= len(self.animation_list[self.action]):
            self.index = 0
    
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()
    
    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)