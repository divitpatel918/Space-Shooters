
import tkinter
import turtle
import random
import datetime
# import time

class SpaceBackground(turtle.RawTurtle): 
    def __init__(self , gameApp):
        
        super().__init__(gameApp.canvas)

        self.gameApp = gameApp

        self.shape('spacebackground.gif')  
        self.penup()            
        self.goto(150,150)
        self.screen.update()

class BigAlien(turtle.RawTurtle): 
    def __init__(self , gameApp):
        
        super().__init__(gameApp.canvas)

        self.gameApp = gameApp

        self.shape('bigalien.gif')  
        self.penup()            
        self.goto(160,30)
        self.screen.update()


class Spaceship(turtle.RawTurtle):
    """
    A tile that a player can click on.

    A Tile *is* a RawTurtle by the power of inheritance.  So it has methods
    such as shape() and goto() already defined.  We can add other methods like
    leftClickHandler().
    """

    def __init__(self, gameApp):

        super().__init__(gameApp.canvas)


        self.gameApp = gameApp
        
        
        self.shape('Spaceship.gif')  
        self.penup()            
        self.goto(180,300)
        self.screen.update()
        
        self.speed = 10 

        
    def moveLeft(self):
        x = self.xcor()
        x -= self.speed
        y = self.ycor()
        if x < 0 or x > 350:
            x = -x 
        self.goto(x,y)

    def moveRight(self):
        x = self.xcor()
        x += self.speed
        y = self.ycor()
        if x < 0 or x > 350:
            x = -x
        self.goto(x,y)
       

    def shipcor(self):
        return [self.xcor(), self.ycor()]
        
    
        
        

    

class Alien(turtle.RawTurtle):
    def __init__(self ,gameApp, rowIndex, colIndex,):

        super().__init__(gameApp.canvas)


        self.gameApp = gameApp
        self.rowIndex = rowIndex
        self.colIndex = colIndex
        
        
        
        self.shape('alien2.gif')  
        self.penup()            
        self.goto(colIndex*55 + 70, rowIndex*55 + 70)
        # print(colIndex, rowIndex)
        self.screen.update()

    def shoot(self):
         self.gameApp.alienBlocks.append(AlienBlock(self.gameApp, self.xcor()+ 50, self.ycor()+7))
    
class Block(turtle.RawTurtle):
    def __init__(self, gameApp, x, y):
        super().__init__(gameApp.canvas)
        self.gameApp = gameApp
        self.color('#FFDF4F')  # Carleton Maize.
        self.shape('laserBullet.gif')
        self.penup()
        
        
        
        self.goto(x, y)

        
        self.dx = random.randint(-3, 3)
        # self.dx = 0 
        self.dy = random.randint(-6, -3)  # Drops down.

    def step(self):
        """Move this block one step."""
        # Use RawTurtle's methods to get the current x, y positions.
        x = self.xcor()
        y = self.ycor()
        x += self.dx 
        y += self.dy 
        self.goto(x, y)

        
        

    def isCollidingWith(self,Alien):
        """Is this block colliding with the other block?"""
        if abs(self.xcor() - Alien.xcor()) < self.gameApp.blockSize and abs(self.ycor() - Alien.ycor()) < self.gameApp.blockSize:
            return True
        return False 

class AlienBlock(turtle.RawTurtle):
    def __init__(self, gameApp, x, y):
        super().__init__(gameApp.canvas)
        self.gameApp = gameApp
        self.color('#FFDF4F')  # Carleton Maize.
        self.shape('alienlaser.gif')
        self.penup()
      
        
        
        
        self.goto(x, y)

        self.dx = random.randint(-5, 5)  # Moves left or right.
        self.dy = random.randint(-6, -3)  # Drops down.

        

    def step(self):
        """Move this block one step."""
        # Use RawTurtle's methods to get the current x, y positions.
        x = self.xcor()
        y = self.ycor()
        x += self.dx 
        y -= self.dy 
        # b = Spaceship.shipcor(self)
        self.goto(self.gameApp.newSpaceship.xcor(), self.gameApp.newSpaceship.ycor())
        self.goto(x,y)

    def isCollidingWith2(self,Spaceship):
        """Is this block colliding with the other block?"""
        if abs(self.xcor() - Spaceship.xcor()) < self.gameApp.blockSize and abs(self.ycor() - Spaceship.ycor()) < self.gameApp.blockSize:
            return True
        return False 
        


    
    
        




class Game(tkinter.Frame):
    
        
    def __init__(self, root=None):
        
        super().__init__(root)
        # Save the root window as self.root so we can refer to it later.
        self.root = root
        self.width = 400
        self.height = 400
        self.blockSize = 30
        self._buildWindow()
        self.startNewGame()
        self._animate()
        self.screen.update()
        

    def _buildWindow(self):
        """Part of __init__, to build the window."""
        self.root.title('Space Shooters')
     
        self.pack()

       
        self.canvas = tkinter.Canvas(self, width=400, height=400)
      
    
        self.canvas.pack(side='left')
        
        # happens.
        sideBar = tkinter.Frame(self, padx=10, pady=10)
        
        sideBar.pack(side='right', fill='y')
        
        self.quitButton = tkinter.Button(sideBar, text='Quit', command=self.root.destroy)
        self.quitButton.pack(side='bottom')
        self.newGameButton = tkinter.Button(sideBar, text='New game', command=self.startNewGame)
        self.newGameButton.pack() 

        timeLabel = tkinter.Label(sideBar, text='Elapsed seconds')
        timeLabel.pack()
        # A tkinter string variable that can be auto-updated.
        self.elapsedTime = tkinter.StringVar()
        self.elapsedTime.set('0')
        self.elapsedTimeLabel = tkinter.Label(sideBar, textvariable=self.elapsedTime)
        self.elapsedTimeLabel.pack()

        self.alienLabel = tkinter.Label(sideBar, text='Aliens remaining = ' + '15')
        self.alienLabel.pack()



        # Create a 'dummy' turtle to configure this canvas a bit.
        theTurtle = turtle.RawTurtle(self.canvas)
        theTurtle.ht()
        self.screen = theTurtle.getscreen()
        self.screen.setworldcoordinates(0, 360, 360, 0)
        self.screen.register_shape('spacebackground.gif')
        self.screen.register_shape('Spaceship.gif')
        self.screen.register_shape('alien2.gif')
        self.screen.register_shape('laserBullet.gif')
        self.screen.register_shape("bigalien.gif")
        self.screen.register_shape('alienlaser.gif')
        
        # self.screen.register_shape('block', ((0, 0), (0, self.blockSize),
        #                                      (self.blockSize, self.blockSize),
        #                                      (self.blockSize, 0)))

      
    

    def startNewGame(self):
        self.isGameOver = False
        self.screen.clear()
        # Turn on screen buffering; this makes drawing a lot faster.
        self.screen.tracer(0)
        self.screen.update()
        self.blocks = []
        self.alienBlocks=[]
        self.over = False
        self.spaceBackground = SpaceBackground(self)
        self.newSpaceship = Spaceship(self)
        # self.l = [self.newSpaceship]
        self.newbigAlien = BigAlien(self)
      
        

        self.matrix = [] # creates list 
        count = 0 # starts with 0 
        for rowIndex in range(3): # for every 3 rows 
            row = []
            for colIndex in range(5): # for every col it makes 5 aliens 
                newAlien = Alien(self, rowIndex, colIndex) # for every col made it creates that alien 
                count = count + 1 # 
                row.append(newAlien)
            self.matrix.append(row)
            
        
        
        self.screen.onkey(self.handleW,'Left')
        self.screen.onkey(self.handleD,'Right')
        self.screen.onkey(self.handleW,'a')
        self.screen.onkey(self.handleD,'d')
         # Quit when 'q' key is pressed.
        self.screen.onkey(self.root.destroy, 'q')
        self.screen.onkey(self.handleM, 'space')
        self.screen.onkey(self.handleN, 'n')
        # Listen to keypresses.
        self.screen.listen()

        # self._animate()
        # self.screen.update()


        # Timer.
        self.startTime = datetime.datetime.now()
        self.root.after(1000, self.tickTock)
        self.lastBulletFired = datetime.datetime.now()


        self.screen.update()

    def matrixLength(self):
        total = 0 
        for row in self.matrix:
            total = total + len(row)
        return total 

           

    def _animate(self):
        number_of_colors = 8

        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
        """Move blocks."""
        for block in self.blocks:
            for row in self.matrix:
                for alien in row:
                    if block.xcor() != alien.xcor() or block.ycor() != alien.ycor():
                        if block.isCollidingWith(alien):
                            self.blocks.remove(block)
                            block.ht()
                            row.remove(alien)
                            alien.ht()
                            numEnemiesleft = self.matrixLength() 
                            self.alienLabel.configure(text='Aliens remaining = ' + str(self.matrixLength()))
                            print(numEnemiesleft)
                        # if block.isCollidingWith(self.newbigAlien):
                        #     self.blocks.remove(block)
                        #     block.ht()
                        #     self.newbigAlien.ht()
                        #     self.onBigAlienDead('You Won!!!!!')  
                        #     print('hello')
                            
                            if numEnemiesleft == 0:
                                print('hello')
                                self.newbigAlien.ht()
                                self.isGameOver = True
                                self.onGameOver('You Won!!!!!')    
                            #print('hello' , self.matrix)
                            self.screen.bgcolor(random.choice(color))
                        
            if self.blocks!=[]:
                block.step() # Have each block move one step.
        for bullet in self.alienBlocks:
            if bullet.isCollidingWith2(self.newSpaceship):
                self.alienBlocks.remove(bullet)
                bullet.ht()
                #self.l.remove(self.newSpaceship)
                self.newSpaceship.ht()
                self.over = True
                self.isGameOver = True
                self.onlose('You Lost')
            bullet.step()
        
        
        self.screen.update()    # Flip the buffer and see the effects all at once.
        # Wait 33 milliseconds and animate again.  That's roughly 30 frames per
        # seconds.  Human eyes likes at least 24 frames per second to make
        # animation look smooth.
        self.screen.ontimer(self._animate, 33)

        # if self.matrix == [[], [], []]:
        #     # print("hello", self.matrix)
            
            
        #     # print('Game Over')
        


    def tickTock(self):
            """Calculate and display the number of seconds elapsed."""
            currentTime = datetime.datetime.now()
            elapsedTime = currentTime - self.startTime
            elapsedSeconds = elapsedTime.seconds
            # Setting the variable is enough to display it.
            self.elapsedTime.set(str(elapsedSeconds))
            # Call this method again after 1000 millisecond = 1 second.
            # print(self.isGameOver)
            if self.isGameOver == False:
                self.root.after(1000, self.tickTock)


   

    def onGameOver(self, text):
        """
        End a game.

        This method called by a Tile object when a bomb has been clicked.  Also
        called by decNumTiles when the game is won.  This method in turn calls
        onGameOver on each of the 100 tiles.
        """
        for row in self.matrix:
            for alien in row:
                alien.onGameOver()
        self.screen.update()
        tkinter.messagebox.showinfo(message=text, title='Game over')

    def onlose(self,text):
        tkinter.messagebox.showinfo(message=text, title='Game over')

    def onBigAlienDead(self,text):
        tkinter.messagebox.showinfo(message=text, title='Game over')
        self.isGameOver = True

        

    def handleW(self):
        """Add a block."""
        # print("hello")
        self.newSpaceship.moveLeft()
        self.screen.update()

    def handleD(self):
        # print("bye")
        self.newSpaceship.moveRight()
        self.screen.update()
        
    def handleM(self):
        # print(datetime.datetime.now())
        recordTime = datetime.datetime.now()
        elapsedTime = recordTime - self.lastBulletFired
        elapsedSeconds = elapsedTime.seconds
        # print(elapsedSeconds)   
        self.newSpaceship.shipcor()
        #self.blocks.append(Block(self, self.newSpaceship.xcor()+ 50, self.newSpaceship.ycor()+7))
        # if self.timeleft > 2000:
        
        if elapsedSeconds > 0 and not self.over:
            self.blocks.append(Block(self, self.newSpaceship.xcor()+ 5, self.newSpaceship.ycor()-10))
            self.lastBulletFired = datetime.datetime.now()
            self.alienBlocks.append(AlienBlock(self,100,50))
            self.alienBlocks.append(AlienBlock(self,150,50))
            # self.alienBlocks.append(AlienBlock(self,150,50))
            self.alienBlocks.append(AlienBlock(self,150,50))
            self.alienBlocks.append(AlienBlock(self,200,50))
        #return
    def handleN(self):
        # for row in self.matrix:
        #     for alien in row:
        self.alienBlocks.append(AlienBlock(self,150,150))
                #alien.shoot()
                    
        print('hello')
        self.screen.update()



def main():
    print('Welcome to Space Shooters')
    root = tkinter.Tk()
    theGame = Game(root)
    theGame.mainloop()
    print('Farewell.')

if __name__ == '__main__':
    main()


