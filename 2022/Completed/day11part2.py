import re
import math
import os
import sys


os.system("cls" if os.name == "nt" else "clear")
print('\n\n\n\n\n\n\n\n\n\n\n**********************************************************'+
    '***********************************')
sys.set_int_max_str_digits(99999)
#my_file = open("day11sampleinput.txt", "r")
my_file = open("day11input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

monkey=[[[],'',1,1,1,0] for i in range(0,int((len(cl)+1)/6))]
items=0; op=1; test=2; testTrue=3; testFalse=4; inspects=5

primeList=[]
tempList=[]
tempStr=''
currentMonkey=0

#monkey parse
for i in range(0,len(cl),7):
    #items
    tempList = cl[i+1].split(' ')
    for n in range(4,len(tempList)):
        if tempList[n].isnumeric():
            monkey[currentMonkey][items].append(int(tempList[n]))
        else:
            monkey[currentMonkey][items].append(int(tempList[n].split(',')[0]))

    #op
    tempList = cl[i+2].split(' ')
    match tempList[6]:
        case '+': monkey[currentMonkey][op]='1 ' 
        case '-': monkey[currentMonkey][op]='2 '
        case '*': monkey[currentMonkey][op]='3 '
    match tempList[7]:
        case 'old':
            monkey[currentMonkey][op]+='0'
        case  num:
            monkey[currentMonkey][op]+=str(num)
    
    #test
    monkey[currentMonkey][test]=int(cl[i+3].split(' ')[-1])
    primeList.append(int(cl[i+3].split(' ')[-1]))
    #testTrue
    monkey[currentMonkey][testTrue]=int(cl[i+4].split(' ')[-1])
    #testFalse
    monkey[currentMonkey][testFalse]=int(cl[i+5].split(' ')[-1])

    currentMonkey+=1

round = 1
currentMonkey = 0
new = 0

def doMath(input,o,num=0):
    '''1add  2subt 3mult 4divide  num=0 means 'old'
    '''
    match o,num:
        case o,0: return doMath(input,o,input)
        case 1,num:  return (input + num)
        case 2,num:  return (input - num)
        case 3,num:  return (input * num)
        case 4,num:  return math.floor(input / num)
        
#debug
def debug():
    for s in range(len(monkey)):
        print('monkey ',s,'holds: ')
        for i in range(len(monkey[s][items])):
            print(monkey[s][items][i])
        #print(monkey[s][op])
        #print(monkey[s][test])
        #print(monkey[s][testTrue])
        #print(monkey[s][testFalse])
    return

lcm = 1
for i in primeList:
    lcm*=i

def newWorry(num):
    while num > lcm +1:
        num-=lcm
    return num

def newWorry2(num):
    if num > lcm+1:
        return num%lcm
    return num

while round <=10000:
    for currentMonkey in range(len(monkey)):
        for old in range(len(monkey[currentMonkey][items])):
            #inspect and monkeymath
            monkey[currentMonkey][inspects]+=1
            new = doMath(monkey[currentMonkey][items].pop(0),
                        int(monkey[currentMonkey][op].split(' ')[0]),
                        int(monkey[currentMonkey][op].split(' ')[1])
                        )

            #worry dived by 3
            #new = doMath(new,4,3)
            new = newWorry2(new)
            #test and toss to new monkey
            if new % monkey[currentMonkey][test]==0:
                monkey[ monkey[currentMonkey][testTrue] ][items].append(new)
            else:
                monkey[ monkey[currentMonkey][testFalse] ][items].append(new)

    #print('\n\nround ',round)
    round+=1
    #debug()


#part 1 answer
li=[]
for i in range(len(monkey)):
    print(monkey[i][inspects])
    li.append(monkey[i][inspects])
li.sort()
print ("monkey business = ",li[-1]*li[-2])