from __future__ import print_function
from Visitor import Visitor
from LuaMiddleLang import *
from LuaVar import *
from LuaTaint import is_taint_source, is_tfor_call
from LuaInstructionItem import *

class TaintFinishEvent(Exception):
    pass

class TaintException(Exception):
    pass

class LuaModeler(Visitor):
    def __init__(self, function, current_instr, instructions, mlils, constants, varDefine, varUsage):
        super(LuaModeler, self).__init__()

        self.function = function
        self.instructions = instructions
        self.mlils     = mlils
        self.constants = constants
        self.varDefine = varDefine
        self.varUsage  = varUsage
        self.current_instr = current_instr
        self.tainted   = False

        if current_instr.GetOperation() not in (
            LuaMiddleOperation.NODE_CALLI,
            LuaMiddleOperation.NODE_CALLN,
            LuaMiddleOperation.NODE_CALLT
            ):
            raise TypeError('current node must be call node')
    
    def FindVarDefine(self, var):
        key = str(var)
        if key in self.varDefine:
            return self.varDefine[key]
        return None
    
    def FindVarUsage(self, var):
        key = str(var)
        if key in self.varUsage:
            return self.varUsage[key]
        return None
    
    def visit_CONCAT(self, instr):
        srclist = instr.GetSrcVal()
        for src in srclist:
            if isinstance(src, LuaVar):
                idx = self.FindVarDefine(src)
                if idx == None:
                    raise RuntimeError('unable to find var [%s] defination' % (src))
                self.visit(self.mlils[idx])
            elif isinstance(src, LuaConstVar):
                return
            else:
                raise NotImplementedError('current var type : %s' % (type(src)))
    
    def visit_TFORCALL(self, instr):
        tab = instr.GetFunctionArg2Var()
        var_def = self.FindVarDefine(tab)
        if var_def == None:
            return
        
        next_instr = self.mlils[var_def]
        if next_instr.GetOperation() not in (
            LuaMiddleOperation.NODE_CALLI,
            LuaMiddleOperation.NODE_CALLN,
            LuaMiddleOperation.NODE_CALLT,
            LuaMiddleOperation.NODE_CALLU
            ):
            return
        
        if next_instr.GetOperation() in (
            LuaMiddleOperation.NODE_CALLI,
            LuaMiddleOperation.NODE_CALLN,
            LuaMiddleOperation.NODE_CALLT
            ):
            name = next_instr.GetName()
            if is_tfor_call(name) == None:
                print('name : %s not defined' % name)
                return
            param = next_instr.GetParam()
            if len(param) == 0:
                print('No param??')
                return
            arg0 = param[0]
            arg0_def = self.FindVarDefine(arg0)
            if arg0_def == None:
                raise RuntimeError('unable to find var [%s] defination' % (arg0))
            return self.visit(self.mlils[arg0_def])
    
    def visit_GETTABLEC(self, instr):
        #who will put something into this table?
        table = instr.GetTabVal()
        const_value = instr.GetSrcVar()
        use = self.FindVarUsage(table)
        
        if use == None or len(use) == 0:
            #nobody uses this table??
            return
        
        for u in use:
            if u == instr.GetIndex():
                continue
            else:
                print(u, instr.GetIndex())
                print(instr)
                print(self.mlils[u])
                #raise NotImplementedError('GETTABLEC -> %s' % self.mlils[u].GetOperation())
        
        
    
    def visit_MOVE(self, instr):
        src = instr.GetSrcVar()
        if isinstance(src, LuaVar):
            idx = self.FindVarDefine(src)
            if idx == None:
                raise RuntimeError('unable to find var [%s] defination' % (src))
            self.visit(self.mlils[idx])
        elif isinstance(src, LuaConstVar):
            print('const value...')
            return
        elif isinstance(src, LuaGlobalVal):
            idx = self.FindVarDefine(src)
            if idx == None:
                if src.version == 0:
                    #comes from other files?
                    self.replaceCurrentLevel(LuaInstructionLevel.LIKELY)
                    self.tainted = True
                    raise TaintFinishEvent()
                else:
                    raise RuntimeError('unable to find var [%s] defination' % (src))
            else:
                return self.visit(self.mlils[idx])
        else:
            raise NotImplementedError('current var type : %s' % (type(src)))
    
    @staticmethod
    def compare_const(a, b):
        if not isinstance(a, LuaConstVar):
            raise TypeError('type of a must be LuaConstVar (%s)' % type(a))
        if not isinstance(b, LuaConstVar):
            raise TypeError('type of b must be LuaConstVar (%s)' % type(b))
        return a.const_type == b.const_type and a.value == b.value
    
    def visit_GETTABUPC(self, instr):
        ref = self.FindVarUsage(instr.GetUpVal())
        varName = instr.GetSrcVar()
        
        if ref is None:
            raise RuntimeError('no reference for current upval : %s' % instr)
        
        for r in ref:
            #find out setter
            i  = self.mlils[r]
            op = i.GetOperation()
            if op == LuaMiddleOperation.NODE_SETTABUPCC:
                #comes from constant, ignore
                continue
            elif op == LuaMiddleOperation.NODE_SETTABUPCR:
                c = i.GetDestVar()
                if LuaModeler.compare_const(varName, c):
                    src = i.GetSrcVar()
                    src_def = self.FindVarDefine(src)
                    if src_def == None:
                        raise RuntimeError('unable to find var [%s] defination' % (src))
                    self.visit(self.mlils[src_def])
            elif op == LuaMiddleOperation.NODE_SETTABUPRC:
                #comes from constant, ignore
                continue
            elif op == LuaMiddleOperation.NODE_SETTABUPRR:
                src = i.GetSrcVar()
                dst = i.GetDestVar()
                print(i)
                raw_input()
            elif op == LuaMiddleOperation.NODE_GETTABUPC:
                if r == instr.GetIndex():
                    continue
                c = i.GetSrcVar()
                if LuaModeler.compare_const(varName, c):
                    dst = i.GetDestVar()
                    current_use = self.FindVarUsage(dst)
                    for u in current_use:
                        self.visit(self.mlils[u])
            '''
            elif op == LuaMiddleOperation.NODE_GETTABUPC:
                dst = i.GetDestVar()
                c   = i.GetSrcVar()
                if LuaModeler.compare_const(varName, c):
                    src = i.GetDestVar()
                    src_usage = self.FindVarUsage(src)
                    if src_usage == None:
                        raise RuntimeError('unable to find var [%s] usage' % (src))
                    for u in src_usage:
                        print(i)
                        print(self.function.hashId)
                        raw_input()
                        #self.visit(self.mlils[u])
            '''
        #still don't know the upval source
    
    def visit_SETTABLECC(self, instr):
        print('const value...')
        return
    
    def visit_SETTABLERR(self, instr):
        src = instr.GetSrcVar()
        src_def = self.FindVarDefine(src)
        if src_def == None:
            raise RuntimeError('unable to find var [%s] defination' % (src))
        self.visit(self.mlils[src_def])

    def visit_CALLT(self, instr):
        return
    
    def visit_CALLI(self, instr):
        name = instr.GetName()
        if name != None:
            if is_taint_source(name) != None:
                #ok, found...
                self.tainted = True
                raise TaintFinishEvent()
        else:
            print('Fxxk, name is empty')

    def check(self):
        self.visited_ins.append(LuaInstructionItem(self.current_instr))
        self.addToSet(self.current_instr.GetIndex())
        param = self.current_instr.GetParam()
        if len(param) == 0:
            print('no param...')
        
        for p in param:
            if isinstance(p, LuaVar):
                idx = self.FindVarDefine(p)
                if idx == None:
                    raise RuntimeError('unable to find var [%s] defination' % (p))
                self.visit(self.mlils[idx])
            elif isinstance(p, LuaConstVar):
                continue
            else:
                print(p)
                raise NotImplementedError('current var type : %s' % (type(p)))
    
    def GetTaintPath(self):
        return self.visited_ins
    
    def IsTainted(self):
        try:
            self.check()
        except TaintException as e:
            print('[-] TaintException : %s' % str(e))
            return False
        except TaintFinishEvent:
            self.visited_ins.reverse()
        
        return self.tainted
    