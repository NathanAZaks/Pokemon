"""
Python Pokemon Pygame.

Taken from https://coderslegacy.com/python/python-pygame-tutorial/
"""
import pygame
import pygame.locals
import sys
import random
import time
import requests
import io
import colorsys

pygame.init()

pygame.display.set_caption("It's Pokemon bitch!")

FPS = 60
FramePerSec = pygame.time.Clock()

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

SPRITE_SIZE = (150, 150)
HP_BAR_LENGTH = 150

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 336
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Setting up fonts
font_large = pygame.font.Font("Pokemon GB.ttf", 60)
font_medium = pygame.font.Font("Pokemon GB.ttf", 20)
font_small = pygame.font.Font("Pokemon GB.ttf", 14)

# Setting up strings to print
game_over_text = "Game Over"
game_over = font_large.render(game_over_text, True, BLACK)
game_over_size = font_large = font_large.size(game_over_text)

button_text = font_medium.render("Attack", True, YELLOW)
welcome_scroll_text = "Hello there!"  # Welcome to the world of Pokémon! My name is Oak! People call me the Pokémon Prof! This world is inhabited by creatures called Pokémon! For some people, Pokémon are pets. Other use them for fights. Myself… I study Pokémon as a profession."

background = pygame.image.load("background.png")  # 240x112
background = pygame.transform.scale(background, RESOLUTION)

DISPLAYSURF = pygame.display.set_mode(RESOLUTION)
DISPLAYSURF.fill(WHITE)
DISPLAYSURF.blit(background, (0,0))


class Player(pygame.sprite.Sprite):
    """Create a pokemon container."""

    def __init__(self, pokemon, location):
        """Create an instance of the class."""
        super().__init__()

        self.request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/")
        self.pokemon_name = pokemon.capitalize()
        self.pokemon_location = location
        self.pokemon_hp = self.request.json()['stats'][0]['base_stat']
        self.pokemon_max_hp = self.pokemon_hp
        self.pokemon_attack = self.request.json()['stats'][1]['base_stat']
        self.pokemon_defense = self.request.json()['stats'][2]['base_stat']
        self.pokemon_special_attack = self.request.json()['stats'][3]['base_stat']
        self.pokemon_special_defense = self.request.json()['stats'][4]['base_stat']
        self.pokemon_speed = self.request.json()['stats'][5]['base_stat']
        self.pokemon_sprite_url = self.request.json()['sprites']['front_shiny']
        self.pokemon_first_type = self.request.json()['types'][0]['type']['name']
        try:
            self.pokemon_second_type = self.request.json()['types'][1]['type']['name']
        except IndexError:
            self.pokemon_second_type = None
        self.pokemon_hp_percentage = self.pokemon_hp/self.pokemon_max_hp
        if location == PLAYER_LOCATION:
            self.pokemon_base_location = BASE_PLAYER_LOCATION
        else:
            self.pokemon_base_location = BASE_ENEMY_LOCATION

        self.image = requests.get(self.pokemon_sprite_url)
        self.image = io.BytesIO(self.image.content)
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale(self.image, SPRITE_SIZE)
        self.surf = pygame.Surface(SPRITE_SIZE)
        self.rect = self.surf.get_rect(topleft=self.pokemon_location)
        # self.rect = self.image.get_rect(topleft=self.pokemon_location)

    def print_stats(self):
        """Print pokemon stats."""
        print(f"{self.pokemon_name} stats:")
        print(f"Pokemon Primary Type: {self.pokemon_first_type}")
        print(f"Pokemon HP: {self.pokemon_hp}")
        print(f"Pokemon Attack: {self.pokemon_attack}")
        print(f"Pokemon Defense: {self.pokemon_defense}")
        print(f"Pokemon Special Attack: {self.pokemon_special_attack}")
        print(f"Pokemon Special Defense: {self.pokemon_special_defense}")
        print(f"Pokemon Speed: {self.pokemon_speed}")
        print(f"Pokemon Location: {self.pokemon_location}")

    def update(self):
        """Redraw whole screen."""
        DISPLAYSURF.blit(self.image, self.pokemon_location)

        self.pokemon_hp_percentage = self.pokemon_hp/self.pokemon_max_hp
        self.pokemon_hp_bar_location = [
            self.pokemon_base_location[0],
            self.pokemon_base_location[1]-5,
            150*self.pokemon_hp_percentage,
            10]
        self.h, self.s, self.v = 0.33*self.pokemon_hp_percentage, 1, 1
        self.r, self.g, self.b = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        self.hp_bar_color = [int(255*self.r), int(255*self.g), int(255*self.b)]

        pygame.draw.rect(
            DISPLAYSURF,
            BLACK,
            (self.pokemon_base_location[0], self.pokemon_base_location[1]-5, 150, 10),
            border_radius=5)
        pygame.draw.rect(
            DISPLAYSURF,
            self.hp_bar_color,
            self.pokemon_hp_bar_location,
            border_radius=5)

        pygame.display.update()

    def take_damage(self, damage):
        """Reduce pokemon hp by 'damage' amount."""
        self.pokemon_hp -= damage
        print(f"{self.pokemon_name} took {damage} damage.")

    def move(self):
        """Move sprite around screen."""
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[pygame.locals.K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[pygame.locals.K_DOWN]:
                self.rect.move_ip(0, 5)
        if self.rect.left > 0:
            if pressed_keys[pygame.locals.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.locals.K_RIGHT]:
                self.rect.move_ip(5, 0)

    def move_on_attack(self):  # FIXME: This is super ugly and refreshes screen every time
        """Make sprite move to opponent location and back."""
        if self.pokemon_location == BASE_PLAYER_LOCATION:
            while self.pokemon_location != BASE_ENEMY_LOCATION:
                time.sleep(.005)
                self.pokemon_location[0] += 6
                self.pokemon_location[1] -= 2
                DISPLAYSURF.fill(WHITE)
                DISPLAYSURF.blit(background, (0, 0))
                all_sprites.update()
            while self.pokemon_location != BASE_PLAYER_LOCATION:
                time.sleep(.005)
                self.pokemon_location[0] -= 6
                self.pokemon_location[1] += 2
                DISPLAYSURF.fill(WHITE)
                DISPLAYSURF.blit(background, (0, 0))
                all_sprites.update()
        elif self.pokemon_location == BASE_ENEMY_LOCATION:
            while self.pokemon_location != BASE_PLAYER_LOCATION:
                time.sleep(.005)
                self.pokemon_location[0] -= 6
                self.pokemon_location[1] += 2
                DISPLAYSURF.fill(WHITE)
                DISPLAYSURF.blit(background, (0, 0))
                all_sprites.update()
            while self.pokemon_location != BASE_ENEMY_LOCATION:
                time.sleep(.005)
                self.pokemon_location[0] += 6
                self.pokemon_location[1] -= 2
                DISPLAYSURF.fill(WHITE)
                DISPLAYSURF.blit(background, (0, 0))
                all_sprites.update()


def calculate_damage(attacking_pokemon, defending_pokemon, movePower=30):
    """Calculate damage between two pokemon."""
    pokemonLevel = 99
    randValue = random.randint(85, 100)
    atkDmg = ((((((2 * pokemonLevel) / 5) + 2) * movePower * (attacking_pokemon.pokemon_attack / defending_pokemon.pokemon_defense) / 50) + 2) * (randValue/100))
    return round(atkDmg)


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


def text_generator(text):
    """Yield text one letter at a time."""
    tmp = ''
    for letter in text:
        tmp += letter
        if letter != ' ':
            yield tmp


class DynamicText(object):
    """Use to make scrolling text."""

    def __init__(self, font, text, pos, autoreset=False):
        """Use to make constructor for scrolling text."""
        self.done = False
        self.font = font
        self.text = text
        self._gen = text_generator(self.text)
        self.pos = pos
        self.autoreset = autoreset
        self.update()

    def reset(self):
        """Reset text scrolling."""
        self._gen = text_generator(self.text)
        self.done = False
        self.update()

    def update(self):
        """Update screen."""
        if not self.done:
            try:
                self.rendered = self.font.render(next(self._gen), True, DARK_BLUE)
            except StopIteration:
                self.done = True
                if self.autoreset:
                    self.reset()

    def draw(self, screen):
        """Draw on screen."""
        screen.blit(self.rendered, self.pos)


def print_end_message():
    """Display end message on the screen."""
    DISPLAYSURF.fill(GREEN)
    # print(event.message)
    who_won_text = f"{loser} is unable to battle, {winner} wins!"
    who_won_size = font_small.size(who_won_text)
    who_won = font_small.render(who_won_text, True, BLACK)
    DISPLAYSURF.blit(game_over, ((SCREEN_WIDTH-game_over_size[0])/2, 50))
    DISPLAYSURF.blit(who_won, ((SCREEN_WIDTH-who_won_size[0])/2, 150))
    pygame.display.update()


# Setting up sprites
P1 = Player("slaking", PLAYER_LOCATION)
time.sleep(1)
P2 = Player("wailord", ENEMY_LOCATION)

P1.print_stats()
P2.print_stats()

# welcome_message = DynamicText(font_small, welcome_scroll_text, (450, 306))

# Creating sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(P2)

# Adding a new user event
HP_ZERO = pygame.USEREVENT + 1
pokemon_fainted_event = pygame.event.Event(
    HP_ZERO, message="Pokemon fainted and is unable to battle.")

for entity in all_sprites:
    entity.update()

# Game loop
while True:
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.locals.MOUSEBUTTONDOWN:  # Attack button
            if 0 <= mouse[0] <= 120 and 0 <= mouse[1] <= 30:
                if who_is_attacking(P1, P2) == "user":
                    P1.move_on_attack()
                    P2.take_damage(30)
                    P2.print_stats()
                    DISPLAYSURF.fill(WHITE)
                    DISPLAYSURF.blit(background, (0, 0))
                    for entity in all_sprites:
                        entity.update()
                    time.sleep(0.5)
                    P2.move_on_attack()
                    P1.take_damage(30)
                    P1.print_stats()
                else:
                    P2.move_on_attack()
                    P1.take_damage(30)
                    P1.print_stats()
                    DISPLAYSURF.fill(WHITE)
                    DISPLAYSURF.blit(background, (0, 0))
                    for entity in all_sprites:
                        entity.update()
                    time.sleep(0.5)
                    P1.move_on_attack()
                    P2.take_damage(30)
                    P2.print_stats()
                # Clear screen and re-draw all sprites
                DISPLAYSURF.fill(WHITE)
                DISPLAYSURF.blit(background, (0, 0))
                for entity in all_sprites:
                    entity.update()
        if event.type == HP_ZERO:
            time.sleep(2)
            print_end_message()
            time.sleep(2)
            pygame.quit()
            sys.exit()
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    if P1.pokemon_hp <= 0 or P2.pokemon_hp <= 0:
        pygame.event.post(pokemon_fainted_event)
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

    if 0 <= mouse[0] <= 120 and 0 <= mouse[1] <= 30:
        pygame.draw.rect(DISPLAYSURF, LIGHT_BLUE, [0, 0, 130, 30])
    else:
        pygame.draw.rect(DISPLAYSURF, DARK_BLUE, [0, 0, 130, 30])
    DISPLAYSURF.blit(button_text, (6, 6))
    pygame.display.update()

    FramePerSec.tick(FPS)
