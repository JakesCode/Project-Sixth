locations = [["The Porch", "An old, wooden porch lies before the entrance to the house.", {"key": ["A rusty old key.", False, [False, None]]}],
	
	["Hallway", "The hallway is laden with dust. Old paintings hang from the crumbling walls.", {"painting": ["An old painting. '07/10/1873' is written in the lower right corner.", True, [False, None]],

		"safe": ["A steel safe. It ain't coming open with brute force.", True, [True, ["NUM", ["7183", "REMOVE REPETITIONS"]]]]}],
	
	] # <- Final List Bracket (Needed)

# Items #
# [[PLACE NAME, PLACE DESCRIPTION, {ITEMS: [ITEM DESCRIPTION: STATIC(TRUE) OR NOT STATIC(FALSE), SPECIAL [YES(TRUE) OR NO(FALSE), TYPE(OR JUST 'NONE' IF IT SAYS FALSE BEFOREHAND)]]}]]


import os

position = 0
inventory = {}

def displayStats(position):
	print(locations[position][0])
	print(locations[position][1])

def parseUse(item, location, Object):
	go = False
	if item.lower() == "key" and location == "The Porch" and (Object.lower() in ["door", "the door"]):
		go = True
		del inventory[item]
		print("")
	else:
		print("Nothing happened. Are you sure you're thinking straight?")

	return go

def parseSpecial(details):
	if details[0] == "NUM":
		correct = False
		# Number Puzzle #
		print("There's a number lock on this.")
		print("A piece of paper is stuck to the wall beside it.")
		print("")
		print("'" + details[1][1] + "'")
		print("")
		guess = int(input("Please enter your guess > "))

		if guess == details[1][0]:
			correct = True
		else:
			print("...nothing happens.")

		return correct


def prompt(position):
	print("")
	user = input("Enter a command, or type 'help' > ")
	print("")
	user.lower()

	itemKeys = list(locations[position][2].keys())

	if user == "look":
		if len(itemKeys) > 0:
			print("")
			print("Looking around, you see the following items: ")
			for x in range(0, len(itemKeys)):
				print("	" + itemKeys[x].title())
				print("	 " + locations[position][2][itemKeys[x]][0] + "\n")
		elif len(itemKeys) == 0:
			print("There's nothing at this location....")

	elif user[:7] == "inspect":
		if locations[position][2][user[8:]][2][0]:
			correct = parseSpecial((locations[position][2][user[8:]][2][1]))
		else:
			print("	 " + locations[position][2][user[8:]][0])

	elif user[:4] == "take":
		if user[5:] in itemKeys and not(locations[position][2][user[5:]][1]): # if the item you're trying to take is at the location and it's not a static item then take it
			print("Took the " + user[5:] + ".")
			inventory[user[5:]] = locations[position][2][user[5:]]
			del locations[position][2][user[5:]]
		elif len(user) == 4:
			print("Tell me what to take.")
			print("e.g. take item")

		try:
			if locations[position][2][user[5:]][1] and not(locations[position][2][user[5:]][2][0]):
				print("You can't pick that up. It won't budge!")
		except KeyError:
			if not(user[5:] in itemKeys):
				print("That item's not here....")	

	elif user == "help":
		print("PROJECT-SIXTH")
		print("")
		print("The aim of PROJECT-SIXTH is to advance from one room to the next. It might be as simple as walking through the door, others will require the finding of small object")
		print("")
		print("Items in brackets show the syntax with which the command must be used.")
		print("An x is specified by you, the player, when using the command.")
		print("")
		print("look - look around for items")
		print("take (take x) - take an item")
		print("use (take x) - use an item")

	elif user[:4] == "move":
		if user[5:] == "left":
			position -= 1
		elif user[5:] == "right":
			position += 1

	elif user[:3] == "use":
		itemToUse = user[4:]
		if itemToUse in list(inventory.keys()):
			toUseOn = input("On what? > ")
			go = parseUse(itemToUse, (locations[position][0]), toUseOn)
			if go:
				position += 1
				print("Moved forward.")
		else:
			print("You don't have that item.")

	elif user == "items":
		itemKeys = list(inventory.keys())
		if len(itemKeys) > 0:
			for x in range(0, len(itemKeys)):
				print("	" + itemKeys[x].title())
		else:
			print("You haven't got anything yet!")

	else:
		print("Eh?")

	input("\nPlease press any key....")

	return user, position


os.system("title PROJECT-SIXTH - A Puzzle Game by Jake Stringer")
while 1<2:
	os.system("cls")
	displayStats(position)
	user, position = prompt(position)

input("")