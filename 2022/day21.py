from liz import *
import copy
wipeTerminal()
import timing

#my_file = open("inputs\day21sampleinput.txt", "r")
my_file = open("inputs\day21input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

monkey={}
donkey={}
#monkey[name]=value,mon1,mon2,operation
value=0
m1=1
m2=2
op=3

li=[0,0,0,0,0]
for line in cl:
    if len(ints(line))==0:
        li[0],li[1],li[2],li[3]=line.split(' ')
        if li[0]=='root':
            li[2]="="
        if li[1]=='humn':
            li[1]='1j'
        if li[3]=='humn':
            li[3]='x'
        monkey[li[0][0:-1]]=0,li[1],li[3],li[2]
    else:
        monkey[line[0:4]]=[ints(line)[0]]
        if line[0:4]=='humn':
            del monkey['humn']

#test values of x
test=30000

conkey=copy.deepcopy(monkey)
donkey={}

old=0
new=len(monkey)

while old!=new:
    for name,mk in list(conkey.items()):
        if mk[value] != 0:
            donkey[name]=mk[value]
            del conkey[name]
        elif (mk[m1] in donkey and 
            mk[m2] in donkey and
            name!='root'
            ):
            donkey[name]=int(eval(''+str(donkey[mk[m1]])+mk[op]+str(donkey[mk[m2]])))
            del conkey[name]
        else:
            pass
    old = new
    new = len(conkey)

#print("part 2 answer: {} ".format(donkey['root']))


sum1=''
sum2=''
#write formula
def replace(s):
    tempstr=''
    if s in donkey or s == '1j':
        try: 
            return str(donkey[s])
        except KeyError:
            return '1j'
    else:
        tempstr+='('+replace(conkey[s][m1])
        tempstr+=conkey[s][op]
        tempstr+=replace(conkey[s][m2])+')'
        return eval(tempstr)
        #return tempstr

sum1 = replace(conkey['root'][m1])
sum2 = replace(conkey['root'][m2])

print(sum1)
print(sum2)
"""     if sum1!=sum2:
        test+=1
        if test%1000==0:
            print('currently testing: {}'.format(test))
            timing.now()
    else:
        print('part 2 answer x= : {})'.format(test)) """


#((278206989474842-(2*(769+(14*(((426+((((((277+(605+(((2*((((((((139+(2*(((((((772+((((49+((981+(((2*(113+(((2*(((((((709+((((147+(9*(330+((((((x+466)*23)-620)/3)-677)/2))))*2)-530)/2))*2)-726)/2)+870)/3)-706))-456)/2)))-776)/12))*17))/2)-74)*2))*2)-479)/3)-725)/2)+479)))+590)/3)-44)*2)-840)/3)+16))-592)*2)))/2)-182)/5)+841)*7))/6)-294)))))/5)


#PART 1
""" li=[0,0,0,0,0]
for line in cl:
    if len(ints(line))==0:
        li[0],li[1],li[2],li[3]=line.split(' ')
        monkey[li[0][0:-1]]=0,li[1],li[3],li[2]
    else:
        monkey[line[0:4]]=[ints(line)[0]]

while 'root' in monkey:
    for name,mk in list(monkey.items()):
        if mk[value] != 0:
            donkey[name]=mk[value]
            del monkey[name]
        elif mk[m1] in donkey and mk[m2] in donkey:
            donkey[name]=int(eval(''+str(donkey[mk[m1]])+mk[op]+str(donkey[mk[m2]])))
            del monkey[name]
        else:
            pass

print("part 1 answer: {} ".format(donkey['root'])) """