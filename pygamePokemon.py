"""Python Pokemon Pygame."""
import pygame
import pygame.locals
import sys
import random
import time
import requests
# import io
# import colorsys
from playerClass import Player

# Init pygame
pygame.init()

# Label window
pygame.display.set_caption("Welcome to Pokemon!")

# Set up some globals
LIGHT_BLUE = (59, 125, 213)
DARK_BLUE = (7, 0, 142)
RED = (255, 0, 0)
GREEN = (29, 159, 74)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (241, 255, 78)
PALE_BLUE = (24, 140, 156)

BASE_PLAYER_LOCATION = [95, 185]
BASE_ENEMY_LOCATION = [455, 65]
PLAYER_LOCATION = [95, 185]
ENEMY_LOCATION = [455, 65]

MOVE_LEFT = (-6, 2)
MOVE_RIGHT = (6, -2)

SPRITE_SIZE = (150, 150)
HP_BAR_LENGTH = 150

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 336
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60
FramePerSec = pygame.time.Clock()

# Setting up fonts
FONT_LARGE = pygame.font.Font("./Assets/Pokemon GB.ttf", 60)
FONT_MEDIUM = pygame.font.Font("./Assets/Pokemon GB.ttf", 20)
FONT_SMALL = pygame.font.Font("./Assets/Pokemon GB.ttf", 12)

# Setting up strings to print
game_over_text = "Game Over"
game_over = FONT_LARGE.render(game_over_text, True, BLACK)
game_over_size = FONT_LARGE = FONT_LARGE.size(game_over_text)

# TODO: Add welcome text to opening screen
welcome_text = """Hello there! Welcome to the world of Pokémon!
    My name is Oak! People call me the Pokémon Prof!
    This world is inhabited by creatures called Pokémon!
    For some people, Pokémon are pets. Other use them for fights.
    Myself… I study Pokémon as a profession."""

# Set up backround from 1 of 7 background options, size: 240x112
background = pygame.image.load(f"./Assets/background{random.randint(0,6)}.png")
background = pygame.transform.scale(background, RESOLUTION)

# Load background music for player
pygame.mixer.music.load('./Assets/background_battle_music.wav')

# Set up game window and print background to screen
DISPLAYSURF = pygame.display.set_mode(RESOLUTION)
DISPLAYSURF.fill(WHITE)
DISPLAYSURF.blit(background, (0, 0))


def calculate_damage(attacking_pokemon, defending_pokemon, move_power=280):
    """
    Calculate damage between two pokemon.

    Damage = ((((((2/5) * level) + 2) * power * (atk/def)) / 50) + 2)
    Damage *= targets*weather*badge*critical*random*stab*type*burn*other
    """
    ratio = attacking_pokemon.pokemon_attack / defending_pokemon.pokemon_defense
    rand_value = random.randint(85, 100)
    atk_dmg = (
        (((0.4*attacking_pokemon.pokemon_level + 2) * move_power * ratio / 50) + 2)
        * (rand_value/100)
    )
    return int(atk_dmg)


def who_is_attacking(user_pokemon, enemy_pokemon):
    """Use to determine which pokemon will attack first."""
    if user_pokemon.pokemon_speed > enemy_pokemon.pokemon_speed:
        attacking = "user"
    elif user_pokemon.pokemon_speed < enemy_pokemon.pokemon_speed:
        attacking = "enemy"
    else:
        if random.randint(0, 1) == 1:
            attacking = "user"
        else:
            attacking = "enemy"
    return attacking


def print_end_message(winner, loser):
    """Display end message on the screen."""
    DISPLAYSURF.fill(GREEN)

    play_again_surf = FONT_MEDIUM.render("Play Again", True, BLACK)
    exit_now_surf = FONT_MEDIUM.render("Exit Now", True, BLACK)

    who_won_text = f"{loser} is unable to battle, {winner} wins!"
    who_won_size = FONT_SMALL.size(who_won_text)
    who_won = FONT_SMALL.render(who_won_text, True, BLACK)

    DISPLAYSURF.blit(game_over, ((SCREEN_WIDTH-game_over_size[0])/2, 50))
    DISPLAYSURF.blit(who_won, ((SCREEN_WIDTH-who_won_size[0])/2, 150))

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.locals.MOUSEBUTTONDOWN:  # Attack button
                if 50 <= mouse[0] <= 260 and 200 <= mouse[1] <= 230:  # play again
                    print("return from play again")
                    return
                elif 300 <= mouse[0] <= 470 and 200 <= mouse[1] <= 230:  # quit
                    still_playing = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.locals.QUIT:  # System exit window button
                pygame.quit()
                sys.exit()
        if 50 <= mouse[0] <= 260 and 200 <= mouse[1] <= 230: # play again
            play_again_color = LIGHT_BLUE
        else:
            play_again_color = DARK_BLUE
        if 300 <= mouse[0] <= 470 and 200 <= mouse[1] <= 230: # exit now
            exit_now_color = LIGHT_BLUE
        else:
            exit_now_color = DARK_BLUE

        pygame.draw.rect(DISPLAYSURF, play_again_color, [50, 200, 210, 30])
        pygame.draw.rect(DISPLAYSURF, exit_now_color, [300, 200, 170, 30])
        DISPLAYSURF.blit(play_again_surf, (55, 205))
        DISPLAYSURF.blit(exit_now_surf, (305, 205))

        # Write all changes to screen
        pygame.display.update()
        FramePerSec.tick(FPS)


def choose_pokemon(player_or_enemy):
    """Use to allow user to select which pokemon."""
    choose_pokemon_string = f"Choose {player_or_enemy} pokemon. (Enter a Pokemon name or random)"
    choose_pokemon_surf = FONT_SMALL.render(choose_pokemon_string, True, BLACK)
    choose_pokemon_size = FONT_SMALL.size(choose_pokemon_string)
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(background, (0, 0))
    input_box = pygame.Rect(
        290,
        180,
        140,
        32)
    user_choice = ''
    done = False
    while True:
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print(user_choice)
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_choice = user_choice[:-1]
                    else:
                        user_choice += event.unicode

            DISPLAYSURF.fill(WHITE)
            DISPLAYSURF.blit(background, (0, 0))

            # Render the current text.
            txt_surface = FONT_MEDIUM.render(user_choice, True, BLACK)

            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            input_box.x = 360 - (width/2)

            # Blit the input_box rect.
            pygame.draw.rect(DISPLAYSURF, PALE_BLUE, input_box)

            # Blit the text.
            DISPLAYSURF.blit(txt_surface, (input_box.x+5, input_box.y+5))
            DISPLAYSURF.blit(choose_pokemon_surf,
                (360 - (choose_pokemon_size[0]/2),
                168 - (choose_pokemon_size[1]/2)))

            pygame.display.update()
            FramePerSec.tick(FPS)

        user_choice = user_choice.lower()

        if user_choice == "random" or user_choice == "":
            random_number = str(random.randint(1, 898))
            user_choice_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random_number}/")
        else:
            user_choice_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{user_choice}/")
        # TODO: Add more specific Error Messages
        if user_choice_data.status_code != 200:
            print(f"Sorry, {user_choice} is not a recognized pokemon. Check your spelling, maybe?")
            user_choice = ''
            done = False
        else:
            done = True
            user_choice = user_choice_data.json()['name']
            print(f"{user_choice.capitalize()} was chosen!")
            return user_choice


def battle_screen(P1, P2):
    # Set up attack button text
    button_text = FONT_MEDIUM.render("Attack", True, YELLOW)

    # Display stats to terminal
    P1.print_stats()
    P2.print_stats()

    # Creating sprite groups
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(P2)

    # Draw sprites to screen
    for entity in all_sprites:
        entity.update()
        entity.display()

    # Determine who attacks first
    whose_turn = who_is_attacking(P1, P2)

    # Game loop
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                # Attack button
                if 0 <= mouse[0] <= 130 and 0 <= mouse[1] <= 30:
                    if not P1.is_moving and not P2.is_moving:
                        if whose_turn == "user":
                            P1.is_moving = True
                            whose_turn = "enemy"
                        else:  # if whose_turn == "enemy":
                            P2.is_moving = True
                            whose_turn = "user"
            # System exit window button, close game
            if event.type == pygame.locals.QUIT:
                for entity in all_sprites:
                    entity.kill()
                pygame.quit()
                sys.exit()

        # Blit background
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(background, (0, 0))

        # Update sprite locations while attack moving
        if P1.is_moving:
            if P1.direction == "right":
                if P1.pokemon_location != BASE_ENEMY_LOCATION:
                    P1.update(MOVE_RIGHT)
                    P1.display()
                else:
                    P1.direction = "left"
                    P2.take_damage(calculate_damage(P1, P2))
            elif P1.direction == "left":
                if P1.pokemon_location != BASE_PLAYER_LOCATION:
                    P1.update(MOVE_LEFT)
                    P1.display()
                else:
                    P1.is_moving = False
                    P1.direction = "right"
                    P2.print_stats()
                    P1.update()
                    P1.display()
        else:
            P1.update()
            P1.display()

        if P2.is_moving:
            if P2.direction == "left":
                if P2.pokemon_location != BASE_PLAYER_LOCATION:
                    P2.update(MOVE_LEFT)
                    P2.display()
                else:
                    P2.direction = "right"
                    P1.take_damage(calculate_damage(P2, P1))
            elif P1.direction == "right":
                if P2.pokemon_location != BASE_ENEMY_LOCATION:
                    P2.update(MOVE_RIGHT)
                    P2.display()
                else:
                    P2.is_moving = False
                    P2.direction = "left"
                    P1.print_stats()
                    P2.update()
                    P2.display()
        else:
            P2.update()
            P2.display()

        # Make sure neither pokemon is moving
        if not P1.is_moving and not P2.is_moving:
            # Display attack button only if neither is moving
            if 0 <= mouse[0] <= 130 and 0 <= mouse[1] <= 30:
                attack_button_color = LIGHT_BLUE
            else:
                attack_button_color = DARK_BLUE
            pygame.draw.rect(DISPLAYSURF, attack_button_color, [0, 0, 130, 30])
            DISPLAYSURF.blit(button_text, (6, 6))

            # Check if either pokemon has fainted -> game over screen
            if P1.pokemon_hp <= 0 or P2.pokemon_hp <= 0:
                if P1.pokemon_hp <= 0:
                    winner = P2.pokemon_name
                    loser = P1.pokemon_name
                elif P2.pokemon_hp <= 0:
                    winner = P1.pokemon_name
                    loser = P2.pokemon_name

                # Display end game screen
                time.sleep(2)
                print_end_message(winner, loser)
                print("can i get here bro")
                for entity in all_sprites:
                    entity.kill()
                return

        # Write all changes to screen
        pygame.display.update()
        FramePerSec.tick(FPS)


def main():
    # TODO: add welcome_to_pokemon_screen()

    # initialize outer game loop
    still_playing = True

    # play background music on loop
    # pygame.mixer.music.play(-1)

    while still_playing:
        print("Select user pokemon.")
        P1 = Player(choose_pokemon("player"), PLAYER_LOCATION, DISPLAYSURF)
        print("Select opponent pokemon.")
        P2 = Player(choose_pokemon("enemy"), ENEMY_LOCATION, DISPLAYSURF)

        battle_screen(P1, P2)
        print("Do i even get here?")

    pygame.mixer.music.stop()


if __name__ == "__main__":
    main()

# TODO: Add attacks with special attack/defense
# TODO: Add movesets for pokemon
# TODO: Split code into other files
