import pygame

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Cyberpunk: Edgerunners')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#player variables
moving_left = False
moving_right = False
shooting = False

#load game images
background = pygame.image.load("Resources/img/background.png")
terrain = pygame.image.load("Resources/img/terrain.png")

def draw_bg():
    screen.blit(background, (0,0))
    screen.blit(terrain, (0,528.5))


class characters(pygame.sprite.Sprite):
    def __init__(self, char_type, weapon, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.weapon = weapon
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        temp_list = []
        for i in range(9):
            img = pygame.image.load(f'Resources/img/{self.char_type}/rest/{self.weapon}/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'Resources/img/{self.char_type}/shoot/{self.weapon}/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def move(self, moving_left, moving_right):
        #delta x
        dx = 0
        #delta y
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx = +self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy
  

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame frame index
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if frames run out then reset back to the first frame frame index
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
      #chekc if new action is different from the current one
      if new_action != self.action:
        self.action = new_action
        #update animation settings
        self.fram_index = 0
        self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
    

rebecca = characters('rebecca','pistol', 125, 350, 1.5, 5)


#game loop
run = True
while run:
    
    clock.tick(FPS)
    draw_bg()

    rebecca.update_animation()
    rebecca.draw()

    #update player actions
    if shooting:
      rebecca.update_action(1)#1:shoot
    else:
      rebecca.update_action(0)#0:rest

    rebecca.move(moving_left, moving_right)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_j:
                shooting = True
            # pause page will be added later
            if event.key == pygame.K_ESCAPE:
                run = False
          

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_j:
                shooting = False

    pygame.display.update()

pygame.quit()
        