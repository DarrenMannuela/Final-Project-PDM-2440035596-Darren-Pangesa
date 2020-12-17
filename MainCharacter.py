import pygame
import os
import re

# Function from the internet to help sort the lists of sprites
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


class MainCharacter:
    def __init__(self, lvl=1, hp=20, mp=10, exp_bar=0):
        # Start position of sprite
        self.x_pos = 40
        self.y_pos = 210

        # HP position
        self.x_hp = 40
        self.y_hp = 320

        # Main Character stats
        self.lvl = lvl
        self.hp = hp
        self.mp = mp
        self.exp_bar = exp_bar

        # Checks if Main Character attacked
        self.MOVE = pygame.USEREVENT + 10

        self.RECOVER = pygame.USEREVENT + 11

        # Checks if got hit
        self.got_hit = False

        # Starting index for each sprite
        self.animations = {"Attack": [], "Idle": [], "Hit": []}
        self.hp_bar = []
        self.current_animation = self.animations["Idle"]
        self.current_animation_index = 0
        self.current_hp_index = 20
        
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
        self.current_hp = self.hp_bar[self.current_hp_index]

        # Getting the rect position of the sprite
        self.character_rect = self.current_sprite.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.current_animation_index += 1

        if self.current_animation_index >= len(self.current_animation):
            self.current_animation_index = 0
        else:
            self.current_sprite = self.current_animation[self.current_animation_index]

    def health_bar(self):
        self.current_hp = self.hp_bar[self.current_hp_index]

    def movement(self, x=0.0, y=0.0):
        self.x_pos -= x
        self.y_pos -= y



