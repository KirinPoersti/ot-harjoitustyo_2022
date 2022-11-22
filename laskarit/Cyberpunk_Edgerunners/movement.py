import pygame

class movement(object):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move_x = 0 #Movement on x
        self.move_y = 0 #Movement on y(jump)
        self.frame = 0 #Count frames
    
    def Movement(self, x, y):
        #Player movement
        self.move_x += x
        self.move_y += y
    
    def position_update(self):
        #Update character position
        self.rect.x = self.rect.x + self.move_x
        self.rect.y = self.rect.y + self.move_y

