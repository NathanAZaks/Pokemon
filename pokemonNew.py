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
    pokemonName = ""

    def __init__(self):
        """Init function."""
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
                scrollingText(f"Sorry, {pokemonChoice} is not a recognized pokemon. Check your spelling, maybe?")
            else:
                self.pokemonName = pokemonChoiceData.json()['name']
                break

        for statNum in range(0, 6):
            self.pokemonStats.append(pokemonChoiceData.json()['stats'][statNum]['base_stat'])

        scrollingText(f"You chose {self.pokemonName}")

    def printStats(self):
        """Print pokemon stats."""
        for statNum in range(0, 6):
            print("stat: " + str(self.pokemonStats[statNum]))
        print("\n")

    def takeDamage(self, damage):
        """Reduce pokemon hp by 'damage' amount."""
        self.pokemonStats[0] -= damage
        print(f"{self.pokemonName} took {damage} damage.")


def calculateDamage(attackingPokemon, defendingPokemon, movePower = 60):
    """Calculate damage between two pokemon."""
    pokemonLevel = 99
    randValue = random.randint(85, 100)
    atkDmg = ((((((2 * pokemonLevel) / 5) + 2) * movePower * (attackingPokemon.pokemonStats[1] / defendingPokemon.pokemonStats[2]) / 50) + 2) * (randValue/100))
    return round(atkDmg)


def scrollingText(string):
    if True: # TODO: Remove when done testing
        print(string)
        return
    for char in string:
        print(char, end='', flush = True)
        time.sleep(.05)
    # print("\n")

def whoIsAttacking(userPokemon, oppoPokemon):
    if userPokemon.pokemonStats[5] > oppoPokemon.pokemonStats[5]:
        attacking = "user"
    elif userPokemon.pokemonStats[5] < oppoPokemon.pokemonStats[5]:
        attacking = "oppo"
    else:
        if random.randint(0,1) == 1:
            attacking = "user"
        else:
            attacking = "oppo"
    return attacking


def main():
    """Use the main function to run code."""
    user = pokemon()
    user.choose_pokemon()
    user.printStats()

    oppo = pokemon()
    oppo.choose_pokemon()
    oppo.printStats()

    attacking = whoIsAttacking(user, oppo)
    print("Attacking: " + attacking)

    while user.pokemonStats[0] > 0 and oppo.pokemonStats[0] > 0: # FIXME: This isn't working
        if attacking == "user":
            oppo.takeDamage(calculateDamage(user, oppo))
            oppo.printStats()
            print("user attacking")
            attacking == "oppo"
        else:
            user.takeDamage(calculateDamage(oppo, user))
            user.printStats()
            print("oppo attacking")
            attacking == "user"

    if user.pokemonStats[0] > 0:
        print("You won!")
    else:
        print("You lost!")


if __name__ == "__main__":
    main()

""# Next Steps:
# - Implement actual battling
# - Find applicable moves for each pokemon
# # - Grab move power from json
# - Set up introduction

# img = Image.open(requests.get('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/123.png', stream = True).raw)

# Order of Stats: hp, attack, defense, special-attack, special-defense, speed
