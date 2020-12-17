import pygame
import os
import re

# Function from the internet to help sort the lists of sprites
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


class Enemy:
    def __init__(self, directory: str, hp: float, attack: float):
        self.directory = directory
        self.attack = attack
        self.hp = hp

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
        self.current_health_index = 20
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

        self.current_state = "idle"

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
        self.current_health = self.hp_bar[self.current_health_index]

        # Getting the rect position of the sprite
        self.enemy_rect = self.current_sprite.get_rect(center=(self.x_pos_enemy, self.y_pos_enemy))

    # To change the the enemy sprite based on the list index
    def update(self):
        self.current_animation_index += 1

        if self.current_animation_index >= len(self.current_animation):
            self.current_animation_index = 0
        else:
            self.current_sprite = self.current_animation[self.current_animation_index]

    # Shows current HP bar
    def health_bar(self):
        self.current_health = self.hp_bar[self.current_health_index]

    def move(self, x=0.0, y=0.0):
        self.x_pos_enemy -= x
        self.y_pos_enemy -= y

