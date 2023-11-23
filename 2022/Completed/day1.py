import math
import time

def splitlist(li):
    
    currentsum=0

    for num in li:
        if not num:
            sumchecker(currentsum)
            currentsum=0
            print("0")
        
        else:
            currentsum+=int(num)

    return

def sumchecker(sum,first,second,third):
    temp=0

    if sum > third:
        third = sum
        print(">3")
        if sum > second:
            temp = second
            second = third
            third = temp
            print(">2")
            if sum > first:
                temp = first
                first = second
                second = temp
                print(">1")
    return(first,second,third)

first = int(0)
second =  int(0)
third = int(0)



my_file = open("day1input.txt", "r")
content = my_file.read()
content_list=content.split("\n")


currentsum=0

for num in content_list:
    if not num:
        (first,second,third)=sumchecker(currentsum,first,second,third)
        currentsum=0
        #print("0")
        
    else:
        currentsum+=int(num)


print(first+second+third)
