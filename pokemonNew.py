import requests
import json
import random
import time
import collections
import os
from PIL import Image


class pokemon:
    """Class container for pokemon."""

    pokemonHp = None
    pokemonAttack = None
    pokemonDefense = None
    pokemonSpecialAttack = None
    pokemonSpecialDefense = None
    pokemonSpeed = None
    pokemonType = None
    pokemonName = None
    pokemonSpriteURL = None

    def __init__(self):
        """Init function."""
        # FIXME: Idk if I even need this constructor here or not or what
        pass

    def choose_pokemon(self):
        """Receives user input of a pokemon name or "random" to set pokemon."""
        while True:
            scrollingText("What pokemon do you choose? (Enter a Pokemon name or 'random'): ")
            pokemonChoice = str.lower(input(""))
            if pokemonChoice == "random":
                randomNumber = str(random.randint(1, 898))
                pokemonChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{randomNumber}/")
            else:
                pokemonChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonChoice}/")
            # TODO: Add more specific Error Messages
            if pokemonChoiceData.status_code != 200:
                scrollingText(f"Sorry, {pokemonChoice.capitalize()} is not a recognized pokemon. Check your spelling, maybe?")
            else:
                break

        self.pokemonName = pokemonChoiceData.json()['name']
        self.pokemonHp = pokemonChoiceData.json()['stats'][0]['base_stat']
        self.pokemonAttack = pokemonChoiceData.json()['stats'][1]['base_stat']
        self.pokemonDefense = pokemonChoiceData.json()['stats'][2]['base_stat']
        self.pokemonSpecialAttack = pokemonChoiceData.json()['stats'][3]['base_stat']
        self.pokemonSpecialDefense = pokemonChoiceData.json()['stats'][4]['base_stat']
        self.pokemonSpeed = pokemonChoiceData.json()['stats'][5]['base_stat']
        self.pokemonSpriteURL = pokemonChoiceData.json()['sprites']['front_shiny']


        try:
            self.pokemonType = (
                pokemonChoiceData.json()['types'][0]['type']['name'],
                pokemonChoiceData.json()['types'][1]['type']['name']
                )
        except IndexError:
            self.pokemonType = pokemonChoiceData.json()['types'][0]['type']['name']

        scrollingText(f"{self.pokemonName.capitalize()} was chosen!")

    def printStats(self):
        """Print pokemon stats."""
        scrollingText(f"{self.pokemonName.capitalize()} stats:")
        scrollingText(f"Pokemon HP: {self.pokemonHp}")
        scrollingText(f"Pokemon Attack: {self.pokemonAttack}")
        scrollingText(f"Pokemon Defense: {self.pokemonDefense}")
        scrollingText(f"Pokemon Special Attack: {self.pokemonSpecialAttack}")
        scrollingText(f"Pokemon Special Defense: {self.pokemonSpecialDefense}")
        scrollingText(f"Pokemon Speed: {self.pokemonSpeed}")

    def takeDamage(self, damage):
        """Reduce pokemon hp by 'damage' amount."""
        self.pokemonHp -= damage
        scrollingText(f"{self.pokemonName.capitalize()} took {damage} damage.")

    def showSprite(self):
        """Show pokemon sprite."""
        sprite = Image.open(requests.get(self.pokemonSpriteURL, stream=True).raw)
        sprite.show()


def calculateDamage(attackingPokemon, defendingPokemon, movePower=30):
    """Calculate damage between two pokemon."""
    pokemonLevel = 99
    randValue = random.randint(85, 100)
    atkDmg = ((((((2 * pokemonLevel) / 5) + 2) * movePower * (attackingPokemon.pokemonAttack / defendingPokemon.pokemonDefense) / 50) + 2) * (randValue/100))
    return round(atkDmg)


def scrollingText(string):
    """Use to print text one character at a time."""
    if True:  # TODO: Remove when done testing
        print(string)
        return
    for char in string:
        print(char, end='', flush=True)
        time.sleep(.05)


def whoIsAttacking(userPokemon, oppoPokemon):
    """Use to determine which pokemon will attack first."""
    if userPokemon.pokemonSpeed > oppoPokemon.pokemonSpeed:
        attacking = "user"
    elif userPokemon.pokemonSpeed < oppoPokemon.pokemonSpeed:
        attacking = "oppo"
    else:
        if random.randint(0, 1) == 1:
            attacking = "user"
        else:
            attacking = "oppo"
    return attacking


def runSimulation():
    """Run the simulation."""
    user = pokemon()
    user.choose_pokemon()
    user.printStats()

    oppo = pokemon()
    oppo.choose_pokemon()
    oppo.printStats()

    attacking = whoIsAttacking(user, oppo)

    input("Do you want to attack? ")

    while user.pokemonHp > 0 and oppo.pokemonHp > 0:
        # FIXME: This isn't working
        scrollingText(f"Attacking: {attacking.capitalize()}")
        if attacking == "user":
            oppo.takeDamage(calculateDamage(user, oppo))
            oppo.printStats()
            attacking = "oppo"
        else:
            user.takeDamage(calculateDamage(oppo, user))
            user.printStats()
            attacking = "user"

    if user.pokemonHp > 0:
        print("You won!")
    else:
        print("You lost!")


def main():
    """Use the main function to run code."""
    runSimulation()


if __name__ == "__main__":
    main()

# Next Steps:
# - Implement actual battling
# - Find applicable moves for each pokemon
# # - Grab move power from json
# - Set up introduction

# img = Image.open(requests.get('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/123.png', stream = True).raw)

# Order of Stats: hp, attack, defense, special-attack, special-defense, speed
