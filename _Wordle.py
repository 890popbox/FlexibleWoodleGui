#Just incase we need to import some tkinter guis
from tkinter import *
import random
from functools import partial
class Wordle(object):
	def __init__(self, root):
		self.root = root
		#Default word and tries (EDIT HERE)
		self.minWordLength = 3
		self.maxWordLength = 15
		self.minAttemptLength = 3
		self.maxAttemptLength = 6
		self.wordLength = 5
		self.attemptLength = 6
		#Display
		self.selectionFrames = []
		self.visualFrames = []
		self.keyboardFrames = []
		#WordGuess
		self.wordFrames = []
		self.chosenWord = ""
		#Zero is the start
		self.currentGuess = 0
		self.currentIndex = 0

	#Clear all frames really fast and resetGame
	def clearFrames(self):
		for x in self.keyboardFrames:
			print(x)
			x.destroy()
		for a in self.wordFrames:
			for b in a:
				b.destroy()
		for x in self.visualFrames:
			x.destroy()
		for x in self.selectionFrames:
			x.destroy()
		#Clear the arrays
		self.keyboardFrames.clear()
		self.wordFrames.clear()
		self.visualFrames.clear()
		self.selectionFrames.clear()
		self.resetGame()
		del self



	#Verify the sizes, and set up the game
	def verifyGame(self, size, tries):
		#Default on somewhere between
		if size > self.maxWordLength:
			size = 15
		elif size < self.minWordLength:
			size = 3

		#If it is a real number
		if (size >= self.minWordLength) and (size <= self.maxWordLength):
			self.wordLength = size

		#Default on somewhere between
		if tries > self.maxAttemptLength:
			tries = 10
		elif tries < self.minAttemptLength:
			tries = 5

		#If it is a real number
		if (tries >= self.minAttemptLength) and (tries <= self.maxAttemptLength):
			self.attemptLength = tries

		#Find all words that match the size given
		word_ls = []
		fo = open("words.txt", "r+")
		for word in fo:
			if len(word) == size+1:
				word_ls.append(word.strip('\n'))

		#Randomly choose the word
		random_ind = random.randint(0, len(word_ls)-1)
		self.chosenWord = word_ls[random_ind]
		self.wordSize = len(self.chosenWord)
		#We may be including an \n by mistake

	#Start game
	def playWordle(self, size, tries):
		main = self.root
		# Remove the selection menu only, start game
		for x in self.selectionFrames:
			x.destroy()

		# Verify the game before starting it
		self.verifyGame(size, tries)

		#Testing purposes
		print(self.chosenWord)
		print(self.wordSize)

		#Go the length of the word, and add 6 words to the table
		for n in range(0, self.attemptLength):
			word = []
			for i in range(0, self.wordSize):
				wordLabel = Label(main, text=" ", relief = 'solid')
				wordLabel.config(font = "monospace 12 bold", fg = 'white', bg= 'grey', height = 2,  width = 4)
				wordLabel.place(x = (50*i)+50, y=(50*n)+50)
				word.append(wordLabel)
			self.wordFrames.append(word)

		# Keyboard
		keyboardLabels = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
				  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '<'],
				  ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'Enter']]

		for n, r in enumerate(keyboardLabels):
			for i, c in enumerate(r):
				label = Button(main, relief='solid', font = "monospace 16 bold", fg = 'white', bg= 'grey', text=str(c), command= partial(self.pickCharacter, c))
				label.place(x = (50*i)+100, y=(40*n)+350)
				self.keyboardFrames.append(label)

	def pickCharacter(self, ch):

		#If enter, analyze word
		if(ch=="Enter"):
			if(self.currentIndex ==self.wordSize):
				self.analyzeWord(self.wordFrames[self.currentGuess])
			return

		#More console testing
		print(ch, self.currentIndex, self.currentGuess)
		print(self.wordLength, self.attemptLength)
		if(ch=="<" and self.currentIndex == 0):
			return #No change
		elif(ch=="<"):
			#Word blank now
			self.currentIndex -= 1
			self.wordFrames[self.currentGuess][self.currentIndex].config(text=" ")
		else:
			# Error checking
			if (self.currentIndex >= self.wordSize):
				return
			#CurrentLetter move up and add it
			print(self.wordFrames[self.currentGuess])
			self.wordFrames[self.currentGuess][self.currentIndex].config(text=ch)
			self.currentIndex += 1



	def analyzeWord(self, word):
		main = self.root
		#The guess has already been checked to be valid before entering this function call
		white_list = []
		winnerCheck = 0

		#Alphabet array
		ar = [0] * 26

		#What characters are in the chosen word?
		for ch in self.chosenWord:
			key = ord(ch) % 26
			ar[key] += 1

		#Check if the character is in the word at the same position
		for word_ind, c in enumerate(word):
			ch = c.cget("text")
			#Change that positions colour to green and remove the letter from the array
			if self.chosenWord[word_ind] == ch:
				winnerCheck += 1
				c.config(bg='green')
				key = ord(ch) % 26
				ar[key] -= 1
				white_list.append(ch)

		# Check if the character is in the word at any position
		for word_ind, c in enumerate(word):
			ch = c.cget("text")
			key = ord(ch) % 26
			if ar[key] > 0:
				c.config(bg='yellow')
				white_list.append(ch)

		#Check for a winner or not
		if(winnerCheck==self.wordSize):
			print("Winner")
			winnerLabel = Label(main, text="Good job! That was the correct word", relief='solid', font = "monospace 24 bold")
			winnerLabel.place(x=200, y=400)
			self.visualFrames.append(winnerLabel)
			self.resetGame()
		elif(self.currentGuess== self.attemptLength-1):
			loserLabel = Label(main, text="Nice try, the word was {0}".format(self.chosenWord), relief='solid', font = "monospace 24 bold")
			loserLabel.place(x=200, y=400)
			self.visualFrames.append(loserLabel)
			self.resetGame()
		else:
			#Black out characters not on the white list
			for c in word:
				if (c.cget("text") not in white_list):
					for q in self.keyboardFrames:
						if (c.cget("text") == q.cget("text")):
							q.config(bg='black')
				else:
					pass

			#Reset where we are
			self.currentGuess += 1
			self.currentIndex = 0
			pass

	#Reset the Wordle Game
	def resetGame(self):
		self.chosenWord = ""
		self.wordSize = 3
		self.currentGuess = 0
		self.currentIndex = 0


	#Create this class
	def createWordle(self):
		main = self.root

		sortFrame = Frame(main,width=900,height=450,bg='#aaaaaa')
		sortFrame.place(x=0,y=0)
		self.visualFrames.append(sortFrame)

		#Naming it this because later will allow custom input, how long should the word be?
		wordLabel = Label(main, text="How long do you want the word to be? [{0}-{1}]".format(self.minWordLength, self.maxWordLength), font='arial 24')
		wordLabel.grid(row = 0, column = 0)
		word_length = Entry(main, relief='solid', fg='#000000', bg='#ffffff')
		word_length.grid(row=1, column=0)

		self.selectionFrames.append(wordLabel)
		self.selectionFrames.append(word_length)

		#How many tries.. [3-6]
		triesLabel = Label(main, text="How many tries would you like to solve the word? [{0}-{1}]".format(self.minAttemptLength, self.maxAttemptLength), font='arial 24')
		triesLabel.grid(row = 2, column = 0)
		tries_length = Entry(main, relief='solid', fg='#000000', bg='#ffffff')
		tries_length.grid(row=3, column=0)

		self.selectionFrames.append(triesLabel)
		self.selectionFrames.append(tries_length)

		enterButton = Button(main, text="Enter", command=lambda: self.playWordle(int(word_length.get()), int(tries_length.get())))
		enterButton.grid(row = 4, column = 0)
		self.selectionFrames.append(enterButton)