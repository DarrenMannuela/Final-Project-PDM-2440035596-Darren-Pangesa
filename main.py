import pygame
import pygame.freetype
import random
import sys
from MainCharacter import MainCharacter
from Enemy import Enemy
from Button import Buttons

pygame.freetype.init()
# Game name
pygame.display.set_caption("Lieyapath")

# Set Game icon
icon = pygame.image.load("HP\\Health_bar20.png")
pygame.display.set_icon(icon)

# Sets clock to control the FPS
clock = pygame.time.Clock()

# The background image of the game
bg1 = pygame.image.load("Background 1.jpg")

# Size of the window
game_window_width, game_window_height = 640, 480

# Makes the surface for the game
canvas = pygame.Surface((game_window_width, game_window_height))

# Set display size of the window
window = pygame.display.set_mode((game_window_width, game_window_height))


# Text colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Draws text
def draw_text(text: str, font_size: int, font_colour: tuple):
    font = pygame.freetype.Font("ARCADECLASSIC.TTF", font_size)
    text, _ = font.render(text, font_colour)
    return text.convert_alpha()


# Pick an enemy
def pick_enemy(lvl: int):
    pygame.freetype.init()
    enemy_list = [Enemy("Bat", lvl, 10, 2), Enemy("Dragon", lvl, 20, 3), Enemy("Boar", lvl, 10, 5),
                  Enemy("Chest", lvl, 15, 1), Enemy("Ghost", lvl, 14, 4), Enemy("Lizard", lvl, 12, 2),
                  Enemy("Snake", lvl, 10, 3), Enemy("Mushroom", lvl, 12, 3)]
    random_pick = random.randint(0, len(enemy_list)-1)
    enemy = enemy_list[random_pick]
    return enemy


# Start screen
def start_screen():
    title = draw_text("LIEYAPATH", 50, BLACK)
    Start = Buttons("START", (320, 210), 35, BLACK)
    Quit = Buttons("QUIT", (320, 270), 35, BLACK)
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if Start.position.collidepoint(event.pos):
                    controls_screen()
                if Quit.position.collidepoint(event.pos):
                    pygame.quit()

        canvas.blit(bg1, (0, 0))
        canvas.blit(title, (195, 30))
        Start.draw(canvas)
        Start.check_for_mouse(pos)
        Quit.draw(canvas)
        Quit.check_for_mouse(pos)
        window.blit(canvas, (0, 0))
        pygame.display.flip()


# Control screen
def controls_screen():
    # Creates the key instructions
    w_key = draw_text("PRESS W          TO   GO   UP", 35, BLACK)
    a_key = draw_text("PRESS A          TO   GO   LEFT", 35, BLACK)
    s_key = draw_text("PRESS S          TO   GO   DOWN", 35, BLACK)
    d_key = draw_text("PRESS D          TO   GO   RIGHT", 35, BLACK)
    to_continue = draw_text("PRESS    ENTER    TO    CONTINUE", 25, BLACK)
    to_start = draw_text("PRESS       ESCAPE   TO    START ", 25, BLACK)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                # When pressing enter go to game
                if event.key == pygame.K_RETURN:
                    # Make Player
                    player = MainCharacter()
                    battle_sys(player, 1)

                # When pressing the escape key return back to start screen
                if event.key == pygame.K_ESCAPE:
                    start_screen()

        canvas.blit(bg1, (0, 0))
        canvas.blit(to_start, (10, 10))
        canvas.blit(w_key, (160, 155))
        canvas.blit(a_key, (160, 205))
        canvas.blit(s_key, (160, 255))
        canvas.blit(d_key, (160, 305))
        canvas.blit(to_continue, (320, 450))
        window.blit(canvas, (0, 0))
        pygame.display.flip()


# Pause screen
def pause_screen():
    # Creates pause and resume text

    pause_text = draw_text("PAUSED", 60, WHITE)
    to_resume = draw_text("TO CONTINUE PRESS  P", 30, WHITE)
    to_quit = draw_text("TO QUIT PRESS  Q", 30, WHITE)

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause = False
                if event.key == pygame.K_q:
                    pause = False
                    start_screen()
        canvas.fill(BLACK)
        canvas.blit(pause_text, (225, 200))
        canvas.blit(to_resume, (180, 250))
        canvas.blit(to_quit, (220, 300))
        window.blit(canvas, (0, 0))
        pygame.display.flip()


# Main battle system
def battle_sys(hero, current_lvl: int):
    # Current level
    level = current_lvl

    # Creating the Main Character & Enemy by using the respective class
    main_character = hero
    enemy = pick_enemy(level)
    # Initial timer to set the enemy to run
    pygame.time.set_timer(enemy.IDLE, 1000, True)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Player events
            if event.type == pygame.KEYDOWN:
                main_character.next_level = False
                # Move the player up
                if event.key == pygame.K_w:
                    main_character.current_animation = main_character.animations["Idle"]
                    pygame.event.set_blocked(pygame.KEYDOWN)
                    main_character.movement(y=90)

                    if enemy.enemy_rect.collidepoint((main_character.x_pos, main_character.y_pos)):
                        main_character.current_animation = main_character.animations["Hit"]
                        main_character.hp -= enemy.atk

                        # Disabling the key up and key down events so that the player cannot move if hit
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        pygame.event.set_blocked(pygame.KEYUP)
                        main_character.got_hit = True

                # Move the player back
                if event.key == pygame.K_a:
                    main_character.current_animation = main_character.animations["Idle"]
                    pygame.event.set_blocked(pygame.KEYDOWN)
                    main_character.movement(x=70)

                # Move the player down
                if event.key == pygame.K_s:
                    main_character.current_animation = main_character.animations["Idle"]
                    pygame.event.set_blocked(pygame.KEYDOWN)
                    main_character.movement(y=-120)

                    if enemy.enemy_rect.collidepoint((main_character.x_pos, main_character.y_pos)):
                        main_character.current_animation = main_character.animations["Hit"]
                        main_character.hp -= enemy.atk

                        # Disabling the key up and key down events so that the player cannot move if hit
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        pygame.event.set_blocked(pygame.KEYUP)
                        main_character.got_hit = True

                # Move the player to attack
                if event.key == pygame.K_d:
                    # Set block to Key down events
                    pygame.event.set_blocked(pygame.KEYDOWN)

                    # Set timer to go to MOVE event once
                    pygame.time.set_timer(main_character.MOVE, 5, True)

            #  Key up events are to return the Main Character to the original position
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    main_character.current_animation = main_character.animations["Idle"]
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    main_character.return_to_origin()

                if event.key == pygame.K_a:
                    main_character.current_animation = main_character.animations["Idle"]
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    main_character.return_to_origin()

                if event.key == pygame.K_s:
                    main_character.current_animation = main_character.animations["Idle"]
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    main_character.return_to_origin()

            # Set timer to RECOVER event when d key is pressed
                if event.key == pygame.K_d:
                    pygame.time.set_timer(main_character.RECOVER, 350, True)

                if event.key == pygame.K_p:
                    pause_screen()

            # Moves the player forward until it satisfies the conditional
            if event.type == main_character.MOVE:
                main_character.movement(-100)
                if main_character.x_pos < 400:
                    pygame.time.set_timer(main_character.MOVE, 1, True)
                else:
                    main_character.current_animation = main_character.animations["Attack"]
                    if enemy.enemy_rect.collidepoint((main_character.x_pos, main_character.y_pos)):
                        enemy.current_animation = enemy.animations["Hit"]
                        enemy.hp -= main_character.atk
                        enemy.got_hit = True
                        pygame.event.get(enemy.IDLE)

            # Returns the player to the original position
            if event.type == main_character.RECOVER:
                pygame.event.set_blocked(pygame.KEYDOWN)
                main_character.current_animation = main_character.animations["Idle"]
                main_character.movement(150)
                enemy.got_hit = False
                if main_character.x_pos > 40:
                    pygame.time.set_timer(main_character.RECOVER, 1, True)
                else:
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    main_character.return_to_origin()

            if event.type == main_character.GAIN_EXP:
                # To indicate the enemy has been killed
                main_character.killed = True

                # To draw the you win text onto the screen
                main_character.you_win = True

                # Calls the gain exp method from the main character class and gets the enemy.give exp as a parameter
                main_character.gain_exp(enemy.give_exp)

                # Sets the timer to go to the next level
                pygame.time.set_timer(main_character.LEVEL_UP, 2000, True)

            if event.type == main_character.LEVEL_UP:
                # Resets the killed boolean of the player
                main_character.killed = False

                # Stop health bar shaking if the player has one whilst also getting hit by the enemy
                main_character.got_hit = False

                # Stop drawing the you win text on the screen
                main_character.you_win = False

                # Allows the text of Level up to appear
                main_character.next_level = True

                # Allows the following events into the event queue
                pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, main_character.MOVE, main_character.RECOVER,
                                          enemy.IDLE, enemy.WINDUP, enemy.ATTACK_DOWN, enemy.ATTACK_UP,
                                          enemy.ATTACK_FORWARD, enemy.RECOVER, enemy.HIT])

                # Increment level by 1
                level += 1

                # Clears the event queue
                pygame.event.clear()

                # Repeats the function with the new level and new stats of the player
                battle_sys(main_character, level)

            if event.type == main_character.LEVEL_DOWN:
                enemy.killed = True
                main_character.you_lose = True
                main_character.got_hit = False

                pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, main_character.MOVE, main_character.RECOVER,
                                          enemy.IDLE, enemy.WINDUP, enemy.ATTACK_DOWN, enemy.ATTACK_UP,
                                          enemy.ATTACK_FORWARD, enemy.RECOVER, enemy.HIT])

                main_character.current_animation = main_character.animations["Idle"]
                main_character.hp = main_character.full_hp
                main_character.current_health = main_character.hp_bar[20]
                pygame.event.clear()
                if level > 2:
                    battle_sys(main_character, level-2)
                else:
                    battle_sys(main_character, 1)

            # Enemy events

            # Set the enemy animation to Idle
            if event.type == enemy.IDLE:
                enemy.killed = False
                main_character.you_lose = False
                enemy.current_animation = enemy.animations["Idle"]
                pygame.event.clear(enemy.WINDUP)
                enemy.return_to_origin()

                # See if the enemy will attack
                go_attack = random.randint(1, 5)

                if go_attack == 1:
                    # Set timer for WINDUP event
                    pygame.time.set_timer(enemy.WINDUP, 1000, True)

                if go_attack == 3:
                    # Set timer for WINDUP event
                    pygame.time.set_timer(enemy.WINDUP, 1000, True)
                else:
                    # Repeats the IDLE event until the enemy chooses to attack
                    pygame.time.set_timer(enemy.IDLE, 100, True)

            # Set the animation to Windup
            if event.type == enemy.WINDUP:
                enemy.current_animation = enemy.animations["Windup"]

                # See where the enemy will attack
                where_attack = random.randint(1, 3)

                # The enemy moves back
                enemy.move(-30)

                if where_attack == 1:
                    # Set timer for the ATTACK_FORWARD event & allows the arrow indicator to be drawn
                    enemy.arrow_forward = True
                    pygame.time.set_timer(enemy.ATTACK_FORWARD, 500, True)

                if where_attack == 2:
                    # Set timer for the ATTACK_UP event & allows the arrow indicator to be drawn
                    enemy.arrow_up = True
                    pygame.time.set_timer(enemy.ATTACK_UP, 500, True)

                if where_attack == 3:
                    # # Set timer for the ATTACK_DOWN event & allows the arrow indicator to be drawn
                    enemy.arrow_down = True
                    pygame.time.set_timer(enemy.ATTACK_DOWN, 500, True)

            # Set the enemy animation to Attack and attack forward
            if event.type == enemy.ATTACK_FORWARD:
                enemy.current_animation = enemy.animations["Attack"]
                enemy.arrow_forward = False
                # Moves the enemy towards the player
                enemy.move(50)

                # Repeats the Attack forward event until it satisfies the conditional
                if enemy.x_pos_enemy > 100:

                    # If the enemy hit the player
                    if main_character.character_rect.collidepoint((enemy.x_pos_enemy, enemy.y_pos_enemy)):
                        main_character.current_animation = main_character.animations["Hit"]
                        main_character.hp -= enemy.atk

                        # Disabling the key up and key down events so that the player cannot move if hit
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        pygame.event.set_blocked(pygame.KEYUP)
                        main_character.got_hit = True

                    pygame.time.set_timer(enemy.ATTACK_FORWARD, 5, True)
                else:
                    # Set timer to RECOVER event
                    pygame.time.set_timer(enemy.RECOVER, 1500, True)

            # Set the enemy animation to Attack and attack upwards
            if event.type == enemy.ATTACK_UP:
                enemy.current_animation = enemy.animations["Attack"]

                enemy.arrow_up = False
                # Moves the enemy towards the player
                enemy.move(50, 15)

                # Repeats the Attack forward event until it satisfies the conditional

                if enemy.x_pos_enemy > 100:

                    # If the enemy hit the player
                    if main_character.character_rect.collidepoint((enemy.x_pos_enemy, enemy.y_pos_enemy)):
                        main_character.current_animation = main_character.animations["Hit"]
                        main_character.hp -= enemy.atk

                        # Disabling the key up and key down events so that the player cannot move if hit
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        pygame.event.set_blocked(pygame.KEYUP)
                        main_character.got_hit = True

                    pygame.time.set_timer(enemy.ATTACK_UP, 5, True)
                else:
                    # Set timer to RECOVER event
                    pygame.time.set_timer(enemy.RECOVER, 1500, True)

            # Set the enemy animation to Attack and attack downwards
            if event.type == enemy.ATTACK_DOWN:
                enemy.current_animation = enemy.animations["Attack"]
                enemy.arrow_down = False

                # Moves the enemy towards the player
                enemy.move(50, -10)

                # Repeats the Attack forward event until it satisfies the conditional
                if enemy.x_pos_enemy > 100:

                    # If the enemy hit the player
                    if main_character.character_rect.collidepoint((enemy.x_pos_enemy, enemy.y_pos_enemy)):
                        main_character.current_animation = main_character.animations["Hit"]
                        main_character.hp -= enemy.atk

                        # Disabling the key up and key down events so that the player cannot move if hit
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        pygame.event.set_blocked(pygame.KEYUP)
                        main_character.got_hit = True

                    pygame.time.set_timer(enemy.ATTACK_DOWN, 5, True)
                else:
                    # Set timer to RECOVER event
                    pygame.time.set_timer(enemy.RECOVER, 1500, True)

            # Allows the enemy to return to original position
            if event.type == enemy.RECOVER:
                enemy.current_animation = enemy.animations["Idle"]

                enemy.move(-50)

                # If Player got hit by the enemy
                if main_character.got_hit:
                    main_character.current_animation = main_character.animations["Idle"]

                    # Enables key up and key down events after getting hit
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    pygame.event.set_allowed(pygame.KEYUP)

                    # Returns the player to its original position
                    main_character.return_to_origin()

                main_character.got_hit = False

                # Repeats until condition is satisfied
                if enemy.x_pos_enemy < 490:
                    pygame.time.set_timer(enemy.RECOVER, 5, True)
                else:
                    enemy.return_to_origin()
                    enemy.current_animation = enemy.animations["Idle"]
                    pygame.time.set_timer(enemy.IDLE, 2500, True)

        if enemy.got_hit:
            enemy.shake_health()

        if main_character.got_hit:
            main_character.shake_health()

        # Draw the rectangle of the player based on current coordinates
        main_character.rect()

        # Draw the rectangle of the enemy based on current coordinates
        enemy.rect()

        # Updates the sprites based on animation list
        main_character.update()
        enemy.update()

        # Updates health bar of the enemy & player
        main_character.health_bar()
        enemy.health_bar()

        # Draws background image
        canvas.blit(bg1, (0, 0))

        # Drawing the hp bar and level of the enemy
        canvas.blit(pygame.transform.flip(enemy.current_health, True, False), (enemy.x_pos_hp, enemy.y_pos_hp))
        canvas.blit(enemy.show_hp, (enemy.x_pos_hp + 65, enemy.y_pos_hp + 45))
        canvas.blit(enemy.show_lvl, (enemy.x_pos_enemy + 30, enemy.y_pos_enemy - 25))

        # Drawing the stats of the player
        canvas.blit(main_character.current_health, (main_character.x_hp, main_character.y_hp))
        canvas.blit(main_character.show_hp, (main_character.x_hp + 65, main_character.y_hp + 45))
        canvas.blit(main_character.show_lvl, (main_character.x_pos + 65, main_character.y_pos - 25))
        canvas.blit(main_character.show_exp, (main_character.x_pos + 30, main_character.y_pos - 5))

        # Draws the player and enemy sprites
        canvas.blit(pygame.transform.flip(main_character.current_sprite, True, False),
                    (main_character.x_pos, main_character.y_pos))

        canvas.blit(pygame.transform.flip(enemy.current_sprite, True, False), (enemy.x_pos_enemy, enemy.y_pos_enemy))

        # Draws an arrow forward if enemy.arrow_forward returns True
        if enemy.arrow_forward:
            canvas.blit(enemy.arrow, (enemy.x_pos_enemy - 40, enemy.y_pos_enemy + 20))

        # Draws an arrow forward if enemy.arrow_up returns True
        if enemy.arrow_up:
            canvas.blit(pygame.transform.rotate(enemy.arrow, -45), (enemy.x_pos_enemy - 40, enemy.y_pos_enemy + 20))

        # Draws an arrow forward if enemy.arrow_down returns True
        if enemy.arrow_down:
            canvas.blit(pygame.transform.rotate(enemy.arrow, 45), (enemy.x_pos_enemy - 40, enemy.y_pos_enemy + 20))

        # Draws the you win text if main_character.you_win returns True
        if main_character.you_win:
            canvas.blit(draw_text("YOU WIN", 60, BLACK), (230, 240))

        # Draws the you win text if main_character.next_level returns True
        if main_character.next_level:
            canvas.blit(draw_text("LEVEL {}".format(level), 60, BLACK), (220, 100))

        # Draws the you win text if main_character.you_lose returns True
        if main_character.you_lose:
            canvas.blit(draw_text("YOU  LOSE", 60, BLACK), (220, 240))

        # Checks if the enemy's hp reaches 0 or less
        if enemy.hp <= 0:
            enemy.current_animation = enemy.animations["Hit"]
            enemy.hp = 0
            if not main_character.killed:
                pygame.time.set_timer(main_character.GAIN_EXP, 1, True)

            # Blocks and clears event queue
            pygame.event.set_blocked([pygame.KEYDOWN, pygame.KEYUP, main_character.MOVE, main_character.RECOVER,
                                      enemy.IDLE, enemy.WINDUP, enemy.ATTACK_DOWN, enemy.ATTACK_UP,
                                      enemy.ATTACK_FORWARD, enemy.RECOVER, enemy.HIT])

            main_character.current_animation = main_character.animations["Idle"]
            main_character.movement(50)
            if main_character.x_pos >= 40:
                main_character.movement(50)
            if main_character.x_pos <= 40:
                main_character.return_to_origin()
                pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, main_character.MOVE, main_character.RECOVER,
                                          enemy.IDLE, enemy.WINDUP, enemy.ATTACK_DOWN, enemy.ATTACK_UP,
                                          enemy.ATTACK_FORWARD, enemy.RECOVER, enemy.HIT])

        # Checks if the player's hp reaches 0 or less
        if main_character.hp <= 0:
            main_character.current_animation = main_character.animations["Hit"]
            main_character.hp = 0

            # Returns enemy and player to original positions
            enemy.return_to_origin()
            main_character.return_to_origin()

            if not enemy.killed:
                pygame.time.set_timer(main_character.LEVEL_DOWN, 1, True)

            # Blocks and clears event queue
            pygame.event.set_blocked([pygame.KEYDOWN, pygame.KEYUP, main_character.MOVE, main_character.RECOVER,
                                      enemy.IDLE, enemy.WINDUP, enemy.ATTACK_DOWN, enemy.ATTACK_UP,
                                      enemy.ATTACK_FORWARD, enemy.RECOVER, enemy.HIT])
            pygame.event.clear()
        window.blit(canvas, (0, 0))
        clock.tick(20)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.freetype.init()
    start_screen()
