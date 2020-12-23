import pygame
import pygame.freetype
import random
import os
import re

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Function from the internet to help sort the lists of sprites
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


class Enemy:
    def __init__(self, directory: str, lvl: int, hp: float, atk: float):
        self.directory = directory
        self.lvl = lvl
        self.full_hp = hp+self.lvl
        self.hp = hp+self.lvl
        self.atk = atk+self.lvl

        # Beginning position of enemy
        self.x_pos_enemy = 490
        self.y_pos_enemy = 240

        # Position of HP bar
        self.x_pos_hp = 450
        self.y_pos_hp = 320

        # Animations dictionary and sprites
        self.hp_bar = []
        self.animations = {"Attack": [], "Hit": [], "Idle": [], "Windup": []}
        self.current_animation = self.animations["Idle"]
        self.current_animation_index = 0
        self.arrow = pygame.image.load("Arrow.png")
        self.arrow = pygame.transform.scale(self.arrow, (25, 25))
        self.arrow = pygame.transform.flip(self.arrow, True, False)

        # Custom User event
        self.IDLE = pygame.USEREVENT + 1

        self.WINDUP = pygame.USEREVENT + 2

        self.ATTACK_FORWARD = pygame.USEREVENT + 3

        self.ATTACK_UP = pygame.USEREVENT + 4

        self.ATTACK_DOWN = pygame.USEREVENT + 5
        
        self.RECOVER = pygame.USEREVENT + 6

        self.HIT = pygame.USEREVENT + 7

        # Arrow indicators
        self.arrow_up = False
        self.arrow_forward = False
        self.arrow_down = False

        # Checks if got hit
        self.got_hit = False

        # Checks if enemy killed player
        self.killed = False

        # Change the x pos of the hp bar
        self.x_repeat = 0

        # Loading in the health bar from directory
        health = sorted_alphanumeric(os.listdir("HP"))
        for health_frame in health:
            self.hp_bar.append((pygame.image.load("HP\\" + health_frame)))

        # Loading the enemy sprites based on the directory given
        enemy_animations = sorted_alphanumeric(os.listdir("Enemy\\" + self.directory))
        for animation in enemy_animations:
            animation_sprites = os.listdir("Enemy\\" + self.directory + "\\" + animation)
            for sprites in animation_sprites:
                self.animations[animation] \
                    .append(pygame.image.load("Enemy\\" + self.directory + "\\" + animation + "\\" + sprites))

        # Current enemy sprite & health
        self.current_sprite = self.current_animation[self.current_animation_index]
        self.current_health = self.hp_bar[20]

        # Getting the rect position of the sprite
        self.enemy_rect = self.current_sprite.get_rect(center=(self.x_pos_enemy-30, self.y_pos_enemy))

    # Getting the rect position of the sprite
    def rect(self):
        self.enemy_rect = self.current_sprite.get_rect(center=(self.x_pos_enemy-30, self.y_pos_enemy))

    # To change the the enemy sprite based on the list index
    def update(self):
        self.current_animation_index += 1

        if self.current_animation_index >= len(self.current_animation):
            self.current_animation_index = 0
        else:
            self.current_sprite = self.current_animation[self.current_animation_index]

    # Returns enemy to original position
    def return_to_origin(self):
        self.x_pos_enemy = 490
        self.y_pos_enemy = 240

    # Shows current HP bar
    def health_bar(self):
        current_hp_percentage = self.hp/self.full_hp*100

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

    def move(self, x=0.0, y=0.0):
        self.x_pos_enemy -= x
        self.y_pos_enemy -= y

    def shake_health(self):
        self.x_repeat += 1
        x_pos = [445, 450, 455]

        if self.x_repeat >= len(x_pos):
            self.x_repeat = 0

        self.x_pos_hp = x_pos[self.x_repeat]

    @ property
    def show_lvl(self):
        return self.draw_text("Lvl {}".format(self.lvl), 25, BLACK)

    @ property
    def show_hp(self):
        return self.draw_text("Hp {}".format(self.hp), 25, BLACK)

    @ property
    def give_exp(self):
        base_exp = random.randint(5, 10)
        exp_gain = int(base_exp*self.lvl)//1
        return exp_gain

    @staticmethod
    def draw_text(text: str, font_size: int, font_colour: tuple):
        font = pygame.freetype.Font("ARCADECLASSIC.TTF", font_size)
        text, _ = font.render(text, font_colour)
        return text.convert_alpha()
