locations = [["The Porch", "An old, wooden porch lies before the entrance to the house.", {"key": ["A rusty old key.", True]}, ],
	
	] # <- Final List Bracket (Needed)

# Items #
# [[PLACE NAME, PLACE DESCRIPTION, {ITEMS: [ITEM DESCRIPTION: STATIC(TRUE) OR NOT STATIC(FALSE)]}]]


import os

position = 0
inventory = {}

def displayStats(position):
	print(locations[position][0])
	print(locations[position][1])



def prompt(position):
	print("")
	user = input("Enter a command, or type 'help' > ")
	print("")
	user.lower()

	itemKeys = list(locations[position][2].keys())

	if user == "items":
		for x in range(0, len(itemKeys)):
			print("	" + itemKeys[x].title())
			print("	 " + locations[position][2][itemKeys[x]][0])

		if len(itemKeys) == 0:
			print("There's nothing at this location....")

	elif user[:4] == "take":
		if user[5:] in itemKeys and locations[position][2][user[5:]][1]:
			print("Took the " + user[5:] + ".")
			inventory[user[5:]] = locations[position][2][user[5:]]
			del locations[position][2][user[5:]]
		elif len(user) == 4:
			print("Tell me what to take.")
			print("e.g. take item")
		else:
			print("That item's not here.")

	elif user == "help":
		print("PROJECT-SIXTH")
		print("Items in brackets show the syntax with which the command must be used.")
		print("An x is specified by you, the player, when using the command.")
		print("")
		print("items - view items")
		print("take (take x) - take an item")

	elif user[:4] == "move":
		if user[5:] == "left":
			position -= 1
		elif user[5:] == "right":
			position += 1


	return user, position


while 1<2:
	os.system("cls")
	displayStats(position)
	user, position = prompt(position)

	input("")

input("")