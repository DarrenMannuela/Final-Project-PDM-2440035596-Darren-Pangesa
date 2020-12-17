import pygame
import random
from MainCharacter import MainCharacter
from Enemy import Enemy

# Creating the Main Character & Enemy by using the respective class
main_character = MainCharacter()
bat = Enemy("Bat", 20, 1)


pygame.init()
clock = pygame.time.Clock()
bg1 = pygame.image.load("Background 1.jpg")
game_window_width, game_window_height = 640, 480
canvas = pygame.Surface((game_window_width, game_window_height))
window = pygame.display.set_mode((game_window_width, game_window_height))
running = True

# Initial timer to set the enemy to run
pygame.time.set_timer(bat.IDLE, 1000, True)

if __name__ == "__main__":
    while running:
        canvas.blit(bg1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player events

            if event.type == pygame.KEYDOWN:
                # Move the player up
                if event.key == pygame.K_w:
                    main_character.current_animation = main_character.animations["Idle"]
                    main_character.movement(y=75)

                # Move the player back
                if event.key == pygame.K_a:
                    main_character.current_animation = main_character.animations["Idle"]
                    main_character.movement(x=70)

                # Move the player down
                if event.key == pygame.K_s:
                    main_character.current_animation = main_character.animations["Idle"]
                    main_character.movement(y=-120)

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
                    main_character.current_sprite_index = 0
                    main_character.x_pos = 40
                    main_character.y_pos = 210

                if event.key == pygame.K_a:
                    main_character.current_animation = main_character.animations["Idle"]
                    main_character.current_sprite_index = 0
                    main_character.x_pos = 40
                    main_character.y_pos = 210

                if event.key == pygame.K_s:
                    main_character.current_animation = main_character.animations["Idle"]
                    main_character.current_sprite_index = 0
                    main_character.x_pos = 40
                    main_character.y_pos = 210

            # Set timer to RECOVER event when d key is pressed
                if event.key == pygame.K_d:
                    pygame.time.set_timer(main_character.RECOVER, 350, True)

            # Moves the player forward until it satisfies the conditional
            if event.type == main_character.MOVE:
                main_character.movement(-75)
                if main_character.x_pos < 400:
                    pygame.time.set_timer(main_character.MOVE, 1, True)
                else:
                    main_character.current_animation = main_character.animations["Attack"]
                    if bat.enemy_rect.collidepoint((main_character.x_pos, main_character.y_pos)):
                        bat.current_animation = bat.animations["Hit"]
                    pygame.event.get(bat.IDLE)

            # Returns the player to the original position
            if event.type == main_character.RECOVER:
                pygame.event.set_blocked(pygame.KEYDOWN)
                main_character.current_animation = main_character.animations["Idle"]
                main_character.movement(50)
                if main_character.x_pos > 40:
                    pygame.time.set_timer(main_character.RECOVER, 1, True)
                else:
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    main_character.x_pos = 40
                    main_character.y_pos = 210

            # Enemy events

            # Set the enemy animation to Idle
            if event.type == bat.IDLE:
                bat.current_animation = bat.animations["Idle"]
                bat.x_pos_enemy = 490
                bat.y_pos_enemy = 240

                # See if the enemy will attack
                go_attack = random.randint(1, 5)

                if go_attack == 1:
                    # Set timer for WINDUP event
                    pygame.time.set_timer(bat.WINDUP, 1000, True)

                if go_attack == 3:
                    # Set timer for WINDUP event
                    pygame.time.set_timer(bat.WINDUP, 1000, True)
                else:
                    # Repeats the IDLE event until the enemy chooses to attack
                    pygame.time.set_timer(bat.IDLE, 100, True)

            # Set the animation to Windup
            if event.type == bat.WINDUP:
                bat.current_animation = bat.animations["Windup"]
                # See where the enemy will attack
                where_attack = random.randint(1, 3)
                # The enemy moves back
                bat.move(-30)

                if where_attack == 1:
                    # Draws an arrow and set timer for the ATTACK_FORWARD event
                    canvas.blit(bat.arrow, (450, 280))
                    pygame.time.set_timer(bat.ATTACK_FORWARD, 1000, True)

                if where_attack == 2:
                    # Draws an arrow and set timer for the ATTACK_UP event
                    canvas.blit(pygame.transform.rotate(bat.arrow, -45), (450, 250))
                    pygame.time.set_timer(bat.ATTACK_UP, 1000, True)

                if where_attack == 3:
                    # Draws an arrow and set timer for the ATTACK_DOWN event
                    canvas.blit(pygame.transform.rotate(bat.arrow, 45), (450, 250))
                    pygame.time.set_timer(bat.ATTACK_DOWN, 1000, True)

            # Set the enemy animation to Attack and attack forward
            if event.type == bat.ATTACK_FORWARD:
                bat.current_animation = bat.animations["Attack"]

                # Moves the enemy towards the player
                bat.move(50)

                # Repeats the Attack forward event until it satisfies the conditional
                if bat.x_pos_enemy > 100:

                    # If the enemy hit the player
                    if main_character.character_rect.collidepoint((bat.x_pos_enemy, bat.y_pos_enemy)):
                        main_character.current_animation = main_character.animations["Hit"]

                        # Disabling the key up and key down events so that the player cannot move if hit
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        pygame.event.set_blocked(pygame.KEYUP)
                        main_character.got_hit = True
                    pygame.time.set_timer(bat.ATTACK_FORWARD, 5, True)
                else:
                    # Set timer to RECOVER event
                    pygame.time.set_timer(bat.RECOVER, 1500, True)

            # Set the enemy animation to Attack and attack upwards
            if event.type == bat.ATTACK_UP:
                bat.current_animation = bat.animations["Attack"]

                # Moves the enemy towards the player
                bat.move(50, 15)

                # Repeats the Attack forward event until it satisfies the conditional
                if bat.x_pos_enemy > 100:
                    # If the enemy hit the player
                    if main_character.character_rect.collidepoint((bat.x_pos_enemy, bat.y_pos_enemy)):
                        main_character.current_animation = main_character.animations["Hit"]

                        # Disabling the key up and key down events so that the player cannot move if hit
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        pygame.event.set_blocked(pygame.KEYUP)
                        main_character.got_hit = True

                    pygame.time.set_timer(bat.ATTACK_UP, 5, True)
                else:
                    # Set timer to RECOVER event
                    pygame.time.set_timer(bat.RECOVER, 1500, True)

            # Set the enemy animation to Attack and attack downwards
            if event.type == bat.ATTACK_DOWN:
                bat.current_animation = bat.animations["Attack"]

                # Moves the enemy towards the player
                bat.move(50, -10)

                # Repeats the Attack forward event until it satisfies the conditional
                if bat.x_pos_enemy > 100:

                    # If the enemy hit the player
                    if main_character.character_rect.collidepoint((bat.x_pos_enemy, bat.y_pos_enemy)):
                        main_character.current_animation = main_character.animations["Hit"]
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        pygame.event.set_blocked(pygame.KEYUP)
                        main_character.got_hit = True

                    pygame.time.set_timer(bat.ATTACK_DOWN, 5, True)
                else:
                    # Set timer to RECOVER event
                    pygame.time.set_timer(bat.RECOVER, 1500, True)

            # Allows the enemy to return to original position
            if event.type == bat.RECOVER:
                bat.current_animation = bat.animations["Idle"]
                bat.move(-50)

                # If Player got hit by the enemy
                if main_character.got_hit:
                    main_character.current_animation = main_character.animations["Idle"]

                    # Enables key up and key down events
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    pygame.event.set_allowed(pygame.KEYUP)

                    # Returns the player to its original position
                    main_character.x_pos = 40
                    main_character.y_pos = 210

                # Repeats until condition is satisfied
                if bat.x_pos_enemy < 490:
                    pygame.time.set_timer(bat.RECOVER, 5, True)
                else:
                    bat.x_pos_enemy = 490
                    bat.y_pos_enemy = 240
                    bat.current_animation = bat.animations["Idle"]
                    pygame.time.set_timer(bat.IDLE, 2500, True)

        # Draws the rect of the player based on current coordinates
        main_character.character_rect = main_character.current_sprite.get_rect(
            center=(main_character.x_pos, main_character.y_pos))

        # Draws the rect of the enemy based on current coordinates
        bat.enemy_rect = bat.current_sprite.get_rect(center=(bat.x_pos_enemy-30, bat.y_pos_enemy))

        # Updates the sprites based on animation list
        main_character.update()
        bat.update()

        # To draw the health bar of the enemy & player
        main_character.health_bar()
        bat.health_bar()

        # Drawing the sprites of the player & enemy
        canvas.blit(pygame.transform.flip(bat.current_health, True, False), (bat.x_pos_hp, bat.y_pos_hp))

        canvas.blit(main_character.current_hp, (main_character.x_hp, main_character.y_hp))

        canvas.blit(pygame.transform.flip(main_character.current_sprite, True, False),
                    (main_character.x_pos, main_character.y_pos))

        canvas.blit(pygame.transform.flip(bat.current_sprite, True, False), (bat.x_pos_enemy, bat.y_pos_enemy))

        window.blit(canvas, (0, 0))

        clock.tick(20)
        pygame.display.flip()
