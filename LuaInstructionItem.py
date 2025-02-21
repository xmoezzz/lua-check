from __future__ import print_function
from enum import Enum, IntEnum
from termcolor import colored, cprint

class LuaInstructionLevel(IntEnum):
    NORMAL = 0,
    LIKELY = 1

class LuaInstructionItem(object):
    def __init__(self, instr, level = LuaInstructionLevel.NORMAL):
        self.instr = instr
        self.level = level
    
    def Print(self):
        printx = lambda x: cprint(x, 'white', 'on_blue')
        printr = lambda x: cprint(x, 'white', 'on_yellow')
        if self.level == LuaInstructionLevel.NORMAL:
            printr(self.instr)
        else:
            printx(self.instr)
    
    def __str__(self):
        return str(self.instr)
    
    def __repr__(self):
        return str(self)

