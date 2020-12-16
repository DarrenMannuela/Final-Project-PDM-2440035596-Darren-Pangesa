import pygame
import os
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


class Player:
    def __init__(self, lvl=1, hp=20, mp=10, exp_bar=0):
        # Start position of sprite
        self.x_pos = 40
        self.y_pos = 240

        # HP position
        self.x_hp = 40
        self.y_hp = 350

        # Main Character stats
        self.lvl = lvl
        self.hp = hp
        self.mp = mp
        self.exp_bar = exp_bar

        # Checks if Main Character attacked
        self.IDLE = pygame.USEREVENT
        self.MOVE = pygame.USEREVENT + 1
        self.RECOVER = pygame.USEREVENT + 2
        self.attacked = False
        self.recover = 5

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

        self.current_sprite = self.current_animation[self.current_animation_index]
        self.current_hp = self.hp_bar[self.current_hp_index]

    def update(self):
        self.current_animation_index += 1

        if self.current_animation_index >= len(self.current_animation):
            self.current_animation_index = 0
        else:
            self.current_sprite = self.current_animation[self.current_animation_index]

    def health_bar(self):
        if self.current_hp_index == 0:
            self.current_hp_index = 20
        else:
            self.current_hp_index -= 1
            self.current_hp = self.hp_bar[self.current_hp_index]

    def movement(self, x=0.0, y=0.0):
        self.x_pos -= x
        self.y_pos -= y


main_character = Player()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                main_character.current_animation = main_character.animations["Idle"]
                main_character.movement(y=100)

            if event.key == pygame.K_a:
                main_character.current_animation = main_character.animations["Idle"]
                main_character.movement(50)

            if event.key == pygame.K_s:
                main_character.current_animation = main_character.animations["Idle"]
                main_character.movement(y=-50)

            if event.key == pygame.K_d:
                pygame.time.set_timer(main_character.MOVE, 5, True)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                main_character.current_animation = main_character.animations["Idle"]
                main_character.current_sprite_index = 0
                main_character.x_pos = 40
                main_character.y_pos = 240

            if event.key == pygame.K_a:
                main_character.current_animation = main_character.animations["Idle"]
                main_character.current_sprite_index = 0
                main_character.x_pos = 40
                main_character.y_pos = 240

            if event.key == pygame.K_s:
                main_character.current_animation = main_character.animations["Idle"]
                main_character.current_sprite_index = 0
                main_character.x_pos = 40
                main_character.y_pos = 240

        if event.type == main_character.MOVE:
            pygame.event.set_blocked(pygame.KEYDOWN)
            main_character.movement(-50)
            if main_character.x_pos < 300:
                pygame.time.set_timer(main_character.MOVE, 5, True)
            else:
                main_character.current_animation = main_character.animations["Attack"]
                pygame.time.set_timer(main_character.RECOVER, 350, True)

        if event.type == main_character.RECOVER:
            main_character.current_animation = main_character.animations["Idle"]
            main_character.movement(50)
            if main_character.x_pos > 40:
                pygame.time.set_timer(main_character.RECOVER, 5, True)
            else:
                main_character.x_pos = 40
                main_character.y_pos = 240
                pygame.time.set_timer(main_character.IDLE, 2000, True)

        if event.type == main_character.IDLE:
            pygame.event.set_allowed(pygame.KEYDOWN)

    main_character.update()
    main_character.health_bar()
    canvas.blit(bg1, (0, 0))

    canvas.blit(pygame.transform.flip(main_character.current_sprite, True, False),
                (main_character.x_pos, main_character.y_pos))

    canvas.blit(main_character.current_hp, (main_character.x_pos, main_character.y_pos+110))

    window.blit(canvas, (0, 0))
    clock.tick(20)
    pygame.display.flip()

