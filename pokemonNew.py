import requests
import json
import random
import time
import collections
import os
from PIL import Image


class pokemon:
    """Class container for pokemon."""

    pokemonStats = []

    def __init__(self):
        """Init function."""
        pass

    def choose_pokemon(self):
        """Receives user input of a pokemon name or "random" to set pokemon."""
        pickPokemon = 1
        while pickPokemon == 1:
            pokemonChoice = str.lower(input("What pokemon do you choose? (Enter a Pokemon name or 'random'): "))
            if pokemonChoice == "random":
                randomNumber = str(random.randint(1, 898))
                pokemonChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{randomNumber}/")
            else:
                pokemonChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonChoice}/")
            # TODO: Add more specific Error Messages
            if pokemonChoiceData.status_code != 200:
                print(f"Sorry, {pokemonChoice} is not a recognized pokemon. Check your spelling, maybe?")
            else:
                userPokemon = pokemonChoiceData.json()['name']
                pickPokemon = 0

        for statNum in range(0, 6):
            self.pokemonStats.append(pokemonChoiceData.json()['stats'][statNum]['base_stat'])

        print(f"You chose {userPokemon}")

    def printStats(self):
        """Print pokemon stats."""
        for statNum in range(0, 6):
            print("stat: " + str(self.pokemonStats[statNum]))
        print("\n")

    def takeDamage(self, damage):
        """Reduce pokemon hp by 'damage' amount."""
        self.pokemonStats[5] -= damage


def calculateDamage(attackingPokemon, defendingPokemon):
    """Calculate damage between two pokemon."""
    pokemonLevel = 99
    movePower = 60
    randValue = random.randint(85, 100)
    atkDmg = ((((((2 * pokemonLevel) / 5) + 2) * movePower * (attackingPokemon.pokemonStats[1] / defendingPokemon.pokemonStats[2]) / 50) + 2) * (randValue/100))
    return atkDmg


# def scrollingText(string):
#     for char in string:
#         print(char, end='')
#         flush.flush()
#         time.sleep(.05)


def main():
    """Use the main function to run code."""
    self = pokemon()
    self.choose_pokemon()
    self.printStats()

    oppo = pokemon()
    oppo.choose_pokemon()
    oppo.printStats()


if __name__ == "__main__":
    main()

# Next Steps:
# - Implement actual battling
# - Find applicable moves for each pokemon
# # - Grab move power from json
# - Set up introduction

# img = Image.open(requests.get('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/123.png', stream = True).raw)

# Order of Stats: hp, attack, defense, special-attack, special-defense, speed
