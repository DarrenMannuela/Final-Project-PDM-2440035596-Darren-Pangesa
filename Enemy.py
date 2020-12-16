import pygame
import os
import random
import re

# Function from the internet to help sort the lists of sprites
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


pygame.init()
clock = pygame.time.Clock()
bg1 = pygame.image.load("Background 1.jpg")
game_window_width, game_window_height = 640, 480
canvas = pygame.Surface((game_window_width, game_window_height))
window = pygame.display.set_mode((game_window_width, game_window_height))
running = True


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
        self.health_bar = []
        self.animations = {"Attack": [], "Hit": [], "Idle": [], "Windup": []}
        self.current_animation = self.animations["Idle"]
        self.current_animation_index = 0
        self.current_health_index = 20

        # Custom User event
        self.IDLE = pygame.USEREVENT + 1

        self.WINDUP = pygame.USEREVENT + 2

        self.ATTACK_FORWARD = pygame.USEREVENT + 3

        self.ATTACK_UP = pygame.USEREVENT + 4

        self.ATTACK_DOWN = pygame.USEREVENT + 5
        
        self.RECOVER = pygame.USEREVENT + 6
        
        # Set timer to start loop
        pygame.time.set_timer(self.IDLE, 1000, True)

        # Conditional to see if the enemy attacks
        self.go_attack = random.randint(0, 13)

        # Conditional where to attack
        self.where_attack = random.randint(1, 3)

        # Loading in the health bar from directory
        health = sorted_alphanumeric(os.listdir("HP"))
        for health_frame in health:
            self.health_bar.append((pygame.image.load("HP\\" + health_frame)))

        # Loading the enemy sprites based on the directory given
        enemy_animations = sorted_alphanumeric(os.listdir("Enemy\\" + self.directory))
        for animation in enemy_animations:
            animation_sprites = os.listdir("Enemy\\" + self.directory + "\\" + animation)
            for sprites in animation_sprites:
                self.animations[animation] \
                    .append(pygame.image.load("Enemy\\" + self.directory + "\\" + animation + "\\" + sprites))

        # Current enemy sprite & health
        self.current_sprite = self.current_animation[self.current_animation_index]
        self.current_health = self.health_bar[self.current_health_index]

    # To change the the enemy sprite based on the list index
    def update(self):
        self.current_animation_index += 1

        if self.current_animation_index >= len(self.current_animation):
            self.current_animation_index = 0
        else:
            self.current_sprite = self.current_animation[self.current_animation_index]

    # Shows current HP bar
    def hp_bar(self):
        if self.current_health_index == 0:
            self.current_health_index = 20
        else:
            self.current_health_index -= 1
            self.current_health = self.health_bar[self.current_health_index]

    def move(self, x=0.0, y=0.0):
        self.x_pos_enemy -= x
        self.y_pos_enemy -= y


bat = Enemy("Bat", 20, 1)
pygame.time.set_timer(bat.IDLE, 1000, True)
go_attack = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == bat.IDLE:
            bat.current_animation = bat.animations["Idle"]
            go_attack = random.randint(1, 5)
            if go_attack == 1:
                pygame.time.set_timer(bat.WINDUP, 1000, True)

            if go_attack == 3:
                pygame.time.set_timer(bat.WINDUP, 1000, True)
            else:
                pygame.time.set_timer(bat.IDLE, 100, True)

        if event.type == bat.WINDUP:
            bat.current_animation = bat.animations["Windup"]
            where_attack = random.randint(1, 3)
            bat.move(-30)
            if where_attack == 1:
                pygame.time.set_timer(bat.ATTACK_FORWARD, 1000, True)

            if where_attack == 2:
                pygame.time.set_timer(bat.ATTACK_UP, 1000, True)

            if where_attack == 3:
                pygame.time.set_timer(bat.ATTACK_DOWN, 1000, True)

        if event.type == bat.ATTACK_FORWARD:
            bat.current_animation = bat.animations["Attack"]
            bat.move(50)
            if bat.x_pos_enemy > 100:
                pygame.time.set_timer(bat.ATTACK_FORWARD, 5, True)
            else:
                pygame.time.set_timer(bat.RECOVER, 300, True)

        if event.type == bat.ATTACK_UP:
            bat.current_animation = bat.animations["Attack"]
            bat.move(50, 10)
            if bat.x_pos_enemy > 100:
                pygame.time.set_timer(bat.ATTACK_UP, 5, True)
            else:
                pygame.time.set_timer(bat.RECOVER, 300, True)

        if event.type == bat.ATTACK_DOWN:
            bat.current_animation = bat.animations["Attack"]
            bat.move(50, -10)
            if bat.x_pos_enemy > 100:
                pygame.time.set_timer(bat.ATTACK_DOWN, 5, True)
            else:
                pygame.time.set_timer(bat.RECOVER, 300, True)

        if event.type == bat.RECOVER:
            bat.current_animation = bat.animations["Idle"]
            bat.move(-50)
            if bat.x_pos_enemy < 490:
                pygame.time.set_timer(bat.RECOVER, 5, True)
            else:
                bat.x_pos_enemy = 490
                bat.y_pos_enemy = 240
                bat.current_animation = bat.animations["Idle"]
                pygame.time.set_timer(bat.IDLE, 2500, True)

    bat.update()
    bat.hp_bar()
    canvas.blit(bg1, (0, 0))
    canvas.blit(pygame.transform.flip(bat.current_sprite, True, False), (bat.x_pos_enemy, bat.y_pos_enemy))
    canvas.blit(pygame.transform.flip(bat.current_health, True, False), (bat.x_pos_hp, bat.y_pos_hp))
    window.blit(canvas, (0, 0))
    clock.tick(20)
    pygame.display.flip()
