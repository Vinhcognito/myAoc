from liz import *
from collections import namedtuple
import copy
wipeTerminal()
import timing

my_file = open("inputs\day24sampleinput.txt", "r")
#my_file = open("inputs\day24input.txt", "r")
content = my_file.read()
cl=content.split("\n")
cl.reverse()

#[t,x,y] 
#starting pos = [0,1,5]
#exit pos = [t,6,0]

map=[]
mapWidth=len(cl[0])-1   #7
mapHeight=len(cl)-1     #5

mappings={-1:'#',0:'.',1:'>',2:'^',3:'<',4:'v',20:'2',30:'3',40:'4'}
#-1 = wall, 0 = empty , 1 = blizzard

#printArray(matrix,[],[],True,revY=True,mappings=mappings)

#initalize blank 2dmatrix

    
#parse input or timestep 0
matrixzero = [[0] * (mapWidth+1) for _ in range(mapHeight+1)]
matrix = [[0] * (mapWidth+1) for _ in range(mapHeight+1)]
blizzlist=[]
# > = 1     
# ^ = 2           
# < = 3         
# v = 4

for x,line in enumerate(cl):
    for y,c in enumerate(line):
        match c:
            case '#':
                matrix[x][y]=-1
                matrixzero[x][y]=-1
            case '.':
                matrix[x][y]=0
            case '>':
                matrix[x][y]=1
                blizzlist.append((x,y,1))
            case '^':
                matrix[x][y]=2
                blizzlist.append((x,y,2))
            case '<':
                matrix[x][y]=3
                blizzlist.append((x,y,3))
            case 'v':
                matrix[x][y]=4   
                blizzlist.append((x,y,4))
                
def getEmptyMatrix():
    return copy.deepcopy(matrixzero)
    
map.append(matrix)


def genNextBlizzards(b):
    '''from list of blizzards (x,y,d), output updated matrix and new blizzlist'''
    newmatrix = copy.deepcopy(matrixzero)
    newBlizzlist=[]
    for x,y,d in b:
        match d:
            case 1:
                if y+1 == mapWidth:
                    y=1
                else:
                    y+=1
                newmatrix[x][y]=checkWind(newmatrix[x][y],d)
                newBlizzlist.append((x,y,1))
            case 2:
                if x+1 == mapHeight:
                    x=1
                else:
                    x+=1
                newmatrix[x][y]=checkWind(newmatrix[x][y],d)
                newBlizzlist.append((x,y,2))
            case 3:
                if y-1 == 0:
                    y=mapWidth-1
                else:
                    y-=1
                newmatrix[x][y]=checkWind(newmatrix[x][y],d)
                newBlizzlist.append((x,y,3))
            case 4:
                if x-1 == 0:
                    x=mapHeight-1
                else:
                    x-=1
                newmatrix[x][y]=checkWind(newmatrix[x][y],d) 
                newBlizzlist.append((x,y,4))

    return newmatrix,newBlizzlist

def checkWind(i,d):
    if i == 1 or i==2 or i==3 or i==4:
        return 20
    if i == 20:
        return 30
    if i == 30:
        return 40
    return d

#generate maps for t to 50
#printArray(matrix,[],[],True,revY=True,mappings=mappings,title='TIME={}'.format(0))
t=1
m,b = genNextBlizzards(blizzlist)
#printArray(m,[],[],True,revY=True,mappings=mappings,title='TIME={}'.format(t))
while t < 4:
    map.append(m)
    m,b = genNextBlizzards(b)
    t+=1
    printArray(m,[],[],True,revY=True,mappings=mappings,title='TIME={}'.format(t))
