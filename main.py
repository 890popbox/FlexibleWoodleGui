# Author: Chris Antes (notmoon#0001)
# Date: 03/29/2022
# Description: Simple Wordle but a bit more Flexible

'''
Hope this is easy to read and edit <3
'''

#Import tkinter to create GUI
from tkinter import *
from tkinter import messagebox
import time

#Import the menu and the game
from _Menu import Menu, menuItem
from _Wordle import Wordle

#Global visualFrames
visualFrames = []
def clearVisualFrames():
    for x in visualFrames:
        x.destroy()

#Create functions for the menu to run
def playMoondle():
	Wordle.createWordle()

# Help page..
def helpMe():
    print('notmoon was here')
    readmeFRAME = Frame(main, width=900, height=450, bg='#aaaaaa')
    readmeFRAME.place(x=0, y=0)
    visualFrames.append(readmeFRAME)
    info1 = Label(main, text='You will be able to select how long the word is and how many tries\n'
                             + 'Well sort of (MIN-MAX), [3 - 15 length] [3 - 6 tries]\n'
                             + '[DEFAULT WORD LENGTH: 5, DEFAULT AMOUNT OF TRIES: 6]\n\n'
                             + 'If after entering the word the character is Grey, it is not in the wood\n'
                             + 'If after entering the word the character is Yellow, it is in the wood but in the incorrect position\n'
                             + 'If after entering the word the character is Green, it is in the wood but in the incorrect position\n'
                  , fg='#aaaaaa', bg='#2c2f33', font='arial 12 bold')
    info1.place(x=100, y=200)
    visualFrames.append(info1)

# notmoon readme
def readMe():
    print('notmoon was here')
    readmeFRAME = Frame(main, width=900, height=450, bg='#aaaaaa')
    readmeFRAME.place(x=0, y=0)
    visualFrames.append(readmeFRAME)
    readThis1 = Label(main, text='Simple Flexible Wordle GUI by Chris(notmoon#0001)\n'
                                 + 'You will be able to select how long the word is and how many tries\n'
                                 + 'Thanks to github user dwyl for a list of over 466k English words\n'
                      , fg='#aaaaaa', bg='#2c2f33', font='arial 12 bold')
    readThis1.grid(row=0, column=0, pady=10, padx=10)
    visualFrames.append(readThis1)


#Create the GUI
main = Tk()
main.iconbitmap(r'C:\Users\chris\PycharmProjects\FlexibleWoodleGui\icon.ico')

#Need full map, create calculator right in main and todolist
Wordle = Wordle(main)
main.title('Flexible Simple Wordle Gui')
main.geometry('900x600')
main.config(bg = '#aaaaaa')
#Create the array of items
myMenu = Menu()
myMenu.addMenu(playMoondle, "Play the game")
myMenu.addMenu(helpMe, "Help Me")
myMenu.addMenu(readMe, "Read me")

#Now create them all under list number names
for i,x in enumerate(myMenu.returnMenu()):
	Label(main,text = x.description,font= 'arial 24').grid(row=0+i,column=0)
	Button(main,width=15,height=2, text='Click', bg='light blue', command=x.func).grid(row = 0+i, column = 0+1, padx = 5)
#Creating the reset button
btnRestart = Button(main,text='Go to main', command=lambda:[clearVisualFrames(), Wordle.clearFrames()])
btnRestart.config(width=30)
btnRestart.place(x=350,y=500)
#Hold time
date = Label(main, text= time.asctime(time.localtime(time.time())))
date.config(fg = '#000000', font= 'verdana 12')
date.place(x=0,y=500)
#Self updating time every second (Maybe change to minute?)
def tick():
	time2 = time.strftime('%b %d %Y %H:%M:%S')
	date.config(text=time2)
	date.after(1000, tick)
#Run the main Loop..
tick()
main.mainloop()
#Hmm..
#Cantes(Moon)