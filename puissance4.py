# -*- coding: utf-8 -*-
'''	IMPORTATIONS	'''

try:
	import discord
	from discord.ext import commands

except Exception as e:
	raise e

'''	LOGIC PART	'''

#- bot

bot = commands.Bot(command_prefix = "/p4", description="Puissance 4")

@bot.event
async def on_ready():
	print("Bot is ready, no issue detected")

# @bot.command()
# async def test(ctx):

# 	def verif(mess, user):
# 		print(user)
# 		return True

# 	#msg = await ctx.send("```┌────┬────┬────┬────┬────┬────┬────┐\n│   │   │   │   │   │   │   │\n├───┼───┼───┼───┼───┼───┼───┤\n│   │   │   │   │   │   │   │\n├───┼───┼───┼───┼───┼───┼───┤\n│   │   │   │   │   │   │   │\n├───┼───┼───┼───┼───┼───┼───┤\n│   │   │   │   │   │   │   │\n├───┼───┼───┼───┼───┼───┼───┤\n│   │   │   │   │   │   │   │\n├───┼───┼───┼───┼───┼───┼───┤\n│   │   │   │   │   │   │   │\n└───┴───┴───┴───┴───┴───┴───┘```")
# 	msg = await ctx.send("un\ntest")
# 	await msg.add_reaction('1️⃣')
# 	choice = await bot.wait_for("reaction_add", timeout=60)
# 	print(choice)

@bot.command()
async def battle(context):
	await context.send("En attente d'un autre joueur : (Entrer /p4 acceptBattle pour accepter le défi) :")
	player1 = context.message.author

	# check if:
	# 	-message came from different user
	# 	-message content = command
	# 	-message from same channel
		
	def check(message):
		return message.author != context.message.author and context.message.channel == message.channel and message.content == "/p4 acceptBattle"

	# check if:
	# 	-reaction from user turn
	# 	-good reaction

	def check_reaction(reaction, user):
		return message.id == reaction.message.id and user == game.turn and (reaction in game.get_possible_moves())

	# await bot.wait_for("message", timeout=10, check = check)
	player2_message = await bot.wait_for("message", timeout=60, check = check)
	player2 = player2_message.author

	print(f"DEBUG INFO : \r {player1} \n {player2}")

	await context.send("battle between {0} and {1} has started !".format(player1, player2))

	game = Game(player1, player2)

	# the game :
	# 	- send current grid + reactions
	# 	- wait for player to react
	# 	- add a token on the right column
	# 	- check if player win
	# 	if yes :
	# 		- say winner and stop
	# 	else :
	# 		- check possible moves and back to top


	def check_answer(message):
		print(message.author)
		return message.author == game.player_turn() and message.content in game.define_valid_inputs()

	# show the empty grid + add reactions
	grid = await context.send(f'Au tour de {game.player_turn} de jouer :```la grid```**Vos Choix : {game.define_valid_inputs()}**')

	while True:

		player_choice = await bot.wait_for("message", timeout=60, check=check_answer)
		game.update_grid()
		if game.check_if_player_win():
			break
		game.new_turn()
		await context.send(f'Au tour de {game.player_turn} de jouer :```la grid```**Vos Choix : {game.define_valid_inputs()}**')

#- game class


class Game:

	def __init__(self, player1, player2):
		
		# grid 7*6
		self.player1 = player1
		self.player2 = player2

		self.player_turn = self.player1

		self.grid_width = 7
		self.grid_height = 6

		# tokens places by column  
		self.tokens = {
			0: [' ', ' ', ' ', ' ', ' ', ' '],
			1: [' ', ' ', ' ', ' ', ' ', ' '],
			2: [' ', ' ', ' ', ' ', ' ', ' '],
			3: [' ', ' ', ' ', ' ', ' ', ' '],
			4: [' ', ' ', ' ', ' ', ' ', ' '],
			5: [' ', ' ', ' ', ' ', ' ', ' '],
			6: [' ', ' ', ' ', ' ', ' ', ' ']
		}

		self.row_0 = []
		self.row_1 = []
		self.row_2 = []
		self.row_3 = []
		self.row_4 = []
		self.row_5 = []

		self.update_grid()

	# the game
	# def game(self):

	# 	while True:
	# 		player_choice = self.player_turn()
	# 		self.place_new_token(turn, player_choice)
	# 		print(self.tokens)
	# 		print(self.row_0 + self.row_1 + self.row_2 + self.row_3 + self.row_4 + self.row_5)
	# 		self.update_grid()
	# 		turn = self.new_turn(turn)
	# 		self.show_grid()


	# define which player has to play next
	def new_turn(self, turn):

		if self.player_turn == self.player1:
			return self.player2

		else:
			return self.player1

	
	# search if columns are full	
	def define_valid_inputs(self):

		valid_columns = []

		for key, values in self.tokens.items():
			
			# check if last place in column isn't filled
			if values[-1] == ' ':
				valid_columns.append(str(key))

		return valid_columns


	# give the player instructions and check if it inputs is valid	
	# def player_turn(self):
		
	# 	print("Choisissez une colone (vous pouvez abandonner en entrant 'SURENDER'): ")
	# 	print("reactions: {} : ".format(', '.join(self.define_valid_inputs())))
	# 	player_choice = input('\t> ')
	# 	return player_choice

	# place player token
	def place_new_token(self, turn, player_input):

		# define which token to place:
		# 	- if player1 -> yellow circle
		# 	- if player2 -> red circle
			
		if self.player_turn == self.player1:
			turn == '🟡'
		else:
			turn == '🔴'

		for n, item in enumerate(self.tokens[int(player_input)]):
		 	if item == ' ':
		 		self.tokens[int(player_input)][n] = turn
		 		break


	def update_grid(self):

		row_0 = []
		row_1 = []
		row_2 = []
		row_3 = []
		row_4 = []
		row_5 = []

		# define the content of each row
		for key, value in self.tokens.items():
			row_0.append(value[0])
			row_1.append(value[1])
			row_2.append(value[2])
			row_3.append(value[3])
			row_4.append(value[4])
			row_5.append(value[5])

		self.row_0 = row_0
		self.row_1 = row_1
		self.row_2 = row_2
		self.row_3 = row_3
		self.row_4 = row_4
		self.row_5 = row_5


	#check if 4 tokens are inline
	def check_if_player_win(self):
	
		#  check for rows
		pass
		
	def check_rows(self):

		# row 1
		
		# check if the center is surronded by 2 different tokens
		if self.row_1[3] == self.row[2] or self.row_1[3] == self.row[4]:
			pass
		

		# row 2
		# row 3
		# row 4
		# row 5
		# row 6

		return False

	# return a grid :
	# 	- create a list
	# 	- add each rows to list
	# 	- return '\n' joined list 
	
	def show_grid(self):

		grid = []

		# print first line
		grid.append('┌───┬───┬───┬───┬───┬───┬───┐')

		# print rows
		grid.append('│ {} │ {} │ {} │ {} │ {} │ {} │ {} │'.format(self.row_5[0],self.row_5[1],self.row_5[2],self.row_5[3],self.row_5[4],self.row_5[5],self.row_5[6])) # row 6 : last row
		grid.append('├───┼───┼───┼───┼───┼───┼───┤') # row separator
		grid.append('│ {} │ {} │ {} │ {} │ {} │ {} │ {} │'.format(self.row_4[0],self.row_4[1],self.row_4[2],self.row_4[3],self.row_4[4],self.row_4[5],self.row_4[6])) # row 5
		grid.append('├───┼───┼───┼───┼───┼───┼───┤')
		grid.append('│ {} │ {} │ {} │ {} │ {} │ {} │ {} │'.format(self.row_3[0],self.row_3[1],self.row_3[2],self.row_3[3],self.row_3[4],self.row_3[5],self.row_3[6])) # row 4
		grid.append('├───┼───┼───┼───┼───┼───┼───┤')
		grid.append('│ {} │ {} │ {} │ {} │ {} │ {} │ {} │'.format(self.row_2[0],self.row_2[1],self.row_2[2],self.row_2[3],self.row_2[4],self.row_2[5],self.row_2[6])) # row 3
		grid.append('├───┼───┼───┼───┼───┼───┼───┤')
		grid.append('│ {} │ {} │ {} │ {} │ {} │ {} │ {} │'.format(self.row_1[0],self.row_1[1],self.row_1[2],self.row_1[3],self.row_1[4],self.row_1[5],self.row_1[6])) # row 2
		grid.append('├───┼───┼───┼───┼───┼───┼───┤')
		grid.append('│ {} │ {} │ {} │ {} │ {} │ {} │ {} │'.format(self.row_0[0],self.row_0[1],self.row_0[2],self.row_0[3],self.row_0[4],self.row_0[5],self.row_0[6])) # row 1 : first row

		# print last line
		grid.append('└───┴───┴───┴───┴───┴───┴───┘')

		return '\n'.join(grid)

'''	START PROGRAM'''	
bot.run("")




'''
	TOKENS :

	:yellow_circle: 🟡
	:red_circle: 🔴

	REACTIONS :
	
	:one: 1️⃣
	:two: 2️⃣
	:three: 3️⃣
	:four: 4️⃣
	:five: 5️⃣
	:six: 6️⃣
	:seven: 7️⃣

	GRID :

	┌┐─│└┘├┤┼┬┴

	┌───┬───┬───┬───┬───┬───┬───┐
6	│   │   │   │   │   │   │   │
	├───┼───┼───┼───┼───┼───┼───┤
5	│   │   │   │   │   │   │   │
	├───┼───┼───┼───┼───┼───┼───┤
4	│   │   │   │   │   │   │   │
	├───┼───┼───┼───┼───┼───┼───┤
3	│   │   │   │   │   │   │   │
	├───┼───┼───┼───┼───┼───┼───┤
2	│   │   │   │   │   │   │   │
	├───┼───┼───┼───┼───┼───┼───┤
1	│   │   │   │   │   │   │   │
	└───┴───┴───┴───┴───┴───┴───┘
	  1   2   3   4   5   6   7
'''
