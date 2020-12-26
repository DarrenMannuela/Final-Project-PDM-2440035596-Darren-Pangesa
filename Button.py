import pygame
import pygame.freetype

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


pygame.freetype.init()


class Buttons:
    def __init__(self, text: str, rect: tuple, font_size: int, font_colour: tuple):
        self.mouse_over = False
        self.clicked = False

        self.button_not_clicked = self.draw_text(text, font_size, font_colour)
        self.button_clicked = self.draw_text(text, font_size, WHITE)

        self.buttons_check = [self.button_not_clicked, self.button_clicked]
        self.positions = [self.button_not_clicked.get_rect(center=rect), self.button_clicked.get_rect(center=rect)]

    def draw(self, surface):
        surface.blit(self.text, self.position)

    def check_for_mouse(self, mouse_pos):
        if self.position.collidepoint(mouse_pos):
            self.mouse_over = True
        else:
            self.mouse_over = False

    @property
    def text(self):
        return self.buttons_check[1] if self.mouse_over else self.buttons_check[0]

    @property
    def position(self):
        return self.positions[1] if self.mouse_over else self.positions[0]

    @staticmethod
    def draw_text(text: str, font_size: int, font_colour: tuple):
        font = pygame.freetype.Font("ARCADECLASSIC.TTF", font_size)
        text, _ = font.render(text, font_colour)
        return text.convert_alpha()


