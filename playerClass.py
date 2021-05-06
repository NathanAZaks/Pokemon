"""Holds player class and functions to edit player class."""
import pygame
import requests
import io
import colorsys
import globalVariables as gv

pygame.init()

# Setting up fonts
FONT_LARGE = pygame.font.Font("./Assets/Pokemon GB.ttf", 60)
FONT_MEDIUM = pygame.font.Font("./Assets/Pokemon GB.ttf", 20)
FONT_SMALL = pygame.font.Font("./Assets/Pokemon GB.ttf", 12)


def scale_hp(base_value, IV, EV, level):
    """
    Use to scale hp value from base to level 99.

    HP = (((2 * Base + IV + (EV / 4)) * Level) / 100) + Level + 10

    Returns int of scaled up hp stat value.
    """
    scaled_value = (
        (((2 * base_value + IV + (EV / 4)) * level) / 100)
        + level + 10)
    return int(scaled_value)


def scale_stat(base_value, IV, EV, level):
    """
    Use to scale other stat values from base to level 99.

    Stat = ((((2 * Base + IV + (EV / 4)) * Level) / 100) + 5) * Nature
    Ignoring nature for now

    Returns int of scaled up stat value.
    """
    # TODO: Add nature calculations
    scaled_value = ((((2 * base_value + IV + (EV / 4)) * level) / 100) + 5)
    return int(scaled_value)


class Player(pygame.sprite.Sprite):
    """Create a pokemon container."""

    def __init__(self, pokemon, location, screen):
        """Create an instance of the class."""
        super().__init__()

        self.screen = screen

        self.request = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon}/")

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

        self.ev = 256
        self.iv = 32
        self.pokemon_hp_percentage = 1.0

        if location == gv.BASE_PLAYER_LOCATION:
            self.pokemon_base_location = gv.BASE_PLAYER_LOCATION
        else:
            self.pokemon_base_location = gv.BASE_ENEMY_LOCATION

        self.image = requests.get(self.pokemon_sprite_url)
        self.image = io.BytesIO(self.image.content)
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale(self.image, gv.SPRITE_SIZE)
        self.surf = pygame.Surface(gv.SPRITE_SIZE)
        self.rect = self.image.get_rect(topleft=self.pokemon_location)

        self.pokemon_bg_hp_bar_location = [
            self.pokemon_base_location[0],
            self.pokemon_base_location[1]-5,
            150,
            10]

        self.is_moving = False

        if self.pokemon_location == gv.BASE_PLAYER_LOCATION:
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
        self.name_and_hp = (
            f"{self.pokemon_name} : {self.pokemon_hp}/{self.pokemon_max_hp}")

        # HSV to RGB calculation for Green to Red hp bar color
        self.h, self.s, self.v = 0.33*self.pokemon_hp_percentage, 1, 1
        self.r, self.g, self.b = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        self.hp_bar_color = [int(255*self.r), int(255*self.g), int(255*self.b)]

    def update(self, delta=[0, 0]):
        """Update location of sprite."""
        self.rect.move_ip(delta)  # delta is (x, y)
        self.pokemon_location[0] += delta[0]
        self.pokemon_location[1] += delta[1]

    def display(self):
        """Redraw sprite and hp bars on the screen."""
        self.screen.blit(self.image, self.pokemon_location)

        pygame.draw.rect(  # Background HP Bar
            surface=self.screen,
            color=gv.BLACK,
            rect=self.pokemon_bg_hp_bar_location,
            border_radius=5)
        pygame.draw.rect(  # Colored HP Bar
            surface=self.screen,
            color=self.hp_bar_color,
            rect=self.pokemon_hp_bar_location,
            border_radius=5)

        self.name_and_hp_surf = FONT_SMALL.render(
            self.name_and_hp,
            True,
            gv.BLACK)
        self.name_and_hp_size = FONT_SMALL.size(self.name_and_hp)
        self.screen.blit(
            self.name_and_hp_surf,
            (self.pokemon_base_location[0] + 75 - self.name_and_hp_size[0]/2,
                self.pokemon_base_location[1]-20))
