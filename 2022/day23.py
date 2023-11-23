from liz import *
from collections import namedtuple
wipeTerminal()
import timing

my_file = open("inputs\day23sampleinput.txt", "r")
#my_file = open("inputs\day23input.txt", "r")
content = my_file.read()
cl=content.split("\n")
cl.reverse()

oldDict={}
pDict={}
priorityCounter = 0

elf = namedtuple('elf', ['x', 'y'])

#parse starting positions
for row,line in enumerate(cl):
    for col,c in enumerate(line):
        if c == '#':
            pDict[col,row]=[elf(0,0)]
            

#at end of each round you need to increment priority counter

def calcProposedMove(oldx,oldy):
    broken = False
    for x in range(-1,2):
        for y in range(-1,2):
            if (oldx + x, oldy + y) in oldDict:
                if x == 0 and y == 0:
                    pass
                else:
                    broken = True
                    break
        if broken:
            return(prioritizedMove(oldx, oldy))
    #print("Elf not moving:", oldx, oldy)
    return(oldx, oldy)

def prioritizedMove(oldx, oldy):
    #x + 1 is east of x; y + 1 is north of y
    c = 0
    #print("Elf @: ", oldx, oldy)
    while c < 4:
        #check N
        if (priorityCounter + c) % 4 == 0:
            if (((oldx - 1, oldy + 1) in oldDict ) or
                ((oldx, oldy + 1) in oldDict) or 
                ((oldx + 1, oldy + 1) in oldDict)
                ):
                pass
            else:
                #print("moving north to", oldx, oldy +1)
                return(oldx, oldy + 1)
        #check S
        elif (priorityCounter + c) % 4 == 1:
            if (((oldx - 1, oldy - 1) not in oldDict )and 
                ((oldx, oldy - 1) not in oldDict )and 
                ((oldx + 1, oldy - 1) not in oldDict)
                ):
                #print("moving south to", oldx, oldy - 1)
                return(oldx, oldy - 1)
        #check W
        elif (priorityCounter + c) % 4 == 2:
            if (((oldx - 1, oldy - 1) not in oldDict )and 
                ((oldx - 1, oldy) not in oldDict )and 
                ((oldx - 1, oldy + 1) not in oldDict)
                ):
                #print("moving west to", oldx - 1, oldy)
                return(oldx - 1, oldy)
        #check E
        elif (priorityCounter + c) % 4 == 3:
            if (((oldx + 1, oldy - 1) not in oldDict )and 
                ((oldx + 1, oldy) not in oldDict )and 
                ((oldx + 1, oldy + 1) not in oldDict)
                ):
                #print("moving east to", oldx + 1, oldy)
                return(oldx + 1, oldy)
        c += 1
    #print("NO MOVE AVAILABLE", oldx, oldy)
    return(oldx, oldy)
        


def calcEmptyTiles(d:dict):
    xMin=0
    xMax=0
    yMin=0
    yMax=0
    for pos in d:
        if pos[0]<xMin:
            xMin= pos[0]
        if pos[0]>xMax:
            xMax= pos[0]
        if pos[1]<yMin:
            yMin= pos[1]
        if pos[1]>yMax:
            yMax= pos[1]
            
    mapArray = []
    
    for y in range(yMin,yMax+1):
        mapArray.append([])
        for x in range(xMin,xMax+1):
            mapArray[y - yMin].append(0)
            
    for b in mapArray:
        #print(b)
        pass
        
    for k in d:
        #print(k)
        mapArray[k[1] - yMin][k[0] - xMin] = 1
    
    
    #printArray(mapArray,[],[],true='#',false='.',revY=True)
    return ((xMax-xMin + 1)*(yMax-yMin + 1))-len(d)


print('Initial Elf Positions: {}'.format(calcEmptyTiles(pDict)))
currentRound = 0
while True:
    oldDict= pDict.copy()
    pDict={}
    pX=0
    pY=0
    for key in oldDict:
        tempLi = calcProposedMove(*key)
        #print("tempLi:", tempLi)
        try:
            pX=tempLi[0]
        except:
            pass
        try:
            pY=tempLi[1]
        except:
            pass
        
        if (pX,pY) in pDict:
            pDict[pX,pY].append(elf(*key))
        else:
            pDict[pX,pY]=[elf(*key)]

        
        
    #check for conflicts

    for key,value in pDict.copy().items():
        if len(value) > 1:
            for e in value:
                pDict[e.x,e.y]=elf(e.x,e.y)
            del pDict[key]

    if oldDict == pDict:
        print("done")
        break
    currentRound+=1
    priorityCounter+=1
    print('end of round {}: {}'.format(currentRound,calcEmptyTiles(pDict)))


