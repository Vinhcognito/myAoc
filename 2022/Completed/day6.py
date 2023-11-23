import re
import os
os.system("cls" if os.name == "nt" else "clear")

my_file = open("day6input.txt", "r")
content = my_file.read().strip()

currentList2=[13]
for s,p in enumerate(content):
    currentList2=content[s-14:s]
    currentSet=set(currentList2)
    if len(currentSet)==14:
        print("part2 answer:",currentSet,s)
        break

currentList1=[3]
for s,p in enumerate(content):
    currentList1=content[s-4:s]
    currentSet=set(currentList1)
    if len(currentSet)==4:
        print("part1 answer:",currentSet,s)
        break 

#ellie
""" my_file = open("day6input.txt", "r")
content = my_file.read().strip()

charIndex = 13
contentLength = len(content)
flag = True

while charIndex < contentLength:
    for x in range(14):
        for y in range(14):
            if (x != y) and (content[charIndex-x] == content[charIndex-y]):
                charIndex+=1
                flag=True
                break
            flag=False
        if flag:
            break
    if flag==False:
        print("Marker after",charIndex+1,"characters")
        break """