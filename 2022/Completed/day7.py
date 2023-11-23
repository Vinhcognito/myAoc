import re
import os
os.system("cls" if os.name == "nt" else "clear")

'''
reddit:
from collections import defaultdict
from itertools import accumulate


dirs = defaultdict(int)

for line in open('in.txt'):
    match line.split():
        case '$', 'cd', '/': curr = ['']
        case '$', 'cd', '..': curr.pop()
        case '$', 'cd', x: curr.append(x+'/')
        case '$', 'ls': pass
        case 'dir', _: pass
        case size, _:
            for p in accumulate(curr):
                dirs[p] += int(size)

print(sum(s for s in dirs.values() if s <= 100_000),
      min(s for s in dirs.values() if s >= dirs[''] - 40_000_000))

'''

my_file = open("day7input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

depth=0
marker=[0]
folders={}
folderName=[]

def fileSize(s):
    #read file size from a string
    result=''
    for c in s:
        if c.isnumeric():
            result+=str(c)
        else:
            return int(result)

#parse folder directories and file sizes
for i,s in enumerate(cl):
    if s[0]=="$":
        if s[2:4]=='cd':
            if s[5]=="/":
                folderName=[]
            elif s[5:7]=='..':
                folderName.pop()
            else:
                folderName.append(s[5:])
        if s[2:4]=='ls':
            x=1
            folderContents=[]
            while x>0 and (x+i)<len(cl):
                if cl[i+x][0]=='$':
                    x=0
                elif cl[i+x][0:3]=='dir':
                    folderContents.append(cl[i+x][4:])
                else:
                    folderContents.append(fileSize(str(cl[i+x])))
                if x==0:
                    break
                else:
                    x+=1
            folders[''.join(folderName)]=folderContents


#sum folder sizes
calc={}
flag = True
tempsum=0

while len(calc)!=len(folders):
    for key,value in folders.items():
        tempsum=0
        for i in value:
            if str(i).isnumeric():
                tempsum+=i
            else:
                #look for size in calc
                if (''+key+i) in calc.keys():
                    tempsum+=calc[''+key+i]
                else:
                    flag=False
            if flag==False:
                break
        if flag:
            calc[key]=tempsum
        else:
            flag=True
    #print("+1 cycle")
           
sum=0
#sum small folders, part1 answer
for k,v in calc.items():
    if int(v) <= 100000:
        sum+=int(v)
print('part1 answer:',sum)

#part2 size of smallest folder that can be deleted
freeSpace=70000000-calc['']
print('current free space',freeSpace)
reqDelete=30000000-freeSpace
print('amount to delete',reqDelete)

li=[]
for k,v in calc.items():
    if int(v) > reqDelete:
        li.append(v)
li.sort()
print('part2 answer',li[0])

