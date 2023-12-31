import math
import os

def sign(x):
    """Returns -1 or +1 corresponding to the sign of x"""
    return int(math.copysign(1, x))

def wipeTerminal(s:str ='*',num:int=80):
    """Use to put a line of separators (str) of length (num) in the terminal"""
    temp=s*num
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n'+temp)
    return

def ints(string:str,digits:int=0,signs:bool=True):
    """Returns list of all integers in string
    
    Searches string for connected integers flanked by non integer characters
    Will recognize negative signs (-) in front of digits by default

    digits: 
        max number of digits that each int is allowed to have
        set to 0 for unlimited digits
    signs:
        When False: will ignore negative (-) signs that may be in front of integers
        Defaulted to True

    """
    intlist=[]
    tempString=[]
    count=0
    for idx,c in enumerate(string):
        if str(c).isnumeric():
            if signs==True and idx>0:
                if string[idx-1] == '-':
                    tempString.append('-')
            tempString.append(c)
            count+=1
            if count == digits:
                intlist.append(int(''.join(tempString)))
                tempString=[]
                count=0
        else:
            if count>=1:
                intlist.append(int(''.join(tempString)))
                tempString=[]
                count=0
    
    if count>=1:
        intlist.append(int(''.join(tempString)))
    return intlist

def strs(string:str,chars:int=0,):
    """Returns list of all strings in string
    
    Searches string for connected alphabetic chars flanked by non alpha  characters

    chars: 
        max number of chars that each string is allowed to have
        defaulted to 0 for unlimited digits
    """
    strlist=[]
    tempString=[]
    count=0
    for idx,c in enumerate(string):
        if str(c).isalpha():
            tempString.append(c)
            count+=1
            if count == chars:
                strlist.append(''.join(tempString))
                tempString=[]
                count=0
        else:
            if count>=1:
                strlist.append(''.join(tempString))
                tempString=[]
                count=0
    
    if count>=1:
        strlist.append(''.join(tempString))
    return strlist
    
def extendList(input_list:list,index:int,fill=0):
    """Returns list extended for index of list to exist 
    
    index: index that input_list will be extended to
    fill: default value for newly created indexes in list
    
    """
    while True:
        try:
            temp=tempList[index]
            break
        except IndexError:
            tempList.append(fill)
        except TypeError:
            tempList=[]
            tempList.append(input_list)
            return extendList(tempList,index,fill)
    return tempList

def extendList2D(li:list,index1:int,index2:int,fill=0):
    '''Copies contents of a list and returns it extended to just enough 
    with initial values = (fill)  for  li[index1][index2] to exist'''
    tempList = li
    try:
        temp=tempList[index1][index2]
    except IndexError:
        while len(tempList) <= index1:
            tempList.append([fill])
        tempList[index1] = extendList(tempList[index1],index2,fill)
    except TypeError:
        while len(tempList) <= index1:
            tempList.append([fill])
        tempList[index1] = extendList(tempList[index1],index2,fill)
    return tempList

def extendListRect(li:list,index1:int=1,index2:int=1,fill=0):
    '''Copies contents of a list and returns it extended so that all possible indices
     within [0,index1]X[0,index2] are created with initial values = (fill)'''
    tempList=li
    for i in range(index1):
        tempList=extendList2D(tempList,i,index2-1,fill)
    return tempList


def printArray(input_array:list, hRange=[], vRange=[],
                tight = True,
                revX= False, revY=False,
                true = '1', false = '0',
                mappings:dict={},
                title:str='',
                **kwargs
                ):
    """Prints contents of a 2D list into the terminal

    Args:
        hRange,vRange:list[int,int] 
                specify starting and ending index of values to print
                able to accept None in place of int
        tight: True, values are printed with no comma separation and with replacements specified
                from true and false parameters and any additional keyword pairs
                False, values are printed as values only with a comma separation
        revX:   Specifies whether the horizontal values are printed in ascending (False)
                or descending (True), index order
        revY:   Specifies whether the vertical values are printed in ascending (False)
                or descending (True), index order
        true,false: when tight=True, true replaces all True or 1 values with the str specified by true
                                    and all False or 0 values with the str specified by false
        mappings: a dictionary of value:replacement mappings that the function will use 
                    when tight is false. In addition to true,false, kwargs parameters
                    mapping gets priority if there are conflicts
        **additional keyword arguments:
        keyword='string'
                keywords will be converted from text to integer and will be used to replace 
                instances of that integer to the specified string when printing tight=true
    """
    replace=kwargs.copy()
    for k in list(replace):
        replace[text2int(k)]=replace[k]
    replace[1]=true
    replace[0]=false
    replace = replace | mappings


    if hRange == []:
        hRange = [0,len(input_array[0])-1]
    if vRange == []:
        vRange = [0,len(input_array)-1]

    if hRange[0]==None:
        hRange[1]=0   
    if hRange[1]==None:
        hRange[1]=len(input_array[0])-1
    
    if vRange[1]==None:
        vRange[1]=len(input_array)-1
    if vRange[0]==None:
        vRange[1]=0
    


    s='[{},{}] to [{},{}] revX={} revY={}'.format(
        hRange[0],hRange[1],vRange[0],vRange[1],revX,revY)
    if tight:
        print('\n{} printing tight from {}'.format(title,s))
    else:
        print('\n{} printing comma separated values from {}'.format(title,s))
    print('')
    match revY,revX:
        case False,False:     
            for x in range(vRange[0],vRange[1]+1):
                printBuffer=[]
                for y in range(hRange[0],hRange[1]+1):
                    if tight:
                        if input_array[x][y] in replace:
                            printBuffer.append(replace[input_array[x][y]])
                        else:
                            printBuffer.append(str(input_array[x][y]))
                    else:
                        printBuffer.append(input_array[x][y])
                if tight:
                    print(''.join(printBuffer))
                else:
                    print(printBuffer)
        case True,False:
            x = vRange[1]
            while(x>=vRange[0]):
                printBuffer=[]
                for y in range(hRange[0],hRange[1]+1):
                    if tight:
                        if input_array[x][y] in replace:
                            printBuffer.append(replace[input_array[x][y]])
                        else:
                            printBuffer.append(str(input_array[x][y]))
                    else:
                        printBuffer.append(input_array[x][y])
                if tight:
                    print(''.join(printBuffer))
                else:
                    print(printBuffer)
                x -= 1
        case False,True:
            for x in range(vRange[0],vRange[1]+1):
                y=hRange[1]
                printBuffer=[]
                while(y>=hRange[0]):
                    if tight:
                        if input_array[x][y] in replace:
                            printBuffer.append(replace[input_array[x][y]])
                        else:
                            printBuffer.append(str(input_array[x][y]))
                    else:
                        printBuffer.append(input_array[x][y])
                    y-=1
                if tight:
                    print(''.join(printBuffer))
                else:
                    print(printBuffer)
        case True,True:
            x = vRange[1]
            while(x>=vRange[0]):
                y=hRange[1]
                printBuffer=[]
                while(y>=hRange[0]):
                    if tight:
                        if input_array[x][y] in replace:
                            printBuffer.append(replace[input_array[x][y]])
                        else:
                            printBuffer.append(str(input_array[x][y]))
                    else:
                        printBuffer.append(input_array[x][y])
                    y-=1
                if tight:
                    print(''.join(printBuffer))
                else:
                    print(printBuffer)
                x -= 1
    return


def text2int(textnum, numwords={}):
    """
    takes input text description of number (space separated) and returns int of the number
    """
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
