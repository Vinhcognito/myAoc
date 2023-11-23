from liz import *
wipeTerminal()
import timing

#my_file = open("inputs\day18sampleinput.txt", "r")
my_file = open("inputs\day18input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

grid={}
global testgrid
global outergrid
testgrid={}
outergrid={}
#         x,y,z
for line in cl:
    grid[line]=1


px=0
py=0
pz=0
global xmin
global xmax
global ymin
global ymax
global zmin
global zmax

xmin=100
xmax=0
ymin=100
ymax=0
zmin=100
zmax=0
connectedCount=0

def checkSides_p1(x,y,z):
    count=0
    x=int(x)
    y=int(y)
    z=int(z)

    global xmin
    global xmax
    global ymin
    global ymax
    global zmin
    global zmax

    if x <xmin:
        xmin=x
    if x > xmax:
        xmax=x
    if y <ymin:
        ymin=y
    if y > ymax:
        ymax=y
    if z <zmin:
        zmin=z
    if z > zmax:
        zmax=z

    if str(x+1)+','+str(y)+','+str(z) in grid:
        count+=1
    if str(x-1)+','+str(y)+','+str(z) in grid:
        count+=1
    if str(x)+','+str(y+1)+','+str(z) in grid:
        count+=1
    if str(x)+','+str(y-1)+','+str(z) in grid:
        count+=1
    if str(x)+','+str(y)+','+str(z+1) in grid:
        count+=1
    if str(x)+','+str(y)+','+str(z-1) in grid:
        count+=1

    return count 



def checkExternal(x,y,z):
    #check if cube is air and outside of cube
    #if count is between is 1-5 then definitely outside
    #if 6 then we are unsure
    count=0
    i=0
    if str(x+i)+','+str(y)+','+str(z)  in grid:
        return 0
    else:
        while True:
            if str(x+i)+','+str(y)+','+str(z) in grid:
                count+=1
                break
            if x+i > xmax+5:
                break
            i+=1
        i=0 
        while True:
            if str(x-i)+','+str(y)+','+str(z) in grid:
                count+=1
                break
            if x-i < xmin-5:
                break
            i+=1
        i=0 
        while True:
            if str(x)+','+str(y+i)+','+str(z) in grid:
                count+=1
                break
            if y+i > ymax+5:
                break
            i+=1
        i=0 
        while True:
            if str(x)+','+str(y-i)+','+str(z) in grid:
                count+=1
                break
            if y-i < ymin-5:
                break
            i+=1
        i=0 
        while True:
            if str(x)+','+str(y)+','+str(z+i) in grid:
                count+=1
                break
            if z+i > zmax+5:
                break
            i+=1
        i=0 
        while True:
            if str(x)+','+str(y)+','+str(z-i) in grid:
                count+=1
                break
            if z-i < zmin-5:
                break
            i+=1
        if count>=1:
            if count==6:
                return 6
            else:
                return 1
    return 0

def checkSides_p2(x,y,z):
    #this checks for how many air edges a cube is touching
    #since all internals are now filled
    count=0
    x=int(x)
    y=int(y)
    z=int(z)

    if str(x+1)+','+str(y)+','+str(z) in outergrid:
        count+=1
    if str(x-1)+','+str(y)+','+str(z) in outergrid:
        count+=1
    if str(x)+','+str(y+1)+','+str(z) in outergrid:
        count+=1
    if str(x)+','+str(y-1)+','+str(z) in outergrid:
        count+=1
    if str(x)+','+str(y)+','+str(z+1) in outergrid:
        count+=1
    if str(x)+','+str(y)+','+str(z-1) in outergrid:
        count+=1
    return count





connectedCount2=0
for pos,state in list(grid.items()):
    px,py,pz = pos.split(',')
    connectedCount2+=checkSides_p1(px,py,pz)
    connectedCount+=checkSides_p1(px,py,pz)
print('part1: surface area = ',len(grid.keys())*6-connectedCount)


internalcubeCount=0
#extend limits a bit
xmin-=5
if xmin<0:
    xmin=-1
xmax+=5
ymin-=5
if ymin<0:
    ymin=-1
ymax+=5
zmin-=5
if zmin<0:
    zmin=-1
zmax+=5


testgridcount=0
for x in range(xmin,xmax+1):
    for y in range(ymin,ymax+1):
        for z in range(zmin,zmax+1):        
            temp=checkExternal(x,y,z)
            if temp>0:
                if temp==6:
                    #if external check returns 6, unsure if in or out
                    testgrid[str(x)+','+str(y)+','+str(z)]=1
                    testgridcount+=1
                else:
                    #if external between is 1-5 then definitely outside
                    outergrid[str(x)+','+str(y)+','+str(z)]=1


print('testgridcount = ',testgridcount)
connectedCount2=0

def growOuterGrid(x,y,z):
    #assume every cube touching something in outergrid to be outergrid
    #unless it is in grid
    #if we test it against testgrid, we should find it and conclude that
    #it is outer, ie everything left in testgrid will be an internal airpocket

    count=0
    x=int(x)
    y=int(y)
    z=int(z)

    if str(x+1)+','+str(y)+','+str(z) not in grid:   
        if str(x+1)+','+str(y)+','+str(z) in testgrid:
            outergrid[str(x+1)+','+str(y)+','+str(z)]=1
            del testgrid[str(x+1)+','+str(y)+','+str(z)]
    if str(x-1)+','+str(y)+','+str(z) not in grid:
        if str(x-1)+','+str(y)+','+str(z) in testgrid:
            outergrid[str(x-1)+','+str(y)+','+str(z)]=1
            del testgrid[str(x-1)+','+str(y)+','+str(z)]
    if str(x)+','+str(y+1)+','+str(z) not in grid:
        if str(x)+','+str(y+1)+','+str(z) in testgrid:
            outergrid[str(x)+','+str(y+1)+','+str(z)]=1
            del testgrid[str(x)+','+str(y+1)+','+str(z)]
    if str(x)+','+str(y-1)+','+str(z) not in grid:
        if str(x)+','+str(y-1)+','+str(z) in testgrid:
            outergrid[str(x)+','+str(y-1)+','+str(z)]=1
            del testgrid[str(x)+','+str(y-1)+','+str(z)]
    if str(x)+','+str(y)+','+str(z+1) not in grid:
        if str(x)+','+str(y)+','+str(z+1) in testgrid:
            outergrid[str(x)+','+str(y)+','+str(z+1)]=1
            del testgrid[str(x)+','+str(y)+','+str(z+1)]
    if str(x)+','+str(y)+','+str(z-1) not in grid:
        if str(x)+','+str(y)+','+str(z-1) in testgrid:
            outergrid[str(x)+','+str(y)+','+str(z-1)]=1
            del testgrid[str(x)+','+str(y)+','+str(z-1)]
    
#grow outergrid by 1 cube each iteration,guaranteeing it to be outside
i=0
while True:
    old=len(testgrid.keys())
    for pos,state in list(outergrid.items()):
        px,py,pz = pos.split(',')
        growOuterGrid(px,py,pz)
    new =len(testgrid.keys())
    print('newtestgridcount: ',new)
    if new== old:
        break

for pos,state in list(testgrid.items()):
    px,py,pz = pos.split(',')
    grid[str(x)+','+str(y)+','+str(z)]=1


connectedCount2=0
for pos,state in list(grid.items()):
    px,py,pz = pos.split(',')
    connectedCount2+=checkSides_p2(px,py,pz)
print('part2: surface area = ',connectedCount2)


