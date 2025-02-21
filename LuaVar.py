from __future__ import print_function
import enum


class LuaConstType(enum.Enum):
    CONST_NIL  = 0,
    CONST_BOOL = 1,
    CONST_INT  = 2,
    CONST_NUM  = 3,
    CONST_STR  = 4

class LuaFunctionType(enum.Enum):
    LUA_NORMAL = 0,
    LUA_THIS   = 1

class LuaConstVar(object):
    def __init__(self, var, var_type):
        self.var  = var
        self.type = var_type
    
    @property
    def value(self):
        return self.var
    
    @property
    def const_type(self):
        return self.type
    
    def __str__(self):
        #zhuan yi zi fu
        if self.var is None:
            return 'nil'
        return str(self.var)
    
    def __repr__(self):
        if self.var is None:
            return 'nil'
        return str(self.var)

class LuaVar(object):
    def __init__(self, name, version):
        self.name     = name
        self.version  = version
    
    def __str__(self):
        return '%s#%d' % (self.name, self.version)
    
    def __repr__(self):
        return '%s#%d' % (self.name, self.version)

class LuaVararg(object):
    def __init__(self, version = 0):
        self.version = version
    
    def __str__(self):
        return '__lua_vararg_%d' % (self.version)
    
    def __repr__(self):
        return '__lua_vararg_%d' % (self.version)


class LuaUpVal(object):
    def __init__(self, idx, instack, version, symbol = None):
        self.idx     = idx
        self.instack = instack
        self.symbol  = symbol
        self.version = version
    
    def __str__(self):
        tag = 0
        if self.instack:
            tag = 1
        
        if self.symbol != None:
            return 'upval_%s_%d_%d#%d' % (self.symbol, self.idx, tag, self.version)
        
        return 'upval_?_%d_%d#%d' % (self.idx, tag, self.version)
    
    def __repr__(self):
        return str(self)

class LuaGlobalVal(object):
    def __init__(self, name, version):
        self.name    = name
        self.version = version
    
    def __str__(self):
        return '@G@_%s#%d' % (self.name, self.version)
    
    def __repr__(self):
        return str(self)

def MakeSSAVar(name, version):
    var = LuaVar(name, version)
    return var

def MakeSSAGlobalVar(name, version):
    var = LuaGlobalVal(name, version)
    return var