from __future__ import print_function
from LuaInstructionItem import *

class Visitor(object):
    def __init__(self):
        self.visited_ins = list()
        self.visited_set = set()
    
    def replaceCurrentLevel(self, level):
        if len(self.visited_ins) == 0:
            return
        
        self.visited_ins[len(self.visited_ins) - 1].level = level
    
    def addToSet(self, idx):
        self.visited_set.add(idx)

    def visit(self, instr):
        method_name = 'visit_{}'.format(instr.GetOpCode())
        idx = instr.GetIndex()
        if idx in self.visited_set:
            print('--------------')
            print('visited node : %d' % idx)
            print('%s' % self.visited_ins[idx])
            print('--------------')
            return None
        self.visited_set.add(idx)
        self.visited_ins.append(LuaInstructionItem(instr))
        print(method_name)
        if hasattr(self, method_name):
            value = getattr(self, method_name)(instr)
        else:
            print('no attr :', method_name)
            value = None
        return value