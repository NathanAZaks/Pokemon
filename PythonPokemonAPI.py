import json, requests, random, time, collections

from PIL import Image
from sys import stdout as flush

def dmgCalc(level, power, attack, defense):

	# ATTACKS' DAMAGES ARE CALCULATED

	randValue = random.randint(85, 100)
	
	atkDmg = ((((((2 * level) / 5) + 2) * power * (attack / defense) / 50) + 2) * (randValue/100)) #* mods
	return atkDmg

def modCalc(targets, weather, badge, critical, random, stab, type, burn):
	#damage modification calculations
	mods = targets * weather * critical * random * stab * types * burn

def scrollingText(string):
	for char in string:
		print(char, end='')
		flush.flush()
		time.sleep(.05)

def introSequence():

	# OPEN POKÉMON IMGAGE

	# pokeImg = Image.open("pokeImg.png")

	# pokeImg.show()

	# INTRO TO GAME AND WORLD OF POKÉMON

	intro1 = "Hey you look like that new kid in town. Hi, Welcome to Pallet Town. I'm Nathan, I'll be your guide. What was your name again? "
	
	# print("Oh right, %s! Professor Oak told us you would be coming." % trainerName)
	# print("Well, welcome to the world of Pokemon. This world is inhabited by creatures called Pokémon! For some people, pokémon are pets. Others use them for fights. Professor Oak studies pokémon as a profession. Myself... I just want to study them.")
	# print("My guess is that you already knew that and you came to Pallet Town to start your journey to becoming a Pokémon Master. Well let's get started.")
	# print("Let me show you how to battle!")

	scrollingText(intro1)
	trainerName = input("").capitalize()
	intro2 = "Oh right, %s! Professor Oak told us you would be coming. Well, welcome to the world of Pokemon. This world is inhabited by creatures called Pokémon! For some people, pokémon are pets. Others use them for fights. Professor Oak studies pokémon as a profession. Myself... I just want to be friends. My guess is that you already knew that and you came to Pallet Town to start your journey to becoming a Pokémon Master. Well let's get started. Let me show you how to battle!" % trainerName
	scrollingText(intro2)

def fightSequence():

	movePower = 45

	validUserPokemon = 0
	validOppoPokemon = 0

	while(validUserPokemon == 0):
		userPokemon = str.lower(input("\nWhat pokemon do you want? (Enter a pokemon name or 'random'): "))

		if userPokemon == "random":
			userPokemon = random.randint(1, 808)
			userPokemonData = requests.get('https://pokeapi.co/api/v2/pokemon/%s/' % str(userPokemon))
			userPokemon = userPokemonData.json()['forms'][0]['name']

			validUserPokemon = 1

			### Add error message about no internet connection

		else:
			userPokemonData = requests.get('https://pokeapi.co/api/v2/pokemon/%s/' % str(userPokemon))
			### Add more specific Error Messages

			if userPokemonData.status_code != 200:
				print ("Sorry, " + userPokemon + " is not a recognized pokemon. Check your spelling, maybe?")
				validUserPokemon = 0

			else:
				userPokemon = userPokemonData.json()['forms'][0]['name']
				validUserPokemon = 1


	print ("You chose: %s" % (userPokemonData.json()['forms'][0]['name'].capitalize()))

	userPokeStats = collections.OrderedDict()

	for statNum in range(0, 6):
		userPokeStats['%s' % (userPokemonData.json()['stats'][statNum]['stat']['name'])] = (int(userPokemonData.json()['stats'][statNum]['base_stat']))
	
	userPokeStats = list(userPokeStats.items())

	### PICK OPPONENT POKEMON, GET STATS

	while(validOppoPokemon == 0):
		oppoPokemon = str.lower(input("What pokemon do you want to battle? (Enter a pokemon name or 'random'): "))

		if oppoPokemon == "random":
			oppoPokemon = random.randint(1, 808)
			oppoPokemonData = requests.get('https://pokeapi.co/api/v2/pokemon/%s/' % str(oppoPokemon))
			oppoPokemon = oppoPokemonData.json()['forms'][0]['name']
			validOppoPokemon = 1

			### Add error message about no internet connenction

		else: 
			oppoPokemonData = requests.get('https://pokeapi.co/api/v2/pokemon/%s/' % str(oppoPokemon))

			if oppoPokemonData.status_code != 200:
				print ("Sorry, " + str(oppoPokemon) + " is not a recognized pokemon. Check your spelling, maybe?")
				validOppoPokemon = 0
			else:	
				oppoPokemon = oppoPokemonData.json()['forms'][0]['name']
				validOppoPokemon = 1


	print ("\nYou will be fighting against: %s" % (oppoPokemonData.json()['forms'][0]['name'].capitalize()))

	oppoPokeStats = collections.OrderedDict()

	for statNum in range(0, 6):
		oppoPokeStats['%s' % (oppoPokemonData.json()['stats'][statNum]['stat']['name'])] = (int(oppoPokemonData.json()['stats'][statNum]['base_stat']))

	oppoPokeStats = list(oppoPokeStats.items())
	#print(json.dumps(oppoPokeStats))

	# print(userPokeStats,oppoPokeStats)

	# PICK USER POKEMON, GET STATS

	userPokeLevel = 99
	oppoPokeLevel = 99

	userPokeHp = 10 + userPokeLevel + userPokeStats[5][1]
	oppoPokeHp = 10 + oppoPokeLevel + oppoPokeStats[5][1]

	userPokeAtk = userPokeStats[4][1]
	oppoPokeAtk = userPokeStats[4][1]

	userPokeDef = userPokeStats[3][1]
	oppoPokeDef = userPokeStats[3][1]

	userPokeSpAtk = userPokeStats[2][1]
	oppoPokeSpAtk = userPokeStats[2][1]

	userPokeSpDef = userPokeStats[1][1]
	oppoPokeSpDef = userPokeStats[1][1]

	userPokeSpd = userPokeStats[0][1]
	oppoPokeSpd = oppoPokeStats[0][1]

	# SEE WHO ATTACKS FIRST

	print ("So you picked:", userPokemon.capitalize(), "and you will be fighting against:", oppoPokemon.capitalize())

	print("\nLET THE BATTLE BEGIN\n")

	print("User Pokemon HP:", userPokeHp)
	print("Opponent Pokemon HP:", oppoPokeHp)

	if userPokeSpd > oppoPokeSpd:
		print ("\nYou're faster, you go first!")
		whoAttacks = 0

	elif userPokeSpd < oppoPokeSpd:
		print ("\nYou're slower, opponent goes first!")
		whoAttacks = 1

	else:
		coinToss = random.randint(0,1)
		if coinToss == 0:
			print ("\nYou won the coin toss, you go first!")
			whoAttacks = 0
		else:
			print ("\nYou lost the coin toss, opponent goes first!")
			whoAttacks = 1

	#BEGIN BATTLE SEQUENCE

	while userPokeHp > 0 and oppoPokeHp > 0:
		# ADD THE STUFF ABOUT ACTUALLY LIKE FIGHTING AND STUFF HERE
		# WHILE BOTH POKEMON ARE ABOVE HP = 0, ALLOW TO USE ATTACKS

		if whoAttacks == 0:
			# User Pokemon attack
			print("\nWhat would you like to do?")
			action = str.lower(input("You can attack or run: \n"))

			if action == "attack":
				atkDmg = round(dmgCalc(userPokeLevel, movePower, userPokeAtk, oppoPokeDef))

				print("\nYour %s attacked the opposing %s!" % (userPokemon,oppoPokemon))
				oppoPokeHp = oppoPokeHp - atkDmg

				print("User Pokemon HP:", userPokeHp)
				print("Opponent Pokemon HP:", oppoPokeHp)	
				
				whoAttacks = 1 # Set opponent Pokemon to attack 

				time.sleep(1)

			elif action == "run":
				print("\nYou have successfully run away.")
				return

			else:
				print(action, "is not a valid option.")

		elif whoAttacks == 1:
			# Opponent Pokemon attack
			atkDmg = round(dmgCalc(oppoPokeLevel, movePower, oppoPokeAtk, userPokeDef))

			print("\nThe opposing %s attacked your %s!" % (oppoPokemon,userPokemon))
			userPokeHp = userPokeHp - atkDmg

			print("User Pokemon HP:", userPokeHp)
			print("Opponent Pokemon HP:", oppoPokeHp)

			whoAttacks = 0

			time.sleep(1)

		if userPokeHp < 0:
			print("Your", userPokemon, "has fainted and is unable to battle.", oppoPokemon, "wins!")

		if oppoPokeHp < 0:
			print("The opponent", oppoPokemon, "has fainted is unable to battle.", "Your", userPokemon, "wins!")
	
	return

introSequence()
fightSequence()
# modCalc()
