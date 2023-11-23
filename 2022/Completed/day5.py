import re
import os
os.system("cls" if os.name == "nt" else "clear")

my_file = open("day5input.txt", "r")
content = my_file.read().strip()
content_list=content.split("\n")

#read initial stacks
stacks = [[] for i in range(9)]

for s in content_list[:10]:
    for p,c in enumerate(s):
        if c.isalpha():
            col = int(((p-1)/4))
            stacks[col].append(c)
    
for col in range(len(stacks)):
    stacks[col].reverse()


iMove=0
iFrom=0
iTo=0
tempStack=[]

#read (and perform) moves
for s in content_list[10:]:
    #read instructions
    iMove=int(s[4:s.find("from")].strip())
    iFrom=int(s[s.find("from")+4:s.find("to")].strip())
    iTo=int(s[s.find("to")+2:].strip())

    #moves for part 1
    '''
    for i in range(iMove):
        stacks[iTo-1].append(stacks[iFrom-1].pop())
    '''

    #moves for part 2
    for i in range(iMove):
        tempStack.append(stacks[iFrom-1].pop())
    for i in range(iMove):
        stacks[iTo-1].append(tempStack.pop())



        
#print answer
for i in range(9):
    print(stacks[i].pop())


'''alternate parse instructions

p1,p2 = stacks[:],stacks[:]
for s in content_list[10:]:
    _, n, _, src, _, dest = s.split()

    #what?
    p1[src], p1[dest] = p1[src][n:],  p1[src][:n][::-1] + p1[dest]
    p2[src], p2[dest] = p2[src][n:],  p2[src][:n]       + p2[dest]
    '''