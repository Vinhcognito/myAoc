from liz import *
import copy
wipeTerminal()
import timing

#my_file = open("day14sampleinput.txt", "r")
my_file = open("day14input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

grid={}
#1=rock or sand
#0=air
lowestRock=0
leftlimit=200
rightlimit=0
floor = 0

def fillGap(x1,y1,x2,y2):
    global lowestRock
    global leftlimit
    global rightlimit
    grid[x1,y1]=1

    #figure out lowest rock
    if y1 > lowestRock:
        lowestRock = y1
    if y2 > lowestRock:
        lowestRock = y2

    #figure out x limits
    if x1 < leftlimit or x2 < leftlimit:
        leftlimit = min(x1,x2)
    if x2 > rightlimit or x1 > rightlimit:
        rightlimit = max(x1,x2)

    while x2!=x1 or y2!=y1:
        if x2 != x1:
            x1+=sign(x2-x1)
        if y2 != y1:
            y1+=sign(y2-y1)
        grid[x1,y1]=1
    return


#parse rocks
for line in cl:
    #print(line.split())
    for i,str in enumerate(line.split()):
        if str != '->':
            if i == 0:
                prevX,prevY = str.split(',')
            else:
                curX,curY = str.split(',')
                fillGap(int(prevX),int(prevY),int(curX),int(curY))
                prevX,prevY = curX,curY



#dropsand
def moveSand(x,y,atRest):
    if (x,y+1) not in grid.keys():
        return (x,y+1,0)
    if (x-1,y+1) not in grid.keys():
        return (x-1,y+1,0)
    if (x+1,y+1) not in grid.keys():
        return (x+1,y+1,0)
    return (x,y,1)


print("lowest rock is at: ",lowestRock)
floor=lowestRock+2
rightlimit +=400
print("leftlimit @ ",leftlimit)
print("rightlimit @ ",rightlimit)
i= 1
#make floor
for j in range(leftlimit,rightlimit):
    grid[j,floor]=1

while i > 0:
    sandX = 500
    sandY = 0
    atRest = 0
    while atRest != 1:
        sandX,sandY,atRest = moveSand(sandX,sandY,atRest)

        #part1 condition
        '''if sandY > lowestRock:
            print("part1: last sand at rest @ i = ",i-1)
            i=-1
            break'''
    grid[sandX,sandY]=1
    
    #part 2 condition
    if (500,0) in grid.keys():
        print("sand hole blocked @ i = ",i)
        i=-1
        break
    i+=1
    #print("i=",i)






