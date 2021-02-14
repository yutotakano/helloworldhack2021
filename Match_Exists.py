import random


class Tile: #Ignore the constructor
    def __init__(self,kind,value):
        self.kind = kind
        self.value = value
    
    def isEqTile(self): #isEqTile,isPlusMinus and isNumTile go in tile.py?
        if self.value == "=":
            return True
        else:
            return False
    def isPlusMinus(self):
        if self.value == "+" or self.value == "-":
            return True
        else:
            return False 
    def isNumTile(self):
        if self.kind == "num":
            return True
        else:
            return False         


def bothNum(tile1,tile2): #bothNum and bothPlusMinus used in match_exists- put in game?
    if ((tile1.kind == tile2.kind) and (tile1.kind == "num")):
        return True
    else:
        return False 

def bothPlusMinus(tile1,tile2):
    if (tile2.isPlusMinus() and tile1.isPlusMinus()):
        return True
    else:
        return False       

#lookForEq1 and looksForEq2 are used in match_exists
#(Optional) swap order of if and elifs to always choose largest match, but beware of the "continue" statements
def lookForEq1(board):
    matchList1 = []
    for i in range(0,5):
        for j in range(1,4):
            if(board[i][j].isEqTile()):
                if(bothNum(board[i][j-1],board[i][j+1])):
                    if int(board[i][j+1].value) == int(board[i][j-1].value): 
                        matchList1.extend([(i,j-1),(i,j),(i,j+1)])
                    
                    elif (j == 1 and board[i][3].isPlusMinus() and board[i][4].isNumTile()):
                        if int(board[i][0].value) == eval(str(board[i][2].value)+board[i][3].value+str(board[i][4].value)):
                            matchList1.extend([(i,0),(i,1),(i,2),(i,3),(i,4)])
                        else:
                            continue
                    
                    elif (j == 3 and board[i][1].isPlusMinus() and board[i][0].isNumTile()):
                        if int(board[i][4].value) == eval(str(board[i][2].value)+board[i][1].value+str(board[i][0].value)):
                            matchList1.extend([(i,0),(i,1),(i,2),(i,3),(i,4)])
                        else:
                            continue     

                else: continue
            else: 
                continue 

    return matchList1

def looksForEq2(board):
    matchList2 = []
    for j in range(0,5):
        for i in range(1,4):
            if(board[i][j].isEqTile()):
                if(bothNum(board[i-1][j],board[i+1][j])):
                    if int(board[i-1][j].value) == int(board[i+1][j].value): 
                        matchList2.extend([(i-1,j),(i,j),(i+1,j)])
                    
                    elif (i == 1 and board[3][j].isPlusMinus() and board[4][j].isNumTile()):
                        if int(board[0][j].value) == eval(str(board[2][j].value)+board[3][j].value+str(board[4][j].value)):
                            matchList2.extend([(0,j),(1,j),(2,j),(3,j),(4,j)])
                        else:
                            continue
                    
                    elif (i == 3 and board[1][j].isPlusMinus() and board[0][j].isNumTile()):
                        if int(board[4][j].value) == eval(str(board[2][j].value)+board[1][j].value+str(board[0][j].value)):
                            matchList2.extend([(0,j),(1,j),(2,j),(3,j),(4,j)])
                        else:
                            continue     

                else: continue
            else: 
                continue 

    return matchList2 

#This is the match exists function, currently takes a list of list of tiles as argument, change to make instance method
def match_exists(b):
    matches1 = lookForEq1(b)
    matches2 = looksForEq2(b)
    matches1.extend(matches2)
    totalMatches = []
    [totalMatches.append(x) for x in matches1 if x not in totalMatches]
    return totalMatches

#These were used for testing, don't put in game
t1 = Tile("num",1)
t2 = Tile("num",2)
te = Tile("op","=")
tp = Tile("op","+")
tm = Tile("op","-")

testBoard = [[t1,t1,t2,t1,t2],[te,t1,t1,te,t1],[t1,t2,t1,tp,t1],[tm,t1,tp,t1,t1],[t2,t1,t1,t1,t1]]

 





