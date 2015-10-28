locations = [["The Porch", "An old, wooden porch lies before the entrance to the house.", {"key": ["A rusty old key.", False, [False, None]]}],
	
	["Hallway", "The hallway is laden with dust. Old paintings hang from the crumbling walls.", {"painting": ["An old painting. '17/11/1873' is written in the lower right corner.", True, [False, None]],

		"safe": ["A steel safe. It ain't coming open with brute force.", True, [True, ["NUM", ["1783", "LEFT TO RIGHT | REMOVE REPETITIONS"]]]]}],
	
	] # <- Final List Bracket (Needed)

# Items #
# [[PLACE NAME, PLACE DESCRIPTION, {ITEMS: [ITEM DESCRIPTION: STATIC(TRUE) OR NOT STATIC(FALSE), SPECIAL [YES(TRUE) OR NO(FALSE), TYPE(OR JUST 'NONE' IF IT SAYS FALSE BEFOREHAND)]]}]]


import os
from tkinter import *
from PIL import Image as PILImage
import re

position = 0
inventory = {}

import glob

for infn in glob.glob("icons/*.png"):
    if "-small" in infn: continue 
    outfn = infn.replace(".png", "-small.png")
    im = PILImage.open(infn)
    im.thumbnail((100, 100))
    im.save(outfn)

class GameWindow:

	def __init__(self, master):
		self.position = 0
		frame = Frame(master)
		frame.config(width=200, height=80)
		frame.pack()

		iconName = ("icons\\brutal-helm-small.png")
		icon = PhotoImage(file=iconName)
		self.l = Label(master, image=icon)
		self.l.photo = icon
		self.l.pack()

		title = Label(master, text="PROJECT-SIXTH", bg="#A0CFE6", font=("Courier New", 31)).pack(expand=1, fill=BOTH)

		self.locationTitleVar = StringVar()
		self.locationTitleVar.set(locations[self.position][0])
		locationTitle = Label(master, textvariable=self.locationTitleVar).pack()
		self.locationDescriptionVar = StringVar()
		self.locationDescriptionVar.set(locations[self.position][1])
		locationDescription = Label(master, textvariable=self.locationDescriptionVar).pack()

		self.mainWindow(master)


	def mainWindow(self, master):
		l = Label(master, text="Choose an option....", font=("Courier New", 20)).pack()
		lookButton = Button(master, text="Look", font=("Courier New", 8), command=lambda:self.look(master)).pack()
		takeButton = Button(master, text="Take", font=("Courier New", 8), command=lambda:self.take(master)).pack()
		useButton = Button(master, text="Use", font=("Courier New", 8), command=lambda:self.use(master, self.position)).pack()

	def look(self, master):
		lookWindow = Toplevel()
		lookWindow.title("Look")

		itemKeys = list(locations[self.position][2].keys())

		if len(itemKeys) > 0:
			l = Label(lookWindow, text="Looking around, you see the following items....\n").pack()
			for x in range(0, len(itemKeys)):
				icon = PhotoImage(file=("icons\\" + itemKeys[x] + "-small.png"))
				l = Label(lookWindow, image=icon)
				l.photo = icon
				l.pack()
				l = Label(lookWindow, text=("" + itemKeys[x].title())).pack()
				l = Label(lookWindow, text=("	" + locations[self.position][2][itemKeys[x]][0] + "\n")).pack()
		else:
			l = Label(lookWindow, text="There's nothing at this location....").pack()
			icon = PhotoImage(file=("icons\\cancel-small.png"))
			l = Label(lookWindow, image=icon)
			l.photo = icon
			l.pack()

	def take(self, master):
		takeWindow = Toplevel()
		takeWindow.title("Take")
		takeWindow.geometry("230x300")

		self.itemKeys = list(locations[self.position][2].keys())

		l = Label(takeWindow, text="Take what?").pack()

		v = StringVar(takeWindow)
		v.set(self.itemKeys[0])
		m = OptionMenu(takeWindow, v, self.itemKeys)
		m.pack()
		
		b = Button(takeWindow, text="Take", command=lambda:self.getStuff(m, v, takeWindow)).pack()

		self.l2 = StringVar()
		l3 = Label(takeWindow, textvariable=self.l2).pack()

		look = Button(takeWindow, text="See what items are around you", command=lambda:self.look(master)).pack()

		iconName = ("icons\\bowman-small.png")

		icon = PhotoImage(file=iconName)
		self.l = Label(takeWindow, image=icon)
		self.l.photo = icon
		self.l.pack()

		blankLabel = Label(takeWindow, text="\n").pack()


	def updateImage(self, toChangeTo, window):
		self.l.destroy()
		iconName = ("icons\\" + toChangeTo + "-small.png")
		icon = PhotoImage(file=iconName)
		self.l = Label(window, image=icon)
		self.l.photo = icon
		self.l.pack()


	def getStuff(self, m, v, takeWindow):
		self.itemToGet = v.get()
		self.itemToGet2 = self.itemToGet.replace("[", "").replace("]", "").replace("'", "")
		print(self.itemToGet2)
		self.l2.set(self.itemToGet2)

		if self.itemToGet2 in self.itemKeys and not(locations[self.position][2][self.itemToGet2][1]): # if the item you're trying to take is at the location and it's not a static item then take it
			self.l2.set(("Took the " + self.itemToGet2 + "."))
			self.itemKeys = self.updateList(self.itemKeys)
			inventory[self.itemToGet2] = locations[self.position][2][self.itemToGet2]
			del locations[self.position][2][self.itemToGet2]
			self.updateImage(self.itemToGet2, takeWindow)

		try:
			if locations[self.position][2][self.itemToGet2][1] and not(locations[self.position][2][self.itemToGet2][2][0]):
				self.l2.set("You can't pick that up. It won't budge!")
		except KeyError:
			if not(self.itemToGet2 in self.itemKeys):
				print("That item's not here....")


	def updateList(self, itemKeys):
		self.itemKeys = list(locations[self.position][2].keys())
		return self.itemKeys


	def use(self, master, position):
		useWindow = Toplevel()
		useWindow.title("Use")
		self.invKeys = list(inventory.keys())


		if len(self.invKeys) > 0:
			iconName = ("icons\\bowman-small.png")
			icon = PhotoImage(file=iconName)
			self.l = Label(useWindow, image=icon)
			self.l.photo = icon
			self.l.pack()

			v = StringVar(useWindow)
			v.set(self.invKeys[0])
			l = Label(useWindow, text="Use an item....").pack()
			m = OptionMenu(useWindow, v, self.invKeys)
			m.pack()

			b = Button(useWindow, text="Use", command=lambda:self.useStuff(v.get(), useWindow, self.position)).pack()
		else:
			l = Label(useWindow, text="You don't have anything in your inventory....").pack()
			icon = PhotoImage(file=("icons\\cancel-small.png"))
			l = Label(useWindow, image=icon)
			l.photo = icon
			l.pack()


	def useStuff(self, thing, window, position):
		itemToUse = thing.replace("[", "").replace("]", "").replace("'", "")
		if itemToUse in list(inventory.keys()):
			l = Label(window, text="On what?\n").pack()
			e = Entry(window)
			e.pack()
			b = Button(window, text="Submit", command=lambda:self.checkUse(e.get(), itemToUse, self.position, window)).pack()
		else:
			l = Label(window, text="You don't have that item.").pack()

	def checkUse(self, e, itemToUse, position, window):
		go = parseUse(itemToUse, (locations[self.position][0]), e)
		if go:
			self.position += 1
			self.wellDone()
			window.destroy()

	def wellDone(self):
		moveWindow = Toplevel()
		moveWindow.title("Congratulations!")
		l = Label(moveWindow, text="The pathway to the next room is open.\nWell done!").pack()
		iconName = ("icons\\one-eyed-small.png")
		icon = PhotoImage(file=iconName)
		self.l = Label(moveWindow, image=icon)
		self.l.photo = icon
		self.l.pack()
		b = Button(moveWindow, text="-> -> Go -> ->", command=lambda:moveWindow.destroy()).pack()





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

root = Tk()
game = GameWindow(root)
root.mainloop()

os.system("title PROJECT-SIXTH - A Puzzle Game by Jake Stringer")
while 1<2:
	os.system("cls")
	displayStats(position)
	user, position = prompt(position)

input("")