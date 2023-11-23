import re
import os
os.system("cls" if os.name == "nt" else "clear")

my_file = open("day10inputele.txt", "r")
#my_file = open("day10sampleinput.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

cycleCounter = 1
valueX = 1
value20 = 0
log = [0]

#make list of vals to add at each cycle
for line in cl:
    inst = line.split()
    log.append(0)
    if len(inst) == 2:
        log.append(int(inst[1]))

#run through list, adding and doing appropriate thing

printBuffer=''
for pixelCounter in range(len(log)):
    valueX += log[pixelCounter]
    if cycleCounter%40==1 and cycleCounter>6:
        print(printBuffer+'')
        printBuffer=''
    if ((pixelCounter+1) % 40)==20:
        value20 += valueX * (pixelCounter + 1)
        pass
    if abs((valueX) - (((pixelCounter)%40))) <= 1:
        printBuffer+='#'
    else:
        printBuffer+='.'
    cycleCounter += 1

print(value20)


