import re
import os
os.system("cls" if os.name == "nt" else "clear")

#my_file = open("day10input.txt", "r")
my_file = open("day10sampleinput.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")
bigSum = 0

cycleCounter = 1
valueX = 1

    


print("\nstart")
for line in cl:
    inst = line.split()
    flag = False
    if inst[0] == "addx":
        valueX += int(inst[1])
        flag = True
        cycleCounter += 1
    elif inst[0] == "noop":
        cycleCounter += 1
    else:
        print("not recognized")
        break
    if cycleCounter % 40 == 20:
        bigSum += (cycleCounter * valueX)
        print(cycleCounter,(cycleCounter*valueX),bigSum)
    if flag:
        cycleCounter += 1
        if cycleCounter % 40 == 20:
            bigSum += (cycleCounter * valueX)
            print(cycleCounter,(cycleCounter*valueX),bigSum)
        
print(bigSum)
print(len(cl),cycleCounter)

#up to 180 is right, 220 is wrong lol
