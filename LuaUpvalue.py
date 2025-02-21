from __future__ import print_function
import os
import sys


class LuaUpvalue(object):
    def __init__(self):
        self._name    = ''
        self._instack = False
        self._upidx   = -1
    
    def SetName(self, name):
        self._name = name
    
    def GetName(self):
        return self._name
    
    def SetInstack(self, val):
        self._instack = val
    
    def GetInstack(self):
        return self._instack
    
    def SetUpIndex(self, idx):
        self._upidx = idx
    
    def GetUpIndex(self):
        return self._upidx
    