import requests, json, random, time, collections, os
from PIL import Image

class pokemon:
	def __init__(self, name, stats):
		self.name = name
		self.stats = stats

# PICK USER POKEMON
def choose_user_pokemon():
	validUserPokemon = 1
	while validUserPokemon == 1:
		userChoice = str.lower(input("What pokemon do you choose? (Enter a pokemon name or 'random'): "))
		if userChoice == "random":
			randomNumber = str(random.randint(1, 898))
			userChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{randomNumber}/")
		else:
			userChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{userChoice}/")
			### Add more specific Error Messages
			if userChoiceData.status_code != 200:
				print (f"Sorry, {userChoice} is not a recognized pokemon. Check your spelling, maybe?")
				validUserPokemon = 0
			else:
				userPokemon = userPokemonData.json()['name']
				validUserPokemon = 1

	userStats={}
	for statNum in range(0, 5):
		userStats[req.json()['stats'][statNum]['stat']['name']] = userChoiceData.json()['stats'][statNum]['base_stat']
	return userPokemon = pokemon(userChoiceData.json()['name'], userStats)

def choose_oppo_pokemon():
	validOppoPokemon = 1
	while validOppoPokemon == 1:
		oppoChoice = str.lower(input("What pokemon do you choose? (Enter a pokemon name or 'random'): "))
		if oppoChoice == "random":
			randomNumber = str(random.randint(1, 898))
			oppoChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{randomNumber}/")
		else:
			oppoChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{oppoChoice}/")
			### Add more specific Error Messages
			if oppoChoiceData.status_code != 200:
				print (f"Sorry, {oppoChoice} is not a recognized pokemon. Check your spelling or your internet connection, maybe?")
				validOppoPokemon = 0
			else:
				oppoPokemon = userOppoData.json()['name']
				validOppoPokemon = 1

	oppoStats={}
	for statNum in range(0, 5):
		oppoStats[req.json()['stats'][statNum]['stat']['name']] = oppoChoiceData.json()['stats'][statNum]['base_stat']
	return oppoPokemon = pokemon(oppoChoiceData.json()['name'], oppoStats)

def do_damage(attackingPokemon, defendingPokemon):
	randValue = random.randint(85, 100)
	atkDmg = ((((((2 * 99) / 5) + 2) * 60 * (attackingPokemon.stats["attack"] / defendingPokemon.stats["defense"]) / 50) + 2) * (randValue/100)) # 99 is Pokemon Level, 60 is Move Power
	defendingPokemon.stats['hp'] -= atkDmg

def scrollingText(string):
	for char in string:
		print(char, end='')
		flush.flush()
		time.sleep(.05)

# Next Steps:
# - Implement actual battling
# - Find applicable moves for each pokemon
# - - Grab move power from json
# - Set up introduction
# - 

# img = Image.open(requests.get('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/123.png', stream = True).raw)
# img


# Order of Stats: hp, attack, defense, special-attack, special-defense, speed
