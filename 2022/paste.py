"""
Create a text file called  pi_digits.txt  as shown below . 
1. Read the file 
2. use readline() method 
3. write a number to the existing file 

Assignment 3
Vinh Tran
301324533
"""
# Week 12 Exercise 1 File Handling

f = open('pi_digits.txt', 'r')

while (True):
    line = f.readline()
    if not line:
        break
    print(line)

f.close()

f = open('pi_digits.txt', 'a')
f.write('5')
f.close()

f = open('pi_digits.txt', 'r')
print('\n\n'+f.read())