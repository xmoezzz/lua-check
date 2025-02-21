from __future__ import print_function
from LuaVar import *

class VarEngine(object):
    def __init__(self):
        self.vars = {}
    
    @staticmethod
    def var_equal(l, r):
        if not isinstance(l, LuaVar):
            raise TypeError('type of left value must be LuaVar')
        if not isinstance(r, LuaVar):
            raise TypeError('type of right value must be LuaVar')
        return l.name == r.name and l.version == r.version
    
    def Insert(self, var):
        if not isinstance(var, LuaVar):
            raise TypeError('the type of var must be LuaVar')
        key = var.name

        if key in self.vars:
            #maybe very slow, for debugging purpose
            for v in self.vars[key]:
                if VarEngine.var_equal(v, var):
                    raise RuntimeError('alreay contains var : %s' % v)
            self.vars[key].append(var)
        else:
            self.vars[key] = [var]
    
    def RaiseVersionFrom(self, var, version):
        '''
        range : [version, end]
        including version ifself
        call this before insert phi node
        '''
        if not isinstance(var, LuaVar):
            raise TypeError('the type of var must be LuaVar')
        key = var.name
        if key not in self.vars:
            return False
        for v in self.vars[key]:
            if v.version >= version:
                v.version += 1
        return True
        
        