import re
import os
import math
os.system("cls" if os.name == "nt" else "clear")

my_file = open("day9input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

dictVisit={'0,0':1}
#tailPos=[0,0]
tailPos=[[0,0] for i in range(10)]
#headPos=[0,0]
x=0
y=1
head=0
'''from reddit

rope = [0] * 10
seen = [set([x]) for x in rope]
dirs = {'L':+1, 'R':-1, 'D':1j, 'U':-1j}
sign = lambda x: complex((x.real>0) - (x.real<0), (x.imag>0) - (x.imag<0))

for line in open('in.txt'):
    for _ in range(int(line[2:])):
        rope[0] += dirs[line[0]]

        for i in range(1, 10):
            dist = rope[i-1] - rope[i]
            if abs(dist) >= 2:
                rope[i] += sign(dist)
                seen[i].add(rope[i])

print(len(seen[1]), len(seen[9]))
'''

def moveHead(dir,steps):
    match dir:
        case 'U':
            for i in range(1,steps+1):
                tailPos[head][y]+=1
                moveTail(0)
        case 'D':
            for i in range(1,steps+1):
                tailPos[head][y]-=1
                moveTail(0)   
        case 'L':
            for i in range(1,steps+1):
                tailPos[head][x]-=1
                moveTail(0) 
        case 'R':
            for i in range(1,steps+1):
                tailPos[head][x]+=1
                moveTail(0) 
    return

def moveTail(num):
    lead = num
    sub = num+1

    xdiff=(tailPos[lead][x]-tailPos[sub][x])
    ydiff=(tailPos[lead][y]-tailPos[sub][y])
    
    if abs(xdiff)<2 or abs(ydiff)<2:
        pass

    if abs(xdiff)==2 and abs(ydiff)==2:
        tailPos[sub][x]+=int(xdiff/2)
        tailPos[sub][y]+=int(ydiff/2)

    if abs(xdiff)==2 and abs(ydiff)!=2:       
        tailPos[sub][x]+=int(xdiff/2)
        if abs(ydiff)==1:
            tailPos[sub][y]+=ydiff
        else:
            pass

    if abs(ydiff)==2 and abs(xdiff)!=2:
        tailPos[sub][y]+=int(ydiff/2)
        if abs(xdiff)==1:
            tailPos[sub][x]+=xdiff
        else:
            pass
    if num < 8:
        moveTail(num+1)
    if num ==8:
        dictVisit[str(tailPos[9][x])+','+str(tailPos[9][y])]=1
    return

for s in cl:
    dir, steps = s.split()
    moveHead(dir,int(steps))
    
        
print('part2 answer',len(dictVisit))