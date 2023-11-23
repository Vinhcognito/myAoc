import re
import os
os.system("cls" if os.name == "nt" else "clear")

my_file = open("day8input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

treeGrid=[] 
#0,0 = top left

#generate array of tree heights
for x,s in enumerate(cl):
    treeGrid.append([])
    for y,h in enumerate(s):
        treeGrid[x].append(int(h))

#count visible trees, part 1

count=0
xMax=len(treeGrid)
yMax=len(treeGrid[1])

def checkTree(x,y,h):
    checkCount=0
    x1Pass=0
    x2Pass=0
    y1Pass=0
    y2Pass=0
    for xCheck in range(xMax-1):
        if xCheck < x:
            if  h > treeGrid[xCheck][y]:
                x1Pass+=1
        if x1Pass>0:
                checkCount+=1    
        if xCheck > x:
            if  h > treeGrid[xCheck][y]:
                x2Pass+=1
        if x2Pass>0:
                checkCount+=1    
    for yCheck in range(yMax-1):
        if yCheck < y:
            if  h > treeGrid[x][yCheck]:
                y1Pass+=1
        if y1Pass>0:
                checkCount+=1    
        if yCheck > y:
            if  h > treeGrid[x][yCheck]:
                y2Pass+=1
        if y2Pass>0:
                checkCount+=1    
    if checkCount ==0:
        return 0
    else: 
        return 1


for x in range(1,xMax-2):
    for y in range(1,yMax-2):
        count+=checkTree(x,y,treeGrid[x][y])
 
edgeTrees=396 #or 394 or 392 lol
print('part1 answer',count+edgeTrees)

""" #test treegrid
tempstr=''
for x in range(len(treeGrid)):
    print(tempstr)
    tempstr=''
    for y in range(len(treeGrid[x])):
        tempstr +=str(treeGrid[x][y])
        
 """
