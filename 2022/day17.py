from liz import *
import copy
wipeTerminal()
import timing

#my_file = open("day17sampleinput.txt", "r")
my_file = open("day17input.txt", "r")
content = my_file.read().strip()
#cl=content.split("\n")

grid={(1,0):1,(2,0):1,(3,0):1,(4,0):1,(5,0):1,(6,0):1,(7,0):1}
gust=[]
rockChecks=[    
                [(0,0),(1,0),(2,0),(3,0)],
                [(-1,1),(0,0),(1,1),(0,2)],
                [(0,0),(1,0),(2,0),(2,1),(2,2)],
                [(0,0),(0,1),(0,2),(0,3)],
                [(0,0),(1,0),(0,1),(1,1)]
            ]
tallest=[0,0,0,0,0,0,0,0]
#parsegustinput
for c in content:
    if c == '<':
        gust.append(-1)
    else:
        gust.append(1)

gustCount=0
rockCount=0
currentRock=4
rockPosx=0
rockPosy=0
x=0
y=1
atRest=False

#rock origin is at bottom most and then left most rock
def createRock():
    global rockCount
    global currentRock
    global rockPosx
    global rockPosy
    global atRest

    rockCount+=1
    currentRock+=1
    atRest = False

    if currentRock==5:currentRock=0

    if currentRock != 1:
        rockPosx=3
        rockPosy=highestRock()+4
    else:
        rockPosx=4
        rockPosy=highestRock()+4
    return

def highestRock():
    max=0
    for i in grid.keys():
        if i[1] > max:
            max = i[1]
    return max

def calcGust():
    global gustCount
    gustCount+=1
    return (gust[(gustCount-1)%len(gust)])
 

def setRocks():
    global grid
    for check in rockChecks[currentRock]:
        grid[(rockPosx+check[x],rockPosy+check[y])]=1
        #check for tallest in column
        if (rockPosy+check[y]) > tallest[rockPosx+check[x]]:
            tallest[rockPosx+check[x]] = rockPosy+check[y]
    return

def dropRock():
    global rockPosy
    rockPosy-=1
    return

def leftRock():
    global rockPosx
    rockPosx-=1
    return

def rightRock():
    global rockPosx
    rockPosx+=1
    return   

def checkCollision(action):
    flags=0
    for check in rockChecks[currentRock]:
        #check left
        if action==-1:
            if (rockPosx+check[x]-1==0 or
            (rockPosx+check[x]-1,rockPosy+check[y]) in grid):
                flags+=1
        #check right
        if action==1:
            if (rockPosx+check[x]+1==8 or
            (rockPosx+check[x]+1,rockPosy+check[y]) in grid):
                flags+=1
        #check bottom
        if action==0:
            if (rockPosx+check[x],rockPosy+check[y]-1) in grid:
                flags+=1
        
    match action,flags:
        case -1,0:
            leftRock()
            return False
        case -1,flags:
            return False
        case 1,0:
            rightRock()
            return False
        case 1,flags:
            return False
        case 0,0:
            dropRock()
        case 0,flags:
            setRocks()
            pruneSet(tallest)
            return True
        
def pruneSet(tallest):
    global grid
    for i in list(grid.keys()):
        if i[y] < min(tallest[1:]):
            del(grid[i])
    return

remainderrockcount=0

while rockCount < 50455:
    createRock()
    while not atRest:
        temp=calcGust()
        checkCollision(temp)
        atRest=checkCollision(0)
    if rockCount ==2022:
        print('highest rock @ 2022',highestRock())
    if rockCount ==1000000000000%50455:
        print('highest rock @ 1000000000000%50455',highestRock())
        remainderrockcount=highestRock()



print('5*len of gust: ',5*len(gust))
print(highestRock()* math.floor((1000000000000/(5*len(gust))))+ remainderrockcount)