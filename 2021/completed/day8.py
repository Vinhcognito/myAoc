import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from shared.helpers import Grid, Point, Vectors, get_locations, read_input
from shared.util import (
    extend_list,
    extend_list_2D,
    extend_list_rect,
    ints,
    log,
    logger_config,
    logger_enable,
    logger_init,
    print_array,
    strs,
    wait_for_input,
)

logger_init()
logger_enable(log, "day1")

DAY = 8

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")

count = 0
"""
0 = c e
6 =  de
9 = cd 

2 =  ce 
3 =  c f
5 = b  f

1 =   c f
7 = a c f
4 =  bcdf
8 = abcdefg
"""
for line in cl:
    split = line.index("|")

    signals = strs(line[:split])
    outputs = strs(line[split:])

    for word in outputs:
        if len(word) == 2 or len(word) == 3 or len(word) == 4 or len(word) == 7:
            count += 1

print(f"part1:{count}")


class SigSet:
    def __init__(self, signal: str):
        self.signal = signal
        self.n = None
        self.s = set(signal)


class Signal:
    def __init__(self, signal_strs: list[str], output_strs: list[str]):
        self.signals: list[SigSet] = []
        self.outputs: list[str] = output_strs

        for signal in signal_strs:
            self.signals.append(SigSet(signal))

        self.decode_signals()

    def get_sigset_n(self, n: int) -> SigSet:
        for sigset in self.signals:
            if getattr(sigset, "n") == n:
                return sigset

    def get_sigset_sig(self, signal: int) -> SigSet:
        for sigset in self.signals:
            if getattr(sigset, "signal") == signal:
                return sigset

    def get_sigset_set(self, signal: str) -> SigSet:
        for sigset in self.signals:
            if set(sigset.signal) == set(signal):
                return sigset

    def decode_signals(self):
        # 1 = len(2)
        # 7 = len(3)
        # 4 = len(4)
        # 8 = len(7)

        # 2,3,5 = len(5)
        # 0,6,9 = len(6)
        fives: list[SigSet] = []
        sixes: list[SigSet] = []

        for sigset in self.signals:
            match len(sigset.signal):
                case 2:
                    sigset.n = 1
                case 3:
                    sigset.n = 7
                case 4:
                    sigset.n = 4
                case 7:
                    sigset.n = 8
                case 5:
                    fives.append(sigset)
                case 6:
                    sixes.append(sigset)

        # a = s(7) - s(1)
        # *subtract a from everything except 1,4

        set_a = self.get_sigset_n(7).s - self.get_sigset_n(1).s
        a = set_a.pop()

        self.get_sigset_n(7).s.remove(a)
        self.get_sigset_n(8).s.remove(a)

        for sigset in fives:
            sigset.s.remove(a)
        for sigset in sixes:
            sigset.s.remove(a)

        common235 = fives[0].s & fives[1].s & fives[2].s
        common069 = sixes[0].s & sixes[1].s & sixes[2].s

        ####
        # 2,3,5

        # subtract common(2,3,5) from all in fives

        # s(3) - common(2,3,5) = s(1)
        for sigset in fives:
            sigset.s -= common235

        for sigset in fives:
            if sigset.s == self.get_sigset_n(1).s:
                self.get_sigset_sig(sigset.signal).n = 3
                fives.pop(fives.index(sigset))

        # subtract common(0,6,9) from all in sixes
        for sigset in sixes:
            sigset.s -= common069

        # s(2) - common(2,3,5) = s(0) - common(0,6,9)

        for unk5 in fives:
            for unk6 in sixes:
                if unk5.s == unk6.s:
                    self.get_sigset_sig(unk5.signal).n = 2
                    fives.pop(fives.index(unk5))
                    self.get_sigset_sig(unk6.signal).n = 0
                    sixes.pop(sixes.index(unk6))

        # s(5) deduced after s(2), s(3)
        s_5 = fives.pop()
        self.get_sigset_sig(s_5.signal).n = 5

        #####
        # 0,6,9
        # s(0) - common(0,6,9) = s(2) - common(2,3,5)

        # subtract s(4) from everything in sixes
        # s(9) - s(4) = nothing
        # s(6) - s(4) = e
        for sigset in sixes:
            sigset.s -= self.get_sigset_n(4).s
            if len(sigset.s) == 0:
                self.get_sigset_set(sigset.signal).n = 9
            else:
                self.get_sigset_set(sigset.signal).n = 6

    def decrypt_outputs(self) -> int:
        result = ""
        for s in self.outputs:
            for sigset in self.signals:
                if set(s) == set(sigset.signal):
                    result += str(sigset.n)

        return int(result)


signal_sum = 0

for line in cl:
    split = line.index("|")

    signal_strs = strs(line[:split])
    output_strs = strs(line[split:])
    signal = Signal(signal_strs, output_strs)
    signal_sum += signal.decrypt_outputs()

print(f"Part 2: {signal_sum}")
