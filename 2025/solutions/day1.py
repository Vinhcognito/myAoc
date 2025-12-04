
import math


def part_one(input:str):

    dial = 50
    counter = 0
    lines = input.strip().split("\n")
    for line in lines:
        if line[0] == "L":
            dial -= int(line[1:])
        else:
            dial += int(line[1:])

        if dial%100 == 0:
            counter += 1

    return(counter)

    


def part_twofdsafsd(input:str):
    dial = 50
    counter = 0
    lines = input.strip().split("\n")
    for line in lines:
        num = int(line[1:])

        if num > 99:
            counter += math.trunc(num/100)

        else:
            if line[0] == "L":
                if num >= dial:
                    counter += 1
            else:
                if dial+num >= 99:
                    counter += 1

        if line[0] == "L":
            dial -= num
        else:
            dial += num
        dial = dial%100

        print(f"{line[0]}{num} =>{dial}     {counter}")

        
    return(counter)

def part_two(input:str):
    from itertools import accumulate
    lines = input.strip().split("\n")
    turns = [50]

    for line in lines:
        if line[0] == "L":
            sign = -1
        else:
            sign = 1
        num = int(line[1:])
        turns.extend([sign*1]*num)
        
    count = 0
    for num in list(accumulate(turns)):
        if num % 100 == 0:
            count += 1

    return(count)