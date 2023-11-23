import string
import os
from enum import Enum,auto

os.system("cls" if os.name == "nt" else "clear")
print('\n\n\n\n\n\n\n**********************************************************'+
    '***********************************')

my_file = open("day12sampleinput.txt", "r")
#my_file = open("day12input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")


letters = list(string.ascii_lowercase)
l = Enum('', letters, start =1)
'''
l['y'].value  = 25
l(3).name     = c
'''
Grid=[] #x,y 
solveGrid=[]
countGrid=[]
#1=up
#2=down
#3=left
#4=right

#init
for x in range(0,len(cl[0])):
    Grid.append([])
    countGrid.append([])
    for y in range(0,len(cl)):
        Grid[-1].append(0)
        countGrid[-1].append(999)

solveGrid = Grid
#countGrid = Grid

#grid parse
startPos=[0,0]
endPos=[0,0]

for y in range(0,len(cl)):
    for x,m in enumerate(cl[y]):
        match m:
            case 'S':
                startPos = [x,y]
                Grid[x][y]=0
                
            case 'E':
                endPos = [x,y]
                Grid[x][y]=26
            case m:
                Grid[x][y]=l[m].value
                


def solve(x,y,target,step):
    target=Grid[x][y]-1
    #print(x,y,l(target).name)

    li = checkAll(x,y,target)

    if 1 not in li:
        target+=1
        li = checkAll(x,y,target)

    if li[0]:
        if  step+1< countGrid[x][y-1]:
            countGrid[x][y-1]=step+1
            solve(x,y-1,target,step+1)
        else:
            solve(x,y-1,target,countGrid[x][y-1])
    if li[1]:
        if step+1 < countGrid[x][y+1]:
            countGrid[x][y+1]=step+1
            solve(x,y+1,target,step+1)
        else:
            solve(x,y+1,target,countGrid[x][y+1])
    if li[2]:
        if step+1 < countGrid[x-1][y]:
            countGrid[x-1][y]=step+1
            solve(x-1,y,target,step+1)
        else:
            solve(x-1,y,target,countGrid[x-1][y])
    if li[3]:
        if step+1 < countGrid[x+1][y]:
            countGrid[x+1][y]=step+1
            solve(x+1,y,target,step+1)
        else:
            solve(x+1,y,target,countGrid[x+1][y])

    if x == startPos[0] and y == startPos[1]:
        print("finallydone",x,y,step)
    print("done",x,y,step)
    pass
    return 

def checkAll(x,y,target):
    li=[0,0,0,0]
    if checkUp(x,y,target):
        li[0]=1
    if checkDown(x,y,target):
        li[1]=1
    if checkLeft(x,y,target):
        li[2]=1
    if checkRight(x,y,target):
        li[3]=1
    return li

def checkUp(x,y,target):
    if y!=0:
        if Grid[x][y-1] == target:
            return True
    return False
def checkDown(x,y,target):
    if y!=len(Grid[0])-1:
        if Grid[x][y+1] == target:
            return True
    return False
def checkLeft(x,y,target):
    if x!=0:
        if Grid[x-1][y] == target:
            return True
    return False
def checkRight(x,y,target):
    if x!=len(Grid)-1:
        if Grid[x+1][y] == target:
            return True
    return False

solve(*endPos,26,0)

for x in range(len(countGrid)):
    for y in range(len(countGrid[0])):
        print(x,y,countGrid[x][y])