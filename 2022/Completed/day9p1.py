import re
import os
import math
os.system("cls" if os.name == "nt" else "clear")

my_file = open("day9sampleinput2.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

dictVisit={'0,0':1}
tailPos=[0,0]
newtailPos=[[0,0] for i in range(9)]
headPos=[0,0]
x=0
y=1

def moveHead(dir,steps):
    match dir:
        case 'U':
            for i in range(1,steps+1):
                headPos[y]+=1
                moveTail(0)
        case 'D':
            for i in range(1,steps+1):
                headPos[y]-=1
                moveTail(0)   
        case 'L':
            for i in range(1,steps+1):
                headPos[x]-=1
                moveTail(0) 
        case 'R':
            for i in range(1,steps+1):
                headPos[x]+=1
                moveTail(0) 
    return

#part1's movetail
def moveTail():
    
    xdiff=(headPos[x]-tailPos[x])
    ydiff=(headPos[y]-tailPos[y])

    if abs(xdiff)<2 or abs(ydiff)<2:
        pass

    if abs(xdiff)==2 and abs(ydiff)==2:
        tailPos[x]+=int(xdiff/2)
        tailPos[y]+=int(ydiff/2)

    if abs(xdiff)==2 and abs(ydiff)!=2:       
        tailPos[x]+=int(xdiff/2)
        if abs(ydiff)==1:
            tailPos[y]+=ydiff
        else:
            pass

    if abs(ydiff)==2 and abs(xdiff)!=2:
        tailPos[y]+=int(ydiff/2)
        if abs(xdiff)==1:
            tailPos[x]+=xdiff
        else:
            pass

    dictVisit[str(tailPos[x])+','+str(tailPos[y])]=1
    return

def moveTails(num):
    xdiff=(headPos[x]-tailPos[x])
    ydiff=(headPos[y]-tailPos[y])

    if abs(xdiff)<2 or abs(ydiff)<2:
        pass

    if abs(xdiff)==2 and abs(ydiff)==2:
        tailPos[x]+=int(xdiff/2)
        tailPos[y]+=int(ydiff/2)

    if abs(xdiff)==2 and abs(ydiff)!=2:       
        tailPos[x]+=int(xdiff/2)
        if abs(ydiff)==1:
            tailPos[y]+=ydiff
        else:
            pass

    if abs(ydiff)==2 and abs(xdiff)!=2:
        tailPos[y]+=int(ydiff/2)
        if abs(xdiff)==1:
            tailPos[x]+=xdiff
        else:
            pass

    dictVisit[str(tailPos[x])+','+str(tailPos[y])]=1
    return 


for s in cl:
    dir, steps = s.split()
    moveHead(dir,int(steps))
    
        
print('part1 answer',len(dictVisit))
print('part2 answer',len(dictVisit))