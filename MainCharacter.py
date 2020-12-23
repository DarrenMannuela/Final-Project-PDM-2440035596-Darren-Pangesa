import pygame
import pygame.freetype
import os
import re

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Function from the internet to help sort the lists of sprites
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


class MainCharacter:
    def __init__(self, lvl=1, hp=20, atk=5, exp=0):
        # Start position of sprite
        self.x_pos = 40
        self.y_pos = 210

        # HP position
        self.x_hp = 40
        self.y_hp = 320

        # Main Character stats
        self.lvl = lvl
        self.full_hp = hp
        self.hp = hp
        self.atk = atk
        self.exp = exp
        self.exp_req = 100

        # Checks if Main Character attacked
        self.MOVE = pygame.USEREVENT + 10

        self.RECOVER = pygame.USEREVENT + 11

        self.GAIN_EXP = pygame.USEREVENT + 12

        self.LEVEL_UP = pygame.USEREVENT + 13

        self.LEVEL_DOWN = pygame.USEREVENT + 14

        # Checks if got hit
        self.got_hit = False

        # Checks if killed enemy
        self.killed = False

        # Show lose, win and next level text
        self.you_win = False
        self.you_lose = False
        self.next_level = False

        # Change the x pos of the hp bar
        self.x_repeat = 0

        # Starting index for each sprite
        self.animations = {"Attack": [], "Idle": [], "Hit": []}
        self.hp_bar = []
        self.current_animation = self.animations["Idle"]
        self.current_animation_index = 0
        
        #  Loading animations for Main Character
        main_character_animations = os.listdir("MainCharacter")
        for animation in main_character_animations:
            animation_sprites = sorted_alphanumeric(os.listdir("MainCharacter\\"+animation))
            for sprite in animation_sprites:
                self.animations[animation].append(pygame.image.load("MainCharacter\\"+animation+"\\"+sprite))

        # Loading HP bar fot Main Character
        main_character_hp = sorted_alphanumeric(os.listdir("HP"))
        for hp in main_character_hp:
            self.hp_bar.append(pygame.image.load("HP\\"+hp))

        # Current character sprite & health
        self.current_sprite = self.current_animation[self.current_animation_index]
        self.current_health = self.hp_bar[20]

        self.character_rect = self.current_sprite.get_rect(center=(self.x_pos, self.y_pos))

    # Getting the rect position of the sprite
    def rect(self):
        self.character_rect = self.current_sprite.get_rect(center=(self.x_pos, self.y_pos))

    # Returns to original position
    def return_to_origin(self):
        self.x_pos = 40
        self.y_pos = 210

    # A method to allow the animation to flow automatically
    def update(self):
        self.current_animation_index += 1

        if self.current_animation_index >= len(self.current_animation):
            self.current_animation_index = 0
        else:
            self.current_sprite = self.current_animation[self.current_animation_index]

    def health_bar(self):
        current_hp_percentage = self.hp / self.full_hp * 100

        if 95 >= current_hp_percentage <= 100:
            self.current_health = self.hp_bar[20]

        if 90 >= current_hp_percentage < 95:
            self.current_health = self.hp_bar[19]

        if 85 >= current_hp_percentage < 90:
            self.current_health = self.hp_bar[18]

        if 80 >= current_hp_percentage < 85:
            self.current_health = self.hp_bar[17]

        if 75 >= current_hp_percentage < 80:
            self.current_health = self.hp_bar[16]

        if 70 >= current_hp_percentage < 75:
            self.current_health = self.hp_bar[15]

        if 65 >= current_hp_percentage < 70:
            self.current_health = self.hp_bar[14]

        if 60 >= current_hp_percentage < 65:
            self.current_health = self.hp_bar[13]

        if 55 >= current_hp_percentage < 60:
            self.current_health = self.hp_bar[12]

        if 50 >= current_hp_percentage < 55:
            self.current_health = self.hp_bar[11]

        if 45 >= current_hp_percentage < 50:
            self.current_health = self.hp_bar[10]

        if 40 >= current_hp_percentage < 45:
            self.current_health = self.hp_bar[9]

        if 35 >= current_hp_percentage < 40:
            self.current_health = self.hp_bar[8]

        if 30 >= current_hp_percentage < 35:
            self.current_health = self.hp_bar[7]

        if 25 >= current_hp_percentage < 30:
            self.current_health = self.hp_bar[6]

        if 20 >= current_hp_percentage < 25:
            self.current_health = self.hp_bar[5]

        if 15 >= current_hp_percentage < 20:
            self.current_health = self.hp_bar[4]

        if 10 >= current_hp_percentage < 15:
            self.current_health = self.hp_bar[3]

        if 5 >= current_hp_percentage < 10:
            self.current_health = self.hp_bar[2]

        if 0 > current_hp_percentage < 5:
            self.current_health = self.hp_bar[1]

        if current_hp_percentage <= 0:
            self.current_health = self.hp_bar[0]

    def movement(self, x=0.0, y=0.0):
        self.x_pos -= x
        self.y_pos -= y

    def shake_health(self):
        self.x_repeat += 1
        x_pos = [35, 40, 45]

        if self.x_repeat >= len(x_pos):
            self.x_repeat = 0

        self.x_hp = x_pos[self.x_repeat]

    def gain_exp(self, exp_gain: int):
        self.exp += exp_gain
        if self.exp >= self.exp_req:
            self.lvl += 1
            self.full_hp += 5
            self.hp = self.full_hp
            self.atk += 1
            remainder_exp = self.exp - self.exp_req
            self.exp = remainder_exp
            self.exp_req = int(self.lvl*10 + self.exp_req)
            self.current_health = self.hp_bar[20]

    @ property
    def show_lvl(self):
        return self.draw_text("Lvl {}".format(self.lvl), 25, BLACK)

    @ property
    def show_hp(self):
        return self.draw_text("Hp {}".format(self.hp), 25, BLACK)

    @ property
    def show_exp(self):
        return self.draw_text("Exp     {}I     {}".format(self.exp, self.exp_req), 25, BLACK)

    @ staticmethod
    def draw_text(text: str, font_size: int, font_colour: tuple):
        font = pygame.freetype.Font("ARCADECLASSIC.TTF", font_size)
        text, _ = font.render(text, font_colour)
        return text.convert_alpha()
