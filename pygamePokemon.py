"""Python Pokemon Pygame."""
import pygame
import pygame.locals
import sys
import random
import time
import requests
import io
import colorsys

LIGHT_BLUE = (59, 125, 213)
DARK_BLUE = (7, 0, 142)
RED = (255, 0, 0)
GREEN = (29, 159, 74)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (241, 255, 78)

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

pygame.init()

pygame.display.set_caption("It's Pokemon bitch!")

FPS = 60
FramePerSec = pygame.time.Clock()

# Setting up fonts
font_large = pygame.font.Font("Pokemon GB.ttf", 60)
font_medium = pygame.font.Font("Pokemon GB.ttf", 20)
font_small = pygame.font.Font("Pokemon GB.ttf", 14)

# Setting up strings to print
game_over_text = "Game Over"
game_over = font_large.render(game_over_text, True, BLACK)
game_over_size = font_large = font_large.size(game_over_text)

button_text = font_medium.render("Attack", True, YELLOW)
welcome_text = """Hello there! Welcome to the world of Pokémon!
    My name is Oak! People call me the Pokémon Prof!
    This world is inhabited by creatures called Pokémon!
    For some people, Pokémon are pets. Other use them for fights.
    Myself… I study Pokémon as a profession."""

background = pygame.image.load("background.png")  # 240x112
background = pygame.transform.scale(background, RESOLUTION)

DISPLAYSURF = pygame.display.set_mode(RESOLUTION)
DISPLAYSURF.fill(WHITE)
DISPLAYSURF.blit(background, (0, 0))


class Player(pygame.sprite.Sprite):
    """Create a pokemon container."""

    def __init__(self, pokemon, location):
        """Create an instance of the class."""
        super().__init__()

        self.request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/")
        self.pokemon_name = pokemon.capitalize()
        self.pokemon_location = location
        self.pokemon_level = 99
        self.pokemon_base_hp = self.request.json()['stats'][0]['base_stat']
        self.pokemon_base_attack = self.request.json()['stats'][1]['base_stat']
        self.pokemon_base_defense = self.request.json()['stats'][2]['base_stat']
        self.pokemon_base_special_attack = self.request.json()['stats'][3]['base_stat']
        self.pokemon_base_special_defense = self.request.json()['stats'][4]['base_stat']
        self.pokemon_base_speed = self.request.json()['stats'][5]['base_stat']
        self.pokemon_sprite_url = self.request.json()['sprites']['front_shiny']
        self.pokemon_first_type = self.request.json()['types'][0]['type']['name']

        try:
            self.pokemon_second_type = self.request.json()['types'][1]['type']['name']
        except IndexError:
            self.pokemon_second_type = None

        self.ev = 256 # actually only goes to 255
        self.iv = 32 # actually only goes to 31
        self.pokemon_hp_percentage = 1.0

        if location == PLAYER_LOCATION:
            self.pokemon_base_location = BASE_PLAYER_LOCATION
        else:
            self.pokemon_base_location = BASE_ENEMY_LOCATION

        self.image = requests.get(self.pokemon_sprite_url)
        self.image = io.BytesIO(self.image.content)
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale(self.image, SPRITE_SIZE)
        self.surf = pygame.Surface(SPRITE_SIZE)
        self.rect = self.image.get_rect(topleft=self.pokemon_location)

        self.pokemon_bg_hp_bar_location = [
            self.pokemon_base_location[0],
            self.pokemon_base_location[1]-5,
            150,
            10]

        self.is_moving = False

        if self.pokemon_location == PLAYER_LOCATION:
            self.direction = "right"
        else:
            self.direction = "left"

        self.scale_stats_level_99()
        self.update_hp_bar()

    def print_stats(self):
        """Print pokemon stats."""
        print(f"{self.pokemon_name} stats:")
        print(f"Pokemon Primary Type:       {self.pokemon_first_type}")
        print(f"Pokemon Secondary Type:     {self.pokemon_second_type}")
        print(f"Pokemon HP:                 {self.pokemon_hp}")
        print(f"Pokemon Attack:             {self.pokemon_attack}")
        print(f"Pokemon Defense:            {self.pokemon_defense}")
        print(f"Pokemon Special Attack:     {self.pokemon_special_attack}")
        print(f"Pokemon Special Defense:    {self.pokemon_special_defense}")
        print(f"Pokemon Speed:              {self.pokemon_speed}")
        print(f"Pokemon Location:           {self.pokemon_location}")
        print(f"Pokemon Is Moving:          {self.is_moving}\n")

    def scale_stats_level_99(self):
        """
        Set stats scaled to level 99 stats.

        Using max and uniform values for IV and EV, scale base stats to level
        99 stat for pokemon.
        """
        self.pokemon_max_hp = scale_hp(
            self.pokemon_base_hp,
            self.iv,
            self.ev,
            self.pokemon_level)
        self.pokemon_attack = scale_stat(
            self.pokemon_base_attack,
            self.iv,
            self.ev,
            self.pokemon_level)
        self.pokemon_defense = scale_stat(
            self.pokemon_base_defense,
            self.iv,
            self.ev,
            self.pokemon_level)
        self.pokemon_special_attack = scale_stat(
            self.pokemon_base_special_attack,
            self.iv,
            self.ev,
            self.pokemon_level)
        self.pokemon_special_defense = scale_stat(
            self.pokemon_base_special_defense,
            self.iv,
            self.ev,
            self.pokemon_level)
        self.pokemon_speed = scale_stat(
            self.pokemon_base_speed,
            self.iv,
            self.ev,
            self.pokemon_level)

        self.pokemon_hp = self.pokemon_max_hp

    def take_damage(self, damage):
        """Reduce pokemon hp by damage amount and run update hp bar."""
        self.pokemon_hp -= damage
        print(f"{self.pokemon_name} took {damage} damage.\n")
        self.update_hp_bar()

    def update_hp_bar(self):
        """Update hp bar percent and color."""
        self.pokemon_hp_percentage = self.pokemon_hp/self.pokemon_max_hp
        if self.pokemon_hp_percentage < 0:
            self.pokemon_hp_percentage = 0
        self.pokemon_hp_bar_location = [
            self.pokemon_base_location[0],
            self.pokemon_base_location[1]-5,
            150*self.pokemon_hp_percentage,
            10]

        # HSV to RGB calculation for Green to Red hp bar color
        self.h, self.s, self.v = 0.33*self.pokemon_hp_percentage, 1, 1
        self.r, self.g, self.b = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        self.hp_bar_color = [int(255*self.r), int(255*self.g), int(255*self.b)]

    def update(self, delta=[0, 0]):
        """Update location of sprite."""
        self.rect.move_ip(delta)  # delta is (x, y)
        self.pokemon_location[0] += delta[0]
        self.pokemon_location[1] += delta[1]

    def display(self, screen=DISPLAYSURF):
        """Redraw sprite and hp bars on the screen."""
        screen.blit(self.image, self.pokemon_location)
        pygame.draw.rect(  # Background HP Bar
            surface=screen,
            color=BLACK,
            rect=self.pokemon_bg_hp_bar_location,
            border_radius=5)
        pygame.draw.rect(  # Colored HP Bar
            surface=screen,
            color=self.hp_bar_color,
            rect=self.pokemon_hp_bar_location,
            border_radius=5)


def calculate_damage(attacking_pokemon, defending_pokemon, move_power=180):
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

def scale_hp(base_value, IV, EV, level):
    """
    Use to scale hp value from base to level 99.

    HP = (((2 * Base + IV + (EV / 4)) * Level) / 100) + Level + 10
    """
    scaled_value = ((((2 * base_value + IV + (EV / 4)) * level) / 100)
        + level + 10)
    return int(scaled_value)

def scale_stat(base_value, IV, EV, level):
    """
    Use to scale other stat values from base to level 99.

    Stat = ((((2 * Base + IV + (EV / 4)) * Level) / 100) + 5) * Nature
    Ignoring nature for now
    """
    # TODO: Add nature calculations
    scaled_value = ((((2 * base_value + IV + (EV / 4)) * level) / 100) + 5)
    return int(scaled_value)


def print_end_message():
    """Display end message on the screen."""
    DISPLAYSURF.fill(GREEN)
    who_won_text = f"{loser} is unable to battle, {winner} wins!"
    who_won_size = font_small.size(who_won_text)
    who_won = font_small.render(who_won_text, True, BLACK)
    DISPLAYSURF.blit(game_over, ((SCREEN_WIDTH-game_over_size[0])/2, 50))
    DISPLAYSURF.blit(who_won, ((SCREEN_WIDTH-who_won_size[0])/2, 150))
    pygame.display.update()


# Setting up sprites
P1 = Player("garchomp", PLAYER_LOCATION)
time.sleep(1)
P2 = Player("goodra", ENEMY_LOCATION)

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
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.locals.MOUSEBUTTONDOWN:  # Attack button
            if 0 <= mouse[0] <= 120 and 0 <= mouse[1] <= 30:
                if not P1.is_moving and not P2.is_moving:
                    if whose_turn == "user":
                        P1.is_moving = True
                        whose_turn = "enemy"
                    else:  # if whose_turn == "enemy":
                        P2.is_moving = True
                        whose_turn = "user"
        if event.type == pygame.locals.QUIT:  # System exit window button
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
        if 0 <= mouse[0] <= 120 and 0 <= mouse[1] <= 30:
            pygame.draw.rect(DISPLAYSURF, LIGHT_BLUE, [0, 0, 130, 30])
        else:
            pygame.draw.rect(DISPLAYSURF, DARK_BLUE, [0, 0, 130, 30])
        DISPLAYSURF.blit(button_text, (6, 6))

        # Check if either pokemon has fainted, after done moving
        if P1.pokemon_hp <= 0 or P2.pokemon_hp <= 0:
            if P1.pokemon_hp <= 0 and P2.pokemon_hp <= 0:
                if P1.pokemon_hp > P2.pokemon_hp:
                    winner = P1.pokemon_name
                    loser = P2.pokemon_name
                else:
                    winner = P2.pokemon_name
                    loser = P1.pokemon_name
            elif P1.pokemon_hp <= 0:
                winner = P2.pokemon_name
                loser = P1.pokemon_name
            elif P2.pokemon_hp <= 0:
                winner = P1.pokemon_name
                loser = P2.pokemon_name

            # Display end game screen
            time.sleep(2)
            print_end_message()
            for entity in all_sprites:
                entity.kill()
            time.sleep(2)
            pygame.quit()
            sys.exit()

    # Write all changes to screen
    pygame.display.update()

    # Set FPS
    FramePerSec.tick(FPS)

# TODO: Add attacks with special attack/defense
# TODO: Add movesets for pokemon
# TODO: Allow user to pick pokemon
# TODO: Add Pokemon name and hp value to battle screen
# TODO: Allow option to play again
# TODO: Add music
