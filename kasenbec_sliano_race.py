#Kim Asenbeck and Simone Liano
#CS 111
#Final Project

from Tkinter import *
import time
import random

class RaceApp(Tk): 
    def __init__(self):
        Tk.__init__(self) #Initialize the class
        self.title('Race for a Space!') #Name the window
        self.grid() #Put a grid on the GUI
        self.createWidgets() #Prepare to create widgets
        
    def createWidgets(self):
        
        self.GIF_width = 500  # Width of GIF
        self.GIF_height = 525 # Height of GIF
        self.numRows = 4 #Need four rows
        self.numCols = 6 #six columns (one for each parking space)
        self.cellHeight = 100 #Each cell is 100 pixels high
        self.cellWidth = 450/6.0 #divided into six columns

        self.minsize(width=self.GIF_width, height=self.GIF_height) #determining size of GIF
        self.maxsize(width=self.GIF_width, height=self.GIF_height) #size of GIF

        self.blanks=[]#make a list of blank canvases so we can refer to them later
        # Create grid of blank widgets behind the background image
        for i in range(self.numRows): #for loop corresponding with num of rows
            self.blanks.append([])#append a list to the existing list
            for j in range(self.numCols): #nested loop for num of columns
                # Create blank canvas widgets
                self.blank = Canvas(self, width=self.cellWidth, height=self.cellHeight)
                self.blank.grid(row=i, column=j)#apply each of those to the grid.
                self.blanks[-1].append(self.blank) #append each blank canvas to the list.
                
        
        # Background image
        pic = PhotoImage(file='parkinglot.gif') #set the background image to the parking lot
        imageLabel = Label(self, image=pic) 
        imageLabel.pic = pic
        imageLabel.grid(row=1, column=0, columnspan=6, rowspan=3) #place parking lot in GUI
        #imageLabel.place(x=0, y=0, relwidth=1, relheight=1) 
        
        
        #Title Bar
        titleBar = Canvas(self, bg='red', height=100, width=500) #Create a red background for title
        titleBar.grid(row=0, columnspan=6)#title bar spans whole gui
        #Title 
        #Set the text for the title
        titleLabel = Label(self, text='RACE FOR A SPACE', font='Helvetica 40 bold', bg='red', fg='white')
        titleLabel.grid(row=0, columnspan=6) #Place the title bar on the gui
        
        #Status Bar                 
        statusBar = Canvas(self, bg='gray', height=50, width=500) #create a gray background for status bar
        statusBar.grid(row=4, column=0, columnspan=6) #place the canvas on gui
        #Status text
        self.text = StringVar() #The status needs to be mutable
        #Creating the actual text variable
        self.statusText = Label(self, fg='red', bg='gray', font='Helvetica 20 bold', textvariable=self.text)
        self.text.set('Welcome, player!') #Setting the initial text
        self.statusText.grid(row=4, column=0, columnspan=6) #placing the text on gui
        
        #The Car
        self.mainCar = Car(2, 0, 'E.gif') #Creating the initial car
        self.addCar(self.mainCar)#Invoke the add car function
        self.direction = 'E' #this variable will be updated to reflect direction of car
        self.carPosition = (2,0) #initial position of car
        self.bindArrowKeys()#bind the arrow keys to allow the car to move

        #Other Cars
        self.dictOfTopSlots = {(1,0):0, (1,1):0, (1,2):0, (1,3):0, (1,4):0, (1,5):0}  
        #this is a dictionary that is populated in order to determine which parking slots are full
        self.dictOfLowSlots = {(3,0):0, (3,1):0, (3,2):0, (3,3):0, (3,4):0, (3,5):0}
        #the keys are row/col pairs, and the values determine whether it's empty or full
        self.populateBoard()#invoke the function which places cars in lot. 
                    
        self.win=False
        
    def addCar(self, car): #this function adds cars to the canvas
        pic = PhotoImage(file=car.typeOfCar)#Add the appropriate type of car (direction/ if parked)
        imageLabel = Label(self, image=pic)
        imageLabel.pic = pic
        imageLabel.grid(row = car.row, column = car.column) #add the car to the given row/column
        
    def populateBoard(self): #This Function randomly determines how many parked cars there are
        for key in self.dictOfTopSlots: #there are two dictionaries, as seen above. This loop is top row
            randomNum = random.randint(0,1) #Randomly determine whether there is a car or not 
            self.dictOfTopSlots[key] = randomNum #Set this randomly determined number as key in dict
            #randomly set value to be 1 or 0 (using randint)
            if self.dictOfTopSlots[key] == 1: #If it's occupied, 
                parked1 = Car(key[0], key[1],'parked_car_up.gif') #then add an up-facing parked car
                self.addCar(parked1) #Invoke the add car function on this parked car
        for key in self.dictOfLowSlots: #this loop is for the bottom row 
            randomNum = random.randint(0,1)  #the lines below are the same as for the top row. 
            self.dictOfLowSlots[key] = randomNum
            if self.dictOfLowSlots[key] == 1:
                parked2 = Car(key[0], key[1],'parked_car_down.gif')  
                self.addCar(parked2)
       
        #Timer
        self.timer = 11  # 10 seconds display to start out
        self.timerLabel = Label(text=str(self.timer), font='Verdana 30 bold', bg='yellow')
        #Timer label updates with integers from self.timer, and the background is yellow. 
        self.timerLabel.grid(column=0, row=4) #add the timer to the gui
        self.updateTimer() #invoke the updateTimer function to decrement the time displayed. 
        #Red Bar
        redBar = Canvas(self, bg='red', height=50, width=500) #this bar is just a red background
        redBar.grid(row=5, column=0, columnspan=6) #add to gui
        #Instructions
        helpButton = Button(self, text= 'Help', command=self.onHelpButtonClick) 
        #Click this button, and a separate window will appear with instructions
        helpButton.grid(row=4, column=5)#add button to gui
        #New Game
        quitButton = Button(self, text= 'Quit', command=self.onQuitButtonClick) 
        quitButton.grid(row=5, column=2, columnspan=2) #Add the quit button to gui

    #Below, all functions within the race app class. 
    def addSign(self, sign, file1): 
        pic = PhotoImage(file=file1)#the specified image fileis a parameter
        imageLabel = Label(self, image=pic) 
        imageLabel.pic = pic
        imageLabel.grid(row=sign.row1, column=sign.column1, columnspan=sign.columnspan)
        #add the sign to canvas

    def updateTimer(self):
         if self.timer>0 and self.text.get != 'Congratulations! You win.':  # Stop when timer reaches 0
             self.timer -= 1  # Decrement timer by 1 second
             self.timerLabel.configure(text=str(self.timer)) #update the timer text
             self.after(1000, self.updateTimer)  # 1000 milliseconds is 1 sec.
         if self.timer==0: #When time runs out
             self.text.set("              Time is up! Game over.            ") 
             #The space above is for aesthetics, so that old text doesn't remain visible behind
             self.bell(0) # makes a sound  and blinks
             self.unbindArrowKeys()#unbind keys to stop player from moving car
             #Stop Sign
             if self.win == False: #Stop sign should only appear if you have lost the game
                 self.stopSign = Sign(2,2,2)#Add the stop sign 
                 self.addSign(self.stopSign, 'stop.gif')#invoke addSign function
    
    def onHelpButtonClick(self):
        window = Toplevel(self) #Inherit top level so that new window functions properly
        window.wm_title('Instructions') #Window title is instructions
        help = Label(window, text='\n\nRules of the game:\n Navigate your car to an empty\n parking space within 30 seconds\n using your arrow keys.\n Good luck!\n\nCreated by Kim Asenbeck \nand Simone Liano\n\n', font='Helvetica 20', bg='yellow')
        #Above is the text that appears in the window.
        help.grid()
        
    def onQuitButtonClick(self):
        self.destroy() #close window.
    
    def setCarLabel(self, theImage, row, col):
        self.blanks[row][col].destroy()#First, destroy whatever is currently in the given row and column
        self.blanks[row][col]=Label(self, image=theImage, width=(450/6.0), height=100)
        self.blanks[row][col].theImage=theImage #insert the appropriate image in the appropriate cell
        self.blanks[row][col].grid(row=row, column=col) #place in given row and column
        row = self.carPosition[0]#row refers to index zero of car position
        col = self.carPosition[1]#column refers to index one
        
    def bindArrowKeys(self):
        self.bind('<Left>', self.leftKey)  # When left arrow key is pressed, invoke self.leftKey method
        self.bind('<Right>', self.rightKey)  # When right arrow key is pressed, invoke self.rightKey method
        self.bind('<Up>', self.upKey)  # When up arrow key is pressed, invoke self.upKey method
        self.bind('<Down>', self.downKey)  # When down arrow key is pressed, invoke self.downKey method

    def unbindArrowKeys(self): #This function unbinds each of the arrow keys, or disables them
        self.unbind('<Left>') 
        self.unbind('<Right>')
        self.unbind('<Up>')
        self.unbind('<Down>')

    def leftKey(self, event):
        row = self.carPosition[0] #Row refers to index zero of carPosition
        col = self.carPosition[1] #column refers to index one of carPosition
        if col >= 1:#IF they are not hitting a wall
            self.blank = Canvas(self, width=self.cellWidth, height=self.cellHeight, bg='gray49')
            self.blank.config(highlightbackground='gray49')
            #Replace the position with a blank gray canvas
            self.blank.grid(row=row, column=col) #place that blank gray canvas in appropriate position
            if self.direction == 'N': #Change direction as needed
                self.direction = 'W'#if currently facing north, change to west
            elif self.direction == 'S': #if currently facing south, change to west
                self.direction = 'W'
            #Change the position of the car        
            self.carPosition = (row, col-1) #moving left means you subtract one column
            pic = PhotoImage(file=str(self.direction)+'.gif') #replace the car image with proper direction
            self.setCarLabel(pic,row,col-1) #invoke setCarLabel function
            self.gameOver()     #check to see if the game is over 

    def rightKey(self, event): #Comments for subsequent arrow key functions are similar to those above
        row = self.carPosition[0]
        col = self.carPosition[1]
        if col <= 4:
            self.blank = Canvas(self, width=self.cellWidth, height=self.cellHeight,bg='gray49')
            self.blank.config(highlightbackground='gray49')
            self.blank.grid(row=row, column=col)
            self.blank.configure(highlightbackground='gray49')
            if self.direction == 'N':
                self.direction = 'E'
            elif self.direction == 'S':
                self.direction = 'E'          
            self.carPosition = (row, col+1)
            pic = PhotoImage(file=str(self.direction)+'.gif')
            self.setCarLabel(pic,row,col+1)
            self.gameOver()      
                
    def upKey(self, event):
            row = self.carPosition[0]
            col = self.carPosition[1]
            if row >= 2 and row <=3:  #If they are not hitting the title bar
                self.blank = Canvas(self, width=self.cellWidth, height=self.cellHeight,bg='gray49')
                self.blank.configure(highlightbackground='gray49')
                self.blank.grid(row=row, column=col)
                if self.direction == 'E':
                    self.direction = 'N'
                elif self.direction == 'W':
                    self.direction = 'N'                
                pic = PhotoImage(file=str(self.direction)+'.gif')
                self.carPosition = (row-1, col)
                self.setCarLabel(pic, row-1,col)
                self.gameOver()

    def downKey(self, event):
            row = self.carPosition[0]
            col = self.carPosition[1]
            if row <= 2:      #If they are not hitting the status bar
                self.blank = Canvas(self, width=self.cellWidth, height=self.cellHeight,bg='gray49')
                self.blank.configure(highlightbackground='gray49')
                self.blank.grid(row=row, column=col)
                if self.direction == 'E':
                    self.direction = 'S'
                elif self.direction == 'W':
                    self.direction = 'S'        
                pic = PhotoImage(file=str(self.direction)+'.gif')
                self.carPosition = (row+1, col)
                self.setCarLabel(pic,row+1,col)
                self.gameOver()   
        
    def gameOver(self):
        if self.carPosition[0]==1:   #If the car is in the top row of the parking lot
            if self.dictOfTopSlots[(self.carPosition[0], self.carPosition[1])] == 0:  #If there is no car currently in that row & column
                self.text.set('        Congratulations! You win.        ')#again, the flanking space is an aesthetic fix
                self.win=True #change win instance variable to true
                self.bell(0) #bell rings and screen flashes
                self.unbindArrowKeys()#unbind arrow keys to stop the car from continuing to move
                pic = PhotoImage(file='youwin.gif') #celbratory picture appears
                imageLabel = Label(self, image=pic)
                imageLabel.pic = pic
                imageLabel.grid(row=1,rowspan=3, columnspan=6)
            elif self.dictOfTopSlots[(self.carPosition[0], self.carPosition[1])] == 1:  #if you crash into a car
                self.text.set('Collision! This spot was occupied.') #status bar is updated
                self.bell(0) #bell rings
                self.crash = Sign(self.carPosition[0],self.carPosition[1],1) #crash image appears
                self.addSign(self.crash, 'newGIF.gif') #invoke addSign function
                
        if self.carPosition[0]==3:    #If the car is in the bottom row of the parking lot 
            #(comments from here to line 265 are same as from lines 235-247
             if self.dictOfLowSlots[(self.carPosition[0], self.carPosition[1])] == 0: 
                self.text.set('        Congratulations! You win.        ')
                self.win=True
                self.bell(0)
                self.unbindArrowKeys()
                pic = PhotoImage(file='youwin.gif')
                imageLabel = Label(self, image=pic)
                imageLabel.pic = pic
                imageLabel.grid(row=1, rowspan=3, columnspan=6)
             elif self.dictOfLowSlots[(self.carPosition[0], self.carPosition[1])] == 1:  
                self.text.set('Collision! This spot was occupied.')
                self.bell(0)        
                self.crash = Sign(self.carPosition[0],self.carPosition[1],1)
                self.addSign(self.crash, 'newGIF.gif')         
                            
class Car(): #Car class
    def __init__(self, row, column, typeOfCar): #initialize the class
        self.row = row #set instance variables
        self.column = column 
        self.typeOfCar = typeOfCar
        
class Sign(): #Sign class
    def __init__(self, row1, column1, columnspan): #initialize class
        self.row1 = row1 #set instance variables
        self.column1 = column1
        self.columnspan = columnspan
         
app = RaceApp() #invoke the Race App
app.mainloop() #Start the mainloop