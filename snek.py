from os import system,get_terminal_size
from random import randint
from readchar import readkey,readchar
from math import fabs
from time import sleep
import signal

TERMINAL_SIZE=get_terminal_size()
TERMINAL_WIDTH=int((TERMINAL_SIZE[0])/4-2)
TERMINAL_HEIGHT=TERMINAL_SIZE[1]-4

class snek():
    def __init__(self):
        self.length=1
        self.position=[(0,0)]
        self.posx_list=[0]
        self.posy_list=[0]
        self.head=self.position[0]
        self.tail=self.position[-1]
        self.food_in=[]
    # for updating the snek on keypress or each position change:
    # how this works is when a key is given, it works like enqueue
    # and dequeue of queue, the position of the head is added and 
    # last part of the snake is removed, so the snek is one block 
    # ahead of it's previous position
    def positionupdate(self,key,food):
        if key==0:
            self.head=(self.head[0] + 0,self.head[1] - 1)
        if key==1:
            self.head=(self.head[0] - 1,self.head[1] + 0)
        if key==2:
            self.head=(self.head[0] + 0,self.head[1] + 1)
        if key==3:
            self.head=(self.head[0] + 1,self.head[1] + 0)
        # Overflow and underflow corrections:
        self.head=((TERMINAL_WIDTH+self.head[0])%(TERMINAL_WIDTH),
                    (TERMINAL_HEIGHT+self.head[1])%(TERMINAL_HEIGHT))
        # once head is updated check if it ate food
        self.yummy(food)
        if self.tail in self.food_in:
            del self.food_in[0]
        # if the food is in snek then grow it, i.e
        # length will be longer then the position array
        if len(self.position)==self.length:
            self.position.pop()
        #Eating itself condition:
        if (self.head in self.position):
            return False
        self.position.insert(0,self.head)
        self.posx_list=[]
        self.posy_list=[]
        for x,y in self.position:
            self.posx_list.append(x)
            self.posy_list.append(y)
        self.tail=self.position[-1]
        return True

    #when the snake eats the food:          
    def yummy(self,food):
        if self.head==food:
            if self.length>1:
                self.food_in.append(self.position[0])
            self.length+=1

class game():
    def __init__(self):
        self.WIN_SCORE=TERMINAL_WIDTH*TERMINAL_HEIGHT-2
        self.SNEK=snek()
        self.score=0
        self.key=0
        # keys ->     up,left,down,right
        self.keylist=['w','a','s','d',
                      'W','A','S','D',
                      'k','h','j','l',
                      'K','H','J','L',
                      '\x1b[A','\x1b[D','\x1b[B','\x1b[C']
    def food(self):
        while True:
            if (pos:=(randint(0,TERMINAL_WIDTH-1),randint(0,TERMINAL_HEIGHT-1))) not in self.SNEK.position:
                self.food_position=pos
                break
    def snek_position(self):
        return self.SNEK.positionupdate(self.key,self.food_position)
    def printboard(self):
        system("clear")
        print(f"score = {self.score}\tfood={self.food_position}\thead={self.SNEK.head}",end=" ")
        #the whole readkeycoordinate system is d#esigned to make these loops work and not the other way round
        for i in range(TERMINAL_HEIGHT+2):
            print()
            for j in range(0,(TERMINAL_WIDTH+2)*4):
                j=j/4
                if((j-1,i-1)==self.food_position):
                    print("o",end="")
                elif((j-1,i-1)==self.SNEK.head):
                    print("O",end="")
                elif((j-1,i-1) in self.SNEK.food_in):
                    print("x",end="")
                elif((j-1,i-1)==self.SNEK.tail):
                    print("x",end="")
                elif((j-1,i-1) in self.SNEK.position):
                    print("-",end="")
                elif(j in [0,TERMINAL_WIDTH+1] or (i in [0,TERMINAL_HEIGHT+1] and j==int(j))):
                    print("*",end="")
                else:
                    print(end=" ")
        print()
    def readinput(self):
        def raise_timeout(*args, **kwargs):
            raise TimeoutError()
        signal.signal(signalnum=signal.SIGALRM, handler=raise_timeout)
        if self.score!=0:
            signal.alarm(1)
        try:
            key=readkey()
        except TimeoutError:
            key=self.keylist[self.key]
        return key

    def gameplay(self):
        self.food()
        print("press any key to start(q to exit)")
        while ((key:=self.readinput())!="q" and self.score!=self.WIN_SCORE):
            if key in self.keylist:
                key=self.keylist.index(key)%4
            else:
                key=-1
            if key!=-1 and (fabs(key-self.key)!=2 or self.SNEK.length<3):
                self.key = key
            if self.snek_position():
                if self.SNEK.head==self.food_position:
                    self.food()
                    self.score+=1
                self.printboard()
            else:
                break
        if self.score==self.WIN_SCORE:
            print(f"You win. Score: {self.score}")
        else:
            print(f"Game over. Score: {self.score}")
a = game()
a.gameplay()
