import pygame
import os
from pygame import mixer

mixer.init()
pygame.init()

#screen settings
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Cyberpunk: Edgerunners')

#set framerate
clock = pygame.time.Clock()
FPS = 144

#game variables
gravity = 0.75

#load game images
background = pygame.image.load("Resources/img/background.png")
terrain = pygame.image.load("Resources/img/terrain.png")
bullet_img = pygame.image.load("Resources/img/bullets/universal/bullet.png")

#load bgm and sounds:
pygame.mixer.music.load("Resources/bgm/the rebel way.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 2000)
pistol_sf = pygame.mixer.Sound("Resources/bgm/pistol_sf.mp3")
pistol_sf.set_volume(0.3)
shotgun_sf = pygame.mixer.Sound("Resources/bgm/shotgun_sf.mp3")
shotgun_sf.set_volume(0.3)
hmg_sf = pygame.mixer.Sound("Resources/bgm/hmg_sf.mp3")
hmg_sf.set_volume(0.3)

#creating background
def draw_bg():
    screen.blit(background, (0,0))
    screen.blit(terrain, (0,528.5))


#in-game character related class
class characters(pygame.sprite.Sprite):
    def __init__(self, char_type, weapon, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        #basic stats for the character
        self.alive = True
        self.char_type = char_type
        self.weapon = weapon
        self.speed = speed
        self.shoot_cooldown = 0
        self.hp = 100
        self.max_hp = self.hp

        #character movement related variables
        self.direction = 1
        self.airborne = False
        self.rest = True
        self.jump = False
        self.v_y = 0
        #(v=velocity)
        self.shooting = False
        self.flip = False
        self.moving_left = False
        self.moving_right = False    

        #animation related variables
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        animation_types = ['rest','jump','shoot','death']
        for animation in animation_types:
            temp_list = []
            #count number of files in the exact folder
            numbers_of_frames = len(os.listdir(f'Resources/img/{self.char_type}/{animation}/{self.weapon}'))
            #frame fetching
            for i in range(numbers_of_frames):
                img = pygame.image.load(f'Resources/img/{self.char_type}/{animation}/{self.weapon}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.width = 70
        self.height = 94
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = (x,y)
        
        


    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown:
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    #method for movement
    def move(self, moving_left, moving_right):
        #delta x
        dx = 0
        #delta y
        dy = 0
        
        #move left
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        
        #move right
        if moving_right:
            dx = +self.speed
            self.flip = False
            self.direction = 1
        
        #jump
        if self.jump == True and self.airborne == False:
            self.v_y = -11
            self.jump = False
            self.airborne = True

        #apply gravity
        self.v_y += gravity
        if self.v_y > 10:
            self.v_y = 10
        dy += self.v_y

        #check collision with terrain
        if self.rect.bottom + dy > 528.5:
            dy = 528.5 - self.rect.bottom
            self.airborne = False

        self.rect.x += dx
        self.rect.y += dy
    
    def shoot(self):
        if self.shoot_cooldown == 0:
            if rebecca.weapon == 'pistol':
                self.shoot_cooldown = 25
                bullet = Bullet(self.rect.centerx + (0.2 * self.rect.size[0]), self.rect.centery*1.07, self.direction)
                bullet_group.add(bullet)
            if rebecca.weapon == 'shotgun':
                self.shoot_cooldown = 160
                bullet = Bullet(self.rect.centerx + (0.2 * self.rect.size[0]), self.rect.centery*1.07, self.direction)
                bullet_group.add(bullet)
            if rebecca.weapon == 'hmg':
                self.shoot_cooldown = 10
                bullet = Bullet(self.rect.centerx + (0.00005 * self.rect.size[0]), self.rect.centery*1.07, self.direction)
                bullet_group.add(bullet)
  
    #method for updating animation
    def update_animation(self):
        if rebecca.weapon == 'pistol':
            ANIMATION_COOLDOWN = 100
        if rebecca.weapon == 'shotgun':
            ANIMATION_COOLDOWN = 200
        if rebecca.weapon == 'hmg':
            ANIMATION_COOLDOWN = 50
        #update image depending on current frame frame index
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if frames run out then reset back to the first frame frame index
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    #method for updating action state
    def update_action(self, new_action):
      #chekc if new action is different from the current one
      if new_action != self.action:
        self.action = new_action
        #update animation settings
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    #method for displaying character in game
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 1)
    

#class for projectile
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self,)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self):
        #move bullets
        if rebecca.weapon == 'hmg':
            self.rect.y -= (1 * self.speed)
        else:
            self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        
        #check collision with characters
        #if pygame.sprite.spritecollide(rebecca, bullet_group, False):
            #if rebecca.alive:
                #rebecca.hp -= 30
                #self.kill()
        
        if pygame.sprite.spritecollide(maxtac, bullet_group, False):
            if maxtac.alive:
                if rebecca.weapon == 'pistol':
                    maxtac.hp -= 5
                    print(maxtac.hp)
                    self.kill()
                if rebecca.weapon == 'shotgun':
                    maxtac.hp -= 100
                    print(maxtac.hp)
                    self.kill()
                if rebecca.weapon == 'hmg':
                    maxtac.hp -= 45
                    print(maxtac.hp)
                    self.kill()
    


#create sprite groups
bullet_group = pygame.sprite.Group()

#test run
rebecca = characters('rebecca','pistol', 125, 435, 1.5, 5)
maxtac = characters('maxtac','ar', 125, 435, 1.5, 5)

#game loop
run = True
while run:
    
    clock.tick(FPS)
    draw_bg()

    #initializing rebecca related methods
    rebecca.update()
    rebecca.draw()

    maxtac.update()
    maxtac.draw()
    rebecca.move(rebecca.moving_left, rebecca.moving_right)

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    #player state check
    if rebecca.alive:
        if rebecca.rest:
            rebecca.update_action(0)#0: resting
        elif rebecca.shooting:
            rebecca.update_action(2)#2: shooting
            rebecca.shoot()
        elif rebecca.airborne:
            rebecca.update_action(1)#1: jumping
    
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                rebecca.moving_left = True
            if event.key == pygame.K_d:
                rebecca.moving_right = True
            if event.key == pygame.K_r:
                rebecca = characters('rebecca','pistol', 125, 435, 1.5, 5)
            if event.key == pygame.K_q:
                rebecca = characters('rebecca','shotgun', 125, 435, 1.5, 5)
            if event.key == pygame.K_e:
                rebecca = characters('rebecca','hmg', 125, 435, 1.5, 5)
            if event.key == pygame.K_SPACE and rebecca.alive:
                if event.key == pygame.K_SPACE and event.key == pygame.K_j:
                    rebecca.jump = True
                    rebecca.shooting = True
                    pistol_sf.play()
                else:
                    rebecca.rest = False
                    rebecca.jump = True
            if event.key == pygame.K_j:
                if rebecca.weapon == 'pistol':
                    pistol_sf.play(-1)
                if rebecca.weapon == 'shotgun':
                    shotgun_sf.play(-1)
                if rebecca.weapon == 'hmg':
                    hmg_sf.play(-1)
                rebecca.rest = False
                rebecca.shooting = True
            # pause page will be added later
            if event.key == pygame.K_ESCAPE:
                run = False
          

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                rebecca.moving_left = False
            if event.key == pygame.K_d:
                rebecca.moving_right = False
            if event.key == pygame.K_SPACE:
                rebecca.rest = True
                rebecca.jump = False
            if event.key == pygame.K_j:
                if rebecca.weapon == 'pistol':
                    pistol_sf.stop()
                    rebecca.shooting = False
                    rebecca.rest = True
                if rebecca.weapon == 'shotgun':
                    shotgun_sf.stop()
                    rebecca.shooting = False
                    rebecca.rest = True
                if rebecca.weapon == 'hmg':
                    hmg_sf.stop()
                    rebecca.shooting = False
                    rebecca.rest = True


    pygame.display.update()

pygame.quit()
        