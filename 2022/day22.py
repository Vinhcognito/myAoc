from liz import *
from collections import namedtuple
wipeTerminal()
import timing

my_file = open("inputs\day22sampleinput.txt", "r")
#my_file = open("inputs\day22input.txt", "r")
content = my_file.read()
cl=content.split("\n")


""" Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^) 
final password is the sum of 1000 times the row, 4 times the column, and the facing."""

grid={}
#0= empty
#1= wall

maxCol=0
#parse map
for row,line in enumerate(cl[:-2]):
    for col,c in enumerate(line):
        match c:
            case '':
                pass
            case '.':
                grid[row+1,col+1]=0
            case '#':
                grid[row+1,col+1]=1
        if col > maxCol:
            maxCol=col
maxCol+=1
#parse instructions
inst=[]
instruction = namedtuple('inst', ['t', 'v'])
#t=0 is a turn, t=1 is a move
#v is the number
isNum=False
templi=[]

for i,c in enumerate(cl[len(cl)-1]):
    match c:
        case "L":
            if isNum:
                inst.append(instruction(1,int(''.join(templi))))
                templi=[]
                isNum=False
            inst.append(instruction(0,-1))
        case "R":
            if isNum:
                inst.append(instruction(1,int(''.join(templi))))
                isNum=False
                templi=[]
            inst.append(instruction(0,1)) 
        case c:
            templi.append(c)
            isNum=True
if isNum == True:
    inst.append(instruction(1,int(''.join(templi))))
point = namedtuple('point', ['x', 'y'])
gridmax=point(maxCol,len(cl)-2)

def startingPos():
    i=0
    while i < len(cl[0]):
        if (1,i) in grid:
            if grid[1,i]==0:
                return i
        i+=1
""" Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^) """
def changeDir(dir,turn):
    #R +1, L -1
    dir+=turn
    if dir==4:
        dir=0
    if dir==-1:
        dir=3
    return dir

def doInst(r,c,d,cur):
    match inst[cur].t:
        case 0:
            d = changeDir(d,inst[cur].v)
        case 1:
            i = 0
            while i < inst[cur].v:
                match d:
                    case 0:
                        c+=1
                        if checkPos(r,c)==0:
                            i+=1
                        elif checkPos(r,c)==1:
                            c-=1
                            break
                        else:
                            clear,r,c = wrap(r,c,d)
                            if clear:
                                i+=1
                            else:
                                c-=1
                                break
                    case 1:
                        r+=1
                        if checkPos(r,c)==0:
                            i+=1
                        elif checkPos(r,c)==1:
                            r-=1
                            break
                        else:
                            clear,r,c = wrap(r,c,d)
                            if clear:
                                i+=1
                            else:
                                r-=1
                                break
                    case 2:
                        c-=1
                        if checkPos(r,c)==0:
                            i+=1
                        elif checkPos(r,c)==1:
                            c+=1
                            break
                        else:
                            clear,r,c = wrap(r,c,d)
                            if clear:
                                i+=1
                            else:
                                c+=1
                                break
                    case 3:
                        r-=1
                        if checkPos(r,c)==0:
                            i+=1
                        elif checkPos(r,c)==1:
                            r+=1
                            break
                        else:
                            clear,r,c = wrap(r,c,d)
                            if clear:
                                i+=1
                            else:
                                r+=1
                                break
    return r,c,d

def checkPos(r,c):
    if (r,c) in grid:
        if grid[r,c]==0:
            return 0
        if grid[r,c]==1:
            return 1
    else:
        return 2

def wrap(r,c,d):
    match d:
        case 0:
            i=c
            step=1
        case 1:
            i=r
            step=1
        case 2:
            i=c
            step=-1
        case 3:
            i=r
            step=-1
    
    if d == 0 or d == 2:
        while True:
            i+=step
            if (r,i) in grid:
                if grid[r,i]==0:
                    return True,r,i
                if grid[r,i]==1:
                    return False,r,c
            if i > gridmax.x and step ==1:
                i=0
            elif i < 1 and step == -1:
                i=gridmax.x
                    
    if d == 1 or d == 3:
        while True:
            i+=step
            if (i,c) in grid:
                if grid[i,c]==0:
                    return True,i,c
                if grid[i,c]==1:
                    return False,r,c
            if i > gridmax.y and step ==1:
                i=0
            elif i < 1 and step == -1:
                i=gridmax.y
                    
cur=0
row=1
col=startingPos()
dir=0
print("starting r:{} c:{}".format(row,col))
while cur < len(inst):
    print('inst type: {} v: {}'.format(inst[cur].t,inst[cur].v))
    row,col,dir = doInst(row,col,dir,cur)
    print('row: {} col: {} dir: {} '.format(row,col,dir))
    cur+=1

print('row: {} col: {} dir: {} '.format(row,col,dir))
print("part1 answer = 1000*{} + 4*{} + dir {} = {}".format(
    row,col,dir,(1000*row)+(4*col)+dir))