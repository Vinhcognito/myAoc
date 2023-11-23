from liz import *
from collections import namedtuple
wipeTerminal()
import timing


my_file = open("inputs\day15sampleinput.txt", "r")
#my_file = open("inputs\day15input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")


pos = namedtuple('SB', ['sx', 'sy' , 'bx','by','r'])
sensors=[]
li=[]

def calcDist(x1,y1,x2,y2):
    return max(x1,x2)-min(x1,x2)+max(y1,y2)-min(y1,y2)

for line in cl:
    li=ints(line)
    sensors.append(pos(*li,calcDist(*li)))


inputRow=2000000
exclude={}
#set that has any position in input row that cannot have a beacon

#determine what sensors influence the input row
for sb in sensors:
    #exclude all pos in sensor range that are in input row
    if sb.sy-sb.r <= inputRow and inputRow <=sb.sy+sb.r:
        for i in range(sb.r-calcDist(sb.sx,sb.sy,sb.sx,inputRow)+1):
            exclude[sb.sx+i]=1
            exclude[sb.sx-i]=1

#run through sensor list and check for any S or B in inputrow
for sb in sensors:
    if sb.sy == inputRow:
        if sb.sy in exclude:
            del(exclude[sb.sy])
    if sb.by == inputRow:
        if sb.by in exclude:
            del(exclude[sb.by])

templist=list(exclude)
templist.sort()

print('part 1 answer, exclusions at y={}: {}'.format(inputRow,len(exclude)))
