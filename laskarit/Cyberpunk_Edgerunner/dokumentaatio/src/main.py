import pygame
import button

pygame.init()

# game window
screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cyberpunk: Edgerunner")

# game variables
paused = False
menu_state = "main"

# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colours
txt_color = (255, 255, 0)


# load menu pictures
mm_img = pygame.image.load("Resources/img/main menu_demo.png")
logo_img = pygame.image.load("Resources/img/Cyberpunk_Edgerunner_logo.png")

# load button images
pause_img = pygame.image.load("Resources/img/pause_demo.png").convert_alpha()
resume_img = pygame.image.load("Resources/img/resume_demo.png").convert_alpha()
exit_img = pygame.image.load("Resources/img/exit_demo.png").convert_alpha()

# create button
pause_button = button.Button(600, 50, pause_img, 1)
resume_button = button.Button(250, 250, resume_img, 1)
exit_button = button.Button(250, 450, exit_img, 1)


def draw_text(text, font, txt_color , x, y):
  img = font.render(text, True, txt_color)
  screen.blit(img, (x, y))

# game loop
run = True
while run:

  screen.blit(mm_img, (0,0))
  screen.blit(logo_img, (0, 550))

  # check menu state
  if menu_state == "main":
        #check if game is paused
    if pause_button.draw(screen):
        paused = True
        menu_state == "paused"
  if menu_state == "paused":
        #draw pause screen buttons
    if resume_button.draw(screen):
        paused = False
    if exit_button.draw(screen):
        run = False

  # event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()