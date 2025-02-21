from __future__ import print_function
import os
import sys


class LuaDecompiler(object):
    def __init__(self, mlils, function):
        self.mlils    = mlils
        self.function = function
        self.statusStack    = []
        self.localAllocator = {}
    
    def _FindLocalVar(self, regIdx):
        if regIdx in self.localAllocator:
            return self.localAllocator[regIdx]
        
        name = 'var_%d' % (regIdx)
        self.localAllocator[regIdx] = name
        return name
    
    def _AllocateArgs(self, argList = []):
        for arg in argList:
            name = 'arg_%d' % (arg)
            self.localAllocator[arg] = name
    
    def Decompile(self):
        if len(self.mlils) == 0:
            return None
        
        argList = []
        for i in range(self.function.paramCount):
            argList.append(i)
        
        if len(argList):
            self._AllocateArgs(argList)
        
        