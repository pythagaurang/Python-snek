from os import system,get_terminal_size
from random import randint
from readchar import readchar

TERMINAL_SIZE=get_terminal_size()
TERMINAL_WIDTH=TERMINAL_SIZE[0]
TERMINAL_HEIGHT=TERMINAL_SIZE[1]-2

class snek():
    def __init__(self):
        self.length=1
        self.position=[(0,0)]
        self.posx_list=[0]
        self.posy_list=[0]
        self.head=self.position[0]
        self.tail=self.position[-1]
    #for updating the snake on keypress or each position change:
    def positionupdate(self,key):
        if key=='w':
            self.head=(self.head[0] + 0,self.head[1] - 1)
        if key=='a':
            self.head=(self.head[0] - 1,self.head[1] + 0)
        if key=='s':
            self.head=(self.head[0] + 0,self.head[1] + 1)
        if key=='d':
            self.head=(self.head[0] + 1,self.head[1] + 0)
        #Overflow and underflow corrections:
        self.head=((TERMINAL_WIDTH+self.head[0])%(TERMINAL_WIDTH),
                (TERMINAL_HEIGHT+self.head[1])%(TERMINAL_HEIGHT))
        #Eating itself condition:
        if (self.head in self.position):
            return False
        else:
            if len(self.position)==self.length:
                self.position.pop()
            self.position.insert(0,self.head)
            self.posx_list=[]
            self.posy_list=[]
            for x,y in self.position:
                self.posx_list.append(x)
                self.posy_list.append(y)
            self.tail=self.position[-1]
            return True
    #when the snake eats the food:          
    def yummy(self):
        self.length+=1

class game():
    WIN_SNEK_LENGTH=TERMINAL_WIDTH*TERMINAL_HEIGHT-1
    SNEK=snek()
    def __init__(self):
        self.score=0
    def food(self):
        while True:
            if (pos:=(randint(0,TERMINAL_WIDTH-1),randint(0,TERMINAL_HEIGHT-1))) not in self.SNEK.position:
                self.food_position=pos
                self.food_posx=pos[0]
                self.food_posy=pos[1]
                break
    def snek_position(self):
        if (self.key in ['w','a','s','d','W','A','S','D']):
           return self.SNEK.positionupdate(self.key)
    def printboard(self):
        print(f"score = {self.score}\tfood={self.food_position}\thead={self.SNEK.head}",end=" ")
        #the whole coordinate system is designed to make these loops work and not the other way round
        for i in range(TERMINAL_HEIGHT):
            print()
            if(i in self.SNEK.posy_list or i==self.food_posy):
                for j in range(TERMINAL_WIDTH):
                    if((j,i)==self.food_position):
                        print("o",end="")
                    elif((j,i)==self.SNEK.head):
                        print("=",end="")
                    elif((j,i) in self.SNEK.position):
                        print("-",end="")
                    else:
                        print(end=" ")
        print() 
    def check_food(self):
        return self.SNEK.head == self.food_position

    def gameplay(self):
        self.food()
        while (key:=readchar())!='q':
            self.key = key
            if self.snek_position():
                if self.check_food():
                    self.SNEK.yummy()
                    self.food()
                    self.score+=1
                self.printboard()
            else:
                break

a = game()
a.gameplay()
