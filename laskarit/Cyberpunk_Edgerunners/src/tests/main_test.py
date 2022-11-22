import unittest
import pygame
from button import Button

pygame.init()

class Testmain(unittest.TestCase):
    def setUp(self):
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
        pause_button = self.button.Button(600, 50, pause_img, 1)
        resume_button = self.button.Button(250, 250, resume_img, 1)
        exit_button = self.button.Button(250, 450, exit_img, 1)


        def draw_text(text, font, txt_color , x, y):
            img = font.render(text, True, txt_color)
            screen.blit(img, (x, y))

    def test_menu_condition(self):
        self.assertEqual(str(self.menu_state), "main")
