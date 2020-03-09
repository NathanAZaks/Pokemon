import json, requests, random, time, collections

from PIL import Image

class pokemon:

	def dmgCalc(self, level, power, attack, defense):

		# ATTACKS' DAMAGES ARE CALCULATED

		randValue = random.randint(85, 100)
		
		atkDmg = ((((((2 * level) / 5) + 2) * power * (attack / defense) / 50) + 2) * (randValue/100)) #* mods
		return atkDmg

	def modCalc(self, targets, weather, badge, critical, random, stab, type, burn):
		#damage modification calculations
		mods = targets * weather * critical * random * stab * types * burn

	def introSequence(self):

		# OPEN POKÉMON IMGAGE

		# pokeImg = Image.open("pokeImg.png")

		# pokeImg.show()

		# INTRO TO GAME AND WORLD OF POKÉMON

		print("Hi, Welcome to Pallet Town. I'm Nathan, I'll be your guide.")
		# time.sleep(2)
		print("Hey you look like that new kid in town.")
		trainerName = input("What was your name again? ").capitalize()
		# time.sleep(1)
		print("Oh right, %s! Professor Oak told us you would be coming." % trainerName)
		# time.sleep(2)
		print("Well, welcome to the world of Pokemon. This world is inhabited by creatures called Pokémon! For some people, pokémon are pets. Others use them for fights. Professor Oak studies pokémon as a profession. Myself... I just want to be homies with all my bois.")
		# time.sleep(8)
		print("My guess is that you already knew that and you came to Pallet Town to start your journey to becoming a Pokémon Master. Well let's get started.")
		print("Let me show you how to battle!")

	def pickPokemon(self):

		self.userPokemon = str.lower(input("What pokemon do you want? (Enter a pokemon name or 'random'): "))

		if self.userPokemon == "random":
			self.userPokemon = random.randint(1, 808)
			self.userPokemonData = requests.get('https://pokeapi.co/api/v2/pokemon/%s/' % str(self.userPokemon))
			self.userPokemon = self.userPokemonData.json()['forms'][0]['name']

			### Add error message about no internet connection

		else:
			self.userPokemonData = requests.get('https://pokeapi.co/api/v2/pokemon/%s/' % str(self.userPokemon))
			self.userPokemonData.json()['forms'][0]['name']
			### Add more specific Error Messages

			if self.userPokemonData.status_code != 200:
				print ("Sorry, " + self.userPokemon + " is not a recognized pokemon. Check your spelling, maybe?")
				return

		print ("You chose: %s" % (self.userPokemonData.json()['forms'][0]['name'].capitalize()))

		self.userPokeStats = collections.OrderedDict()

		for statNum in range(0, 6):
			self.userPokeStats['%s' % (self.userPokemonData.json()['stats'][statNum]['stat']['name'])] = (int(self.userPokemonData.json()['stats'][statNum]['base_stat']))
		
		self.userPokeStats = list(self.userPokeStats.items())

		### PICK OPPONENT POKEMON, GET STATS

		self.oppoPokemon = str.lower(input("What pokemon do you want to battle? (Enter a pokemon name or 'random'): "))


		if self.oppoPokemon == "random":
			self.oppoPokemon = random.randint(1, 808)
			self.oppoPokemonData = requests.get('https://pokeapi.co/api/v2/pokemon/%s/' % str(self.oppoPokemon))
			self.oppoPokemon = self.oppoPokemonData.json()['forms'][0]['name']

			### Add error message about no internet connenction

		else: 
			self.oppoPokemonData = requests.get('https://pokeapi.co/api/v2/pokemon/%s/' % str(self.oppoPokemon))
			self.oppoPokemonData.json()['forms'][0]['name']
			if self.oppoPokemonData.status_code != 200:
				print ("Sorry, " + str(self.userPokemon) + " is not a recognized pokemon. Check your spelling, maybe?")
				return


		print ("\nYou will be fighting against: %s" % (self.oppoPokemonData.json()['forms'][0]['name'].capitalize()))

		self.oppoPokeStats = collections.OrderedDict()

		for statNum in range(0, 6):
			self.oppoPokeStats['%s' % (self.oppoPokemonData.json()['stats'][statNum]['stat']['name'])] = (int(self.oppoPokemonData.json()['stats'][statNum]['base_stat']))

		self.oppoPokeStats = list(self.oppoPokeStats.items())
		#print(json.dumps(oppoPokeStats))
		#-----------------------------------
		# print(userPokeStats,oppoPokeStats)

		return self.userPokeStats,self.oppoPokeStats

	def fightSequence(self):

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

		if userPokeSpd > oppoPokeSpd:
			print ("You're faster, you go first!")
			whoAttacks = 0

		elif userPokeSpd < oppoPokeSpd:
			print ("You're slower, opponent goes first!")
			whoAttacks = 1

		else:
			coinToss = random.randint(0,1)
			if coinToss == 0:
				print ("You won the coin toss, you go first!")
				whoAttacks = 0
			else:
				print ("You lost the coin toss, opponent goes first!")
				whoAttacks = 1

		#BEGIN BATTLE SEQUENCE

		print("\nUser Pokemon HP:", userPokeHp)
		print("Opponent Pokemon HP:", oppoPokeHp)

		while userPokeHp > 0 and oppoPokeHp > 0:
			# ADD THE STUFF ABOUT ACTUALLY LIKE FIGHTING AND STUFF HERE
			# WHILE BOTH POKEMON ARE ABOVE HP = 0, ALLOW TO USE ATTACKS
			
			print("What would you like to do?")
			action = str.lower(input("You can attack or run: "))

			if action == "attack":
				if whoAttacks == 0:
					#User is attacked first
					atkDmg = round(dmgCalc(oppoPokeLevel, 45, oppoPokeAtk, userPokeDef))
					
					print("\nYour", userPokemon, "attacked the opposing", oppoPokemon)
					print("Attack damage:", atkDmg)

					userPokeHp = userPokeHp - atkDmg
					
					print("User Pokemon HP:", userPokeHp)
					print("Opponent Pokemon HP:", oppoPokeHp)

					#Attack opponent
					atkDmg = round(dmgCalc(userPokeLevel, 45, userPokeAtk, oppoPokeDef))
					
					print("\nThe opposing", oppoPokemon, "attacked your", userPokemon)
					print("Attack damage:", atkDmg)

					oppoPokeHp = oppoPokeHp - atkDmg

					print("User Pokemon HP:", userPokeHp)
					print("Opponent Pokemon HP:", oppoPokeHp)
				else:
					#Attack opponent first
					atkDmg = round(dmgCalc(userPokeLevel, 45, userPokeAtk, oppoPokeDef))
					
					print("\nYour", oppoPokemon, "attacked the opposing", userPokemon)
					print("Attack damage:", atkDmg)

					oppoPokeHp = oppoPokeHp - atkDmg

					print("User Pokemon HP:", userPokeHp)
					print("Opponent Pokemon HP:", oppoPokeHp)

					#User is attacked
					atkDmg = round(dmgCalc(oppoPokeLevel, 45, oppoPokeAtk, userPokeDef))
					
					print("\nYour", userPokemon, "attacked the opposing", oppoPokemon)
					print("Attack damage:", atkDmg)

					userPokeHp = userPokeHp - atkDmg
					
					print("User Pokemon HP:", userPokeHp)
					print("Opponent Pokemon HP:", oppoPokeHp)

			elif action == "run":
				print("You successfully escaped from the battle.")
				return

			else:
				print(action, "is not a valid option.")

			if userPokeHp < 0:
				print("Your", userPokemon, "has fainted and is unable to battle.")

			if oppoPokeHp < 0:
				print("The opponent", oppoPokemon, "has fainted is unable to battle.")
		
		return

p = pokemon()

# p.introSequence()
p.pickPokemon()
print(p.pickPokemon(userPokeStats))
# p.fightSequence()
