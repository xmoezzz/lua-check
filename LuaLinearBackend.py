from __future__ import print_function
from LuaMiddleLang import *
from LuaVar import *
from termcolor import colored, cprint
from LnEnum import LuaVersion

class LuaLinearBackend(object):
    '''
    get function name
    '''
    def __init__(self, function, constants, instruction, mlils, varDefine, varUsage):
        self.function    = function
        self.instruction = instruction
        self.mlils       = mlils
        self.constants   = constants
        self.varDefine   = varDefine
        self.varUsage    = varUsage

    def _FindVarDefine(self, var):

        key = str(var)
        if key in self.varDefine:
            return self.varDefine[key]
        return None
    
    def _FindVarUsage(self, var):
        
        key = str(var)
        if key in self.varUsage:
            return self.varUsage[key]
        return []
    
    def _FindFunctionName(self, instr, var, idx):
        usage = self._FindVarUsage(var)
        if len(usage) == 0:
            #defined by CLOSURE?
            d = self._FindVarDefine(var)
            if d == None:
                raise RuntimeError('panic : variable is not defined (%s)' % var)
            return
        
        for u in usage:
            current_instr = self.mlils[u]
            if current_instr.GetOperation() == LuaMiddleOperation.NODE_SETTABUPCR:
                name = current_instr.GetDestVar().value
                self.function.subfunctions[idx].SetFunctionName(name)
                self.function.subfunctions[idx].SetFunctionType(LuaFunctionType.LUA_NORMAL)
                break
            elif current_instr.GetOperation() == LuaMiddleOperation.NODE_SETTABLECR:
                name = current_instr.GetDestVar().value
                self.function.subfunctions[idx].SetFunctionName(name)
                self.function.subfunctions[idx].SetFunctionType(LuaFunctionType.LUA_THIS)
                break
            else:
                cprint("function hash : %s" % (self.function.subfunctions[idx].hashId), 'yellow', attrs=['bold'], file=sys.stderr)
                cprint("instr : %s" % (instr), 'yellow', attrs=['bold'], file=sys.stderr)
                cprint("how to get function name here??", 'yellow', attrs=['bold'], file=sys.stderr)
    
    def AnalysisNew(self):
        for mi in self.mlils:
            if mi.GetOperation() == LuaMiddleOperation.NODE_CLOSURE:
                idx = mi.GetFunction()
                var = mi.GetDestVar()
                self._FindFunctionName(mi, var, idx)


    def _FindFunctionName51(self, instr, var, idx):
        usage = self._FindVarUsage(var)
        if len(usage) == 0:
            d = self._FindVarDefine(var)
            if d == None:
                raise RuntimeError('panic : variable is not defined (%s)' % var)
            return

        for u in usage:
            current_instr = self.mlils[u]
            if current_instr.GetOperation() == LuaMiddleOperation.NODE_MOVE:
                name = current_instr.GetDestVar()
                if not isinstance(name, LuaGlobalVal):
                    cprint("function hash : %s" % (self.function.subfunctions[idx].hashId), 'yellow', attrs=['bold'], file=sys.stderr)
                    cprint("instr : %s" % (instr), 'yellow', attrs=['bold'], file=sys.stderr)
                    cprint("how to get function name here??", 'yellow', attrs=['bold'], file=sys.stderr)
                else:
                    name = name.name
                    self.function.subfunctions[idx].SetFunctionName(name)
                    self.function.subfunctions[idx].SetFunctionType(LuaFunctionType.LUA_NORMAL)
                    break
            elif current_instr.GetOperation() == LuaMiddleOperation.NODE_SETTABLECR:
                name = current_instr.GetDestVar().value
                self.function.subfunctions[idx].SetFunctionName(name)
                self.function.subfunctions[idx].SetFunctionType(LuaFunctionType.LUA_THIS)
                break
            else:
                cprint("function hash : %s" % (self.function.subfunctions[idx].hashId), 'yellow', attrs=['bold'], file=sys.stderr)
                cprint("instr : %s" % (instr), 'yellow', attrs=['bold'], file=sys.stderr)
                cprint("how to get function name here??", 'yellow', attrs=['bold'], file=sys.stderr)
        
    def AnalysisOld(self):
        '''
        for lua 5.1 only
        '''
        for mi in self.mlils:
            if mi.GetOperation() == LuaMiddleOperation.NODE_CLOSURE:
                idx = mi.GetFunction()
                var = mi.GetDestVar()
                self._FindFunctionName51(mi, var, idx)
    
    def Analysis(self, version):
        if version == LuaVersion.LuaVersion51:
            return self.AnalysisOld()
        
        return self.AnalysisNew()