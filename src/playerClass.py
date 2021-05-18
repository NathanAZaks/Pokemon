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
    scaled_value = ((((2 * base_value + IV + (EV / 4)) * level) / 100) + 5)
    return int(scaled_value)


class Player(pygame.sprite.Sprite):
    """Create a pokemon container."""

    def __init__(self, pokemon, location, screen):
        """
        Create an instance of the class.

        Accepts a list from a request, base location, display surface.
        """
        # initialize sprite class
        super().__init__()

        # Display surface
        self.screen = screen

        # Setting up pokemon name, stats, types
        self.request = pokemon.json()
        self.pokemon_name = self.request['name'].capitalize()
        self.pokemon_location = location
        self.pokemon_level = 99
        self.pokemon_base_hp = self.request['stats'][0]['base_stat']
        self.pokemon_base_attack = self.request['stats'][1]['base_stat']
        self.pokemon_base_defense = self.request['stats'][2]['base_stat']
        self.pokemon_base_sp_attack = self.request['stats'][3]['base_stat']
        self.pokemon_base_sp_defense = self.request['stats'][4]['base_stat']
        self.pokemon_base_speed = self.request['stats'][5]['base_stat']
        self.pokemon_first_type = self.request['types'][0]['type']['name']
        try:
            self.pokemon_second_type = self.request['types'][1]['type']['name']
        except IndexError:
            self.pokemon_second_type = None

        # Pokemon's EV's and IV's, using max values
        self.ev = 256
        self.iv = 32

        self.pokemon_hp_percentage = 1.0

        # If pokemon is player -> sprite is back side, set base location
        if location == gv.BASE_PLAYER_LOCATION:
            self.pokemon_base_location = gv.BASE_PLAYER_LOCATION
            self.front_back = "back"
        else:
            self.pokemon_base_location = gv.BASE_ENEMY_LOCATION
            self.front_back = "front"

        # Set up sprite image
        self.pokemon_sprite_url = (
            self.request['sprites'][f"{self.front_back}_shiny"])
        self.image = requests.get(self.pokemon_sprite_url)
        self.image = io.BytesIO(self.image.content)
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale(self.image, gv.SPRITE_SIZE)
        self.surf = pygame.Surface(gv.SPRITE_SIZE)
        self.rect = self.image.get_rect(topleft=self.pokemon_location)

        # Set up hp bar location
        self.pokemon_bg_hp_bar_location = [
            self.pokemon_base_location[0],
            self.pokemon_base_location[1]-5,
            150,
            10]

        # True if pokemon is attacking
        self.is_moving = False

        # Initialize what direction pokemon will move in for attack
        if self.pokemon_location == gv.BASE_PLAYER_LOCATION:
            self.direction = "right"
        else:
            self.direction = "left"

        # Scale stats from base to level 99 stats
        self.scale_stats_level_99()

        # Update hp percentage, hp bar color and location
        self.update_hp_bar()

    def print_stats(self):
        """Print pokemon stats to terminal."""
        print(f"{self.pokemon_name} stats:")
        print(f"Pokemon Primary Type:       {self.pokemon_first_type}")
        print(f"Pokemon Secondary Type:     {self.pokemon_second_type}")
        print(f"Pokemon HP:                 {self.pokemon_hp}")
        print(f"Pokemon Attack:             {self.pokemon_attack}")
        print(f"Pokemon Defense:            {self.pokemon_defense}")
        print(f"Pokemon Special Attack:     {self.pokemon_sp_attack}")
        print(f"Pokemon Special Defense:    {self.pokemon_sp_defense}")
        print(f"Pokemon Speed:              {self.pokemon_speed}")

    def scale_stats_level_99(self):
        """
        Update stats scaled to level 99 stats in-place.

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
        self.pokemon_sp_attack = scale_stat(
            self.pokemon_base_sp_attack,
            self.iv,
            self.ev,
            self.pokemon_level)
        self.pokemon_sp_defense = scale_stat(
            self.pokemon_base_sp_defense,
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

        # If pokemon fainted -> set hp 0
        if self.pokemon_hp_percentage < 0:
            self.pokemon_hp_percentage = 0
            self.pokemon_hp = 0

        # Update pokemon hp bar location, size
        self.pokemon_hp_bar_location = [
            self.pokemon_base_location[0],
            self.pokemon_base_location[1]-5,
            150*self.pokemon_hp_percentage,
            10]

        # String with pokemon name and hp to render on screen
        self.name_and_hp = (
            f"{self.pokemon_name} : {self.pokemon_hp}/{self.pokemon_max_hp}")

        # HSV to RGB calculation for Green to Red hp bar color
        self.h, self.s, self.v = 0.33*self.pokemon_hp_percentage, 1, 1
        self.r, self.g, self.b = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        self.hp_bar_color = [int(255*self.r), int(255*self.g), int(255*self.b)]

    def update(self, delta=[0, 0]):
        """Update location of sprite."""
        self.rect.move_ip(delta)
        self.pokemon_location[0] += delta[0]
        self.pokemon_location[1] += delta[1]

    def display(self):
        """Redraw sprite and hp bars on the screen."""
        # Draw sprite to screen
        self.screen.blit(self.image, self.pokemon_location)

        # Draw full length, black, background hp bar
        pygame.draw.rect(
            surface=self.screen,
            color=gv.BLACK,
            rect=self.pokemon_bg_hp_bar_location,
            border_radius=5)

        # Draw hp scaled color and size hp bar
        pygame.draw.rect(
            surface=self.screen,
            color=self.hp_bar_color,
            rect=self.pokemon_hp_bar_location,
            border_radius=5)

        # Render name and hp
        self.name_and_hp_surf = FONT_SMALL.render(
            self.name_and_hp,
            True,
            gv.BLACK)
        self.name_and_hp_size = FONT_SMALL.size(self.name_and_hp)

        # Draw name and hp to screen, centered above sprite
        self.screen.blit(
            self.name_and_hp_surf,
            (self.pokemon_base_location[0] + 75 - self.name_and_hp_size[0]/2,
                self.pokemon_base_location[1]-20))
