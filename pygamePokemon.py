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

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

LIGHT_BLUE = (59, 125, 213)
DARK_BLUE = (7, 0, 142)
RED = (255, 0, 0)
GREEN = (29, 159, 74)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (241, 255, 78)

PLAYER_LOCATION = (160, 240)
ENEMY_LOCATION = (500, 120)

SCREEN_WIDTH = 720  # 400
SCREEN_HEIGHT = 336  # 600
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
SPEED = 5
SCORE = 0

# Setting up fonts
font = pygame.font.Font("Pokemon GB.ttf", 60)
font_small = pygame.font.Font("Pokemon GB.ttf", 20)

# Setting up strings to print
game_over = font.render("Game Over", True, BLACK)
button_text = font_small.render("Attack", True, YELLOW)
welcome_scroll_text = "Hello there!"  # Welcome to the world of Pokémon! My name is Oak! People call me the Pokémon Prof! This world is inhabited by creatures called Pokémon! For some people, Pokémon are pets. Other use them for fights. Myself… I study Pokémon as a profession."

background = pygame.image.load("background.png")  # 240x112
background = pygame.transform.scale(background, RESOLUTION)

salamence = pygame.image.load("salamence.png")
salamence = pygame.transform.scale(salamence, (150, 150))
dragonite = pygame.image.load("dragonite.png")
dragonite = pygame.transform.scale(dragonite, (150, 150))

DISPLAYSURF = pygame.display.set_mode(RESOLUTION)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("It's Pokemon bitch!")

pygame.time.set_timer(pygame.USEREVENT, 250)


class Player(pygame.sprite.Sprite):
    """Create a pokemon container."""



    def __init__(self, pokemon, image, location):
        """Create an instance of the class."""
        super().__init__()
        # self.pokemonName = pokemon
        self.image = image
        self.surf = pygame.Surface((150, 150))
        self.rect = self.surf.get_rect(center=location)

        self.pokemonName = pokemon
        self.pokemonHp = 100
        self.pokemonAttack = 100
        self.pokemonDefense = 100
        self.pokemonSpecialAttack = 100
        self.pokemonSpecialDefense = 100
        self.pokemonSpeed = 100
        self.pokemonFirstType = "flying"

        # while True:
        #     # print("What pokemon do you choose? (Enter a Pokemon name or 'random'): ")
        #     # self.pokemonChoice = str.lower(input(""))
        #     self.pokemonChoice = pokemon
        #     if self.pokemonChoice == "random":
        #         # self.randomNumber = str(random.randint(1, 898))
        #         # self.pokemonChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.randomNumber}/")
        #         pass
        #     else:
        #         self.pokemonChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.pokemonChoice}/")
        #     # TODO: Add more specific Error Messages
        #     if self.pokemonChoiceData.status_code != 200:
        #         # print(f"Sorry, {self.pokemonChoice.capitalize()} is not a recognized pokemon. Check your spelling, maybe?")
        #         pass
        #     else:
        #         break
        #
        # self.pokemonName = self.pokemonChoiceData.json()['name']
        # self.pokemonHp = self.pokemonChoiceData.json()['stats'][0]['base_stat']
        # self.pokemonAttack = self.pokemonChoiceData.json()['stats'][1]['base_stat']
        # self.pokemonDefense = self.pokemonChoiceData.json()['stats'][2]['base_stat']
        # self.pokemonSpecialAttack = self.pokemonChoiceData.json()['stats'][3]['base_stat']
        # self.pokemonSpecialDefense = self.pokemonChoiceData.json()['stats'][4]['base_stat']
        # self.pokemonSpeed = self.pokemonChoiceData.json()['stats'][5]['base_stat']
        # self.pokemonSpriteURL = self.pokemonChoiceData.json()['sprites']['front_shiny']
        # self.pokemonFirstType = self.pokemonChoiceData.json()['types'][0]['type']['name']
        # try:
        #     self.pokemonSecondType = self.pokemonChoiceData.json()['types'][1]['type']['name']
        # except IndexError:
        #     self.pokemonSecondType = None

    def printStats(self):
        """Print pokemon stats."""
        print(f"{self.pokemonName.capitalize()} stats:")
        print(f"Pokemon HP: {self.pokemonHp}")
        print(f"Pokemon Attack: {self.pokemonAttack}")
        print(f"Pokemon Defense: {self.pokemonDefense}")
        print(f"Pokemon Special Attack: {self.pokemonSpecialAttack}")
        print(f"Pokemon Special Defense: {self.pokemonSpecialDefense}")
        print(f"Pokemon Speed: {self.pokemonSpeed}")

    def takeDamage(self, damage):
        """Reduce pokemon hp by 'damage' amount."""
        self.pokemonHp -= damage
        print(f"{self.pokemonName.capitalize()} took {damage} damage.")

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


def calculateDamage(attackingPokemon, defendingPokemon, movePower=30):
    """Calculate damage between two pokemon."""
    pokemonLevel = 99
    randValue = random.randint(85, 100)
    atkDmg = ((((((2 * pokemonLevel) / 5) + 2) * movePower * (attackingPokemon.pokemonAttack / defendingPokemon.pokemonDefense) / 50) + 2) * (randValue/100))
    return round(atkDmg)


def text_generator(text):
    """Yield text one letter at a time."""
    tmp = ''
    for letter in text:
        tmp += letter
        if letter != ' ':
            yield tmp


class DynamicText(object):
    def __init__(self, font, text, pos, autoreset=False):
        self.done = False
        self.font = font
        self.text = text
        self._gen = text_generator(self.text)
        self.pos = pos
        self.autoreset = autoreset
        self.update()

    def reset(self):
        self._gen = text_generator(self.text)
        self.done = False
        self.update()

    def update(self):
        if not self.done:
            try:
                self.rendered = self.font.render(next(self._gen), True, DARK_BLUE)
            except StopIteration:
                self.done=True
                if self.autoreset:
                    self.reset()

    def draw(self, screen):
        screen.blit(self.rendered, self.pos)


# Setting up sprites
P1 = Player("dragonite", dragonite, PLAYER_LOCATION)
P2 = Player("salamence", salamence, ENEMY_LOCATION)

P1.printStats()
P2.printStats()

welcome_message = DynamicText(font_small, welcome_scroll_text, (450, 306))

# Creating sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(P2)

# Adding a new user event
HP_ZERO = pygame.USEREVENT + 1
pokemon_fainted_event = pygame.event.Event(HP_ZERO, message = "Pokemon fainted and is unable to battle.")

# Game loop
while True:
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()

        # if event.type == INC_SPEED:
        #     SPEED += 0.5
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            if 0 <= mouse[0] <= 120 and 0 <= mouse[1] <= 30:
                P2.takeDamage(50)
                P2.printStats()
        if event.type == HP_ZERO:
            DISPLAYSURF.fill(RED)
            print(event.message)
            time.sleep(2)
            pygame.quit()
            sys.exit()
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    # Display background
    DISPLAYSURF.blit(background, (0, 0))

    # Moves and re-draws all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        # entity.move()

    if P2.pokemonHp <= 0 or P1.pokemonHp <= 0:
        pygame.event.post(pokemon_fainted_event)

    if 0 <= mouse[0] <= 120 and 0 <= mouse[1] <= 30:
        pygame.draw.rect(DISPLAYSURF, LIGHT_BLUE, [0, 0, 130, 30])
    else:
        pygame.draw.rect(DISPLAYSURF, DARK_BLUE, [0, 0, 130, 30])
    DISPLAYSURF.blit(button_text, (6, 6))

    welcome_message.draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)
