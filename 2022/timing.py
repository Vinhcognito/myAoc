import atexit
from time import localtime,perf_counter
from functools import reduce
from enum import Enum

class Weekday(Enum):
    Mon = 0
    Tues= 1
    Wed = 2
    Thur = 3
    Fri = 4
    Sat = 5
    Sun = 6

def seconds_to_str(t):
    return "%d:%02d:%02d.%03d" % \
           reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                  [(t * 1000,), 1000, 60, 60])

def local_to_str(t):
    if t[5] < 10:
        s ='0'+str(t[5])
    else:
        s=t[5]
    return "{}-{}-{}  {}  {}:{}:{}" .format(t[0],t[1],t[2],Weekday(t[6]).name,t[3],t[4],s)

line1 ="\n"+ "-" * 50
line2 = "-" * 50

def log(s, elapsed=None):
    """
    (string, elapsed(T/F))
    """
    print(line1)
    print(s,local_to_str(localtime()))
    if elapsed:
        print("--Elapsed time:", elapsed)
    print(line2)
    print()


def endlog():
    end = perf_counter()
    elapsed = end - start
    log("Program End     ", seconds_to_str(elapsed))


def now():
    "returns time right now since start"
    now = perf_counter()
    elapsed = now - start
    print("Current time ", seconds_to_str(elapsed))


start = perf_counter()
atexit.register(endlog)
log("Program Start   ")

