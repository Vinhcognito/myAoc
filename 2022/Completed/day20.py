from liz import *
from collections import namedtuple
wipeTerminal()
import timing

#my_file = open("inputs\day20sampleinput.txt", "r")
my_file = open("inputs\day20input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")
decryptionkey=811589153
""" 1000th, 2000th, and 3000th
 numbers after the value 0, wrapping around 
 the list as necessary. """

inst= namedtuple('num', ['v','o'])
#v = value, o = origin
li=[]

for idx,value in enumerate(cl):
    li.append(inst(int(value)*decryptionkey,idx))

def printlist(li):
    temp=[]
    for i in li:
        temp.append(i.v)
    print(temp)
    return

def getAnswer(li):
    temp=[]
    for i,inst in enumerate(li):
        if int(inst.v)==0:
            if i+1000 > len(li)-1:
                temp.append((i+1000)%(len(li)))
            else:
                temp.append(i+1000)
            if i+2000 > len(li)-1:
                temp.append((i+2000)%(len(li)))
            else:
                temp.append(i+2000)
            if i+3000 > len(li)-1:
                temp.append((i+3000)%(len(li)))
            else:
                temp.append(i+3000)
            return li[temp[0]].v,li[temp[1]].v,li[temp[2]].v
        else:
            pass
    return

#print("initial")
#printlist(li)
current=0
newidx=0
iteration=0
move=0
while iteration < 10:
    while current < len(li):
        for i,inst in enumerate(li):
            if inst.o==current:
                #if inst.v>len(li):
                move=(inst.v)%(len(li)-1)
                newidx=i+move
                if newidx >= len(li):
                    newidx=newidx%(len(li))+1
                #print("step {},({}) currently at idx:{} moving {} spaces to idx:{} ".format(inst.o,inst.v,i,move,newidx))
                li.insert(newidx,li.pop(i))
                #printlist(li)
                current+=1
    current=0
    iteration+=1
    print(iteration)
    timing.now()


x=getAnswer(li)
print('part2answer: ',int(x[0])+int(x[1])+int(x[2]))