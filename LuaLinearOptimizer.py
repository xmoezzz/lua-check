from __future__ import print_function
from LuaMiddleLang import *
from termcolor import colored, cprint
from LnEnum import LuaVersion
from LuaVar import LuaGlobalVal

class LuaLinearOptimizer(object):
    '''
    only try to find callinfos...
    '''
    def __init__(self, function, constants, instructions, mlils, var_define, var_usage):
        self.function = function
        self.constants= constants
        self.instructions = instructions
        self.mlils = mlils
        self.var_define = var_define
        self.var_usage  = var_usage
    
    def _FindVarAssignment(self, offset, reg):
        if offset < 0:
            raise ValueError('offset is negative value')
        
        while offset >= 0:
            #instr = offset.
            offset -= 1
        
        return None
    
    def _TraceVarComeFrom(self, offset, reg):
        '''
        outdated
        return :
        bool : find result
        int  : offset
        str  : const
        int  : next var
        '''
        pos = offset
        while pos >= 0:
            instr = self.instructions[pos]
            if instr.GetOpCode() in (
                'GETTABLE',
                'SELF',
                'GETTABUP'
                ):
                if instr.A == reg:
                    const_var = None
                    next_var  = None
                    if instr.GetOpCode() == 'GETTABLE':
                        next_var = instr.B
                        if instr.CConstMode:
                            const_var = self.constants[instr.C]
                        else:
                            if offset - 1 < 0:
                                raise RuntimeError('GETTABLE : unable to solve register')
                            #const_var = self._FindVarAssignment(offset - 1, instr.C)
                            cprint("GETTABLE, C comes from register", 'red', attrs=['bold'], file=sys.stderr)
                            return False, None, None, None
                    elif instr.GetOpCode() == 'SELF':
                        pass
                    return True, pos, const_var, next_var
            pos -= 1
        
        return False, None, None, None
    
    def _FindVarDefine(self, var):

        key = str(var)
        if key in self.var_define:
            return self.var_define[key]
        return None
    

    
    def _TraceOffset(self, mi):
        func_ssa = mi.GetFunctionVar()
        next_offset = self._FindVarDefine(func_ssa)
        if next_offset == None:
            raise RuntimeError('panic : var [%s] is not defined' % str(func_ssa))
        #print(mi)
        #print (next_offset)
        #print(self.mlils[next_offset])

        next_instr = self.mlils[next_offset]
        next_var   = None
        cur_const  = None
        
        if next_instr.GetOperation() == LuaMiddleOperation.NODE_GETTABLEC:
            next_var   = next_instr.GetTabVal()
            cur_const  = next_instr.GetSrcVar().value
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_GETTABLER:
            next_var   = next_instr.GetTabVal()
            cur_var    = next_instr.GetSrcVar()
            cprint("NODE_GETTABLER", 'red', attrs=['bold'], file=sys.stderr)
            return False, None, None, None
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_SELFC:
            next_var   = next_instr.GetSrcVar()
            cur_const  = next_instr.GetKeyVar().value
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_SELFR:
            next_var   = next_instr.GetSrcVar()
            cur_var    = next_instr.GetKeyVar()
            cprint("NODE_SELFR", 'red', attrs=['bold'], file=sys.stderr)
            return False, None, None, None
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_GETTABUPC:
            next_var   = None
            cur_const  = next_instr.GetSrcVar().value
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_GETTABUPR:
            next_var   = None
            cur_var    = next_instr.GetSrcVar()
            cprint("NODE_GETTABUPR", 'red', attrs=['bold'], file=sys.stderr)
            return False, None, None, None
        #elif next_instr.GetOperation() == LuaMiddleOperation.NODE_MOVE:
        else:
            message = 'error opcode : %s' % (next_instr.GetOperation())
            cprint(message, 'red', attrs=['bold'], file=sys.stderr)
            return False, None, None, None
        return True, next_instr, cur_const, next_var
    
    def _ReplaceWithNormalCall(self, mi, name):
        address = mi.GetAddress()
        if address == None:
            raise RuntimeError('address is none')
        index = mi.GetIndex()
        if index == None:
            raise RuntimeError('index is none')
        if self.mlils[index] != mi:
            raise RuntimeError('current node is not equal to the node in array')
        if not isinstance(name, str):
            raise TypeError('type of name must be str')
        
        node = CallNMiddleInstruction()
        node.SetName(name)
        node.SetReturn(mi.GetReturn())
        node.SetFunctionVar(mi.GetFunctionVar())
        node.SetParam(mi.GetParam())
        node.SetIndex(index)
        node.SetAddress(mi.GetAddress())
        
        self.mlils[index] = node
        self.instructions[address].SetMlil(node)
    
    def _ReplaceWithThisCall(self, mi, name):
        address = mi.GetAddress()
        if address == None:
            raise RuntimeError('address is none')
        index = mi.GetIndex()
        if index == None:
            raise RuntimeError('index is none')
        if self.mlils[index] != mi:
            raise RuntimeError('current node is not equal to the node in array')
        if not isinstance(name, str):
            raise TypeError('type of name must be str')
        
        node = CallTMiddleInstruction()
        node.SetName(name)
        node.SetReturn(mi.GetReturn())
        node.SetFunctionVar(mi.GetFunctionVar())
        node.SetParam(mi.GetParam())
        node.SetIndex(index)
        node.SetAddress(mi.GetAddress())
        
        self.mlils[index] = node
        self.instructions[address].SetMlil(node)
    
    def _ReplaceWithImportedCall(self, mi, name):
        address = mi.GetAddress()
        if address == None:
            raise RuntimeError('address is none')
        index = mi.GetIndex()
        if index == None:
            raise RuntimeError('index is none')
        if self.mlils[index] != mi:
            raise RuntimeError('current node is not equal to the node in array')
        if not isinstance(name, str):
            raise TypeError('type of name must be str')
        
        node = CallIMiddleInstruction()
        node.SetName(name)
        node.SetReturn(mi.GetReturn())
        node.SetFunctionVar(mi.GetFunctionVar())
        node.SetParam(mi.GetParam())
        node.SetIndex(index)
        node.SetAddress(mi.GetAddress())
        
        self.mlils[index] = node
        self.instructions[address].SetMlil(node)
    
    def _SolveVarChain(self, mi, var, namelist, level):
        if level >= 200:
            cprint("level >= 200", 'red', attrs=['bold'], file=sys.stderr)
            return False
        
        if mi.GetOperation() not in (
            LuaMiddleOperation.NODE_GETTABLEC,
            LuaMiddleOperation.NODE_GETTABLER,
            LuaMiddleOperation.NODE_GETTABUPC,
            LuaMiddleOperation.NODE_GETTABUPR
            ):
            return False
        
        if mi.GetOperation() == LuaMiddleOperation.NODE_GETTABLEC:
            next_var   = mi.GetTabVal()
            cur_const  = mi.GetSrcVar().value
            next_index = self._FindVarDefine(next_var)
            if next_index == None:
                raise RuntimeError('panic : var [%s] is not defined' % str(next_var))
            
            next_instr = self.mlils[next_index]
            level += 1
            namelist.append(cur_const)
            return self._SolveVarChain(next_instr, next_var, namelist, level)

        elif mi.GetOperation() == LuaMiddleOperation.NODE_GETTABUPC:
            cur_const = mi.GetSrcVar().value
            namelist.append(cur_const)
            return True
        
        return False
    
    def OptimizateNew(self):
        for mi in self.mlils:
            if mi.GetOperation() == LuaMiddleOperation.NODE_CALLU:
                address = mi.GetAddress()
                if address == None:
                    raise RuntimeError('panic : address is None')
                if address == 0:
                    raise RuntimeError('panic : address == 0')
                success, next_instr, cur_const, next_var = self._TraceOffset(mi)
                if success == False:
                    continue
                else:
                    if next_instr.GetOperation() in (
                        LuaMiddleOperation.NODE_GETTABUPC,
                        LuaMiddleOperation.NODE_GETTABUPR
                        ):
                        #CALLN, already reach the domination node
                        self._ReplaceWithNormalCall(mi, cur_const)
                        message = 'solved : normal function -> [%s]' % cur_const
                        cprint(message, 'green', attrs=['bold'], file=sys.stderr)
                    elif next_instr.GetOperation() in (
                        LuaMiddleOperation.NODE_SELFC,
                        LuaMiddleOperation.NODE_SELFR
                        ):
                        #CALLT, already reach the domination node
                        self._ReplaceWithThisCall(mi, cur_const)
                        message = 'solved : class method function -> [%s]' % cur_const
                        cprint(message, 'green', attrs=['bold'], file=sys.stderr)
                    else:
                        #only can be imported function (eg : os.execute)
                        namelist = []
                        level    = 0
                        result = self._SolveVarChain(next_instr, next_var, namelist, level)
                        if result:
                            if len(namelist) == 0:
                                raise RuntimeError('namelist is empty')
                            namelist.reverse()
                            name = '.'.join(namelist)
                            self._ReplaceWithImportedCall(mi, name)
    

    def _SolveVarChain51(self, mi, var, namelist, level):
        if level >= 200:
            cprint("level >= 200", 'red', attrs=['bold'], file=sys.stderr)
            return False
        
        #NODE_GETGLOBAL
        if mi.GetOperation() not in (
            LuaMiddleOperation.NODE_MOVE,
            LuaMiddleOperation.NODE_GETTABLEC,
            LuaMiddleOperation.NODE_GETTABLER
            ):
            print('invalid op : %s' % mi.GetOperation())
            return False
        
        if mi.GetOperation() == LuaMiddleOperation.NODE_GETTABLEC:
            next_var   = mi.GetTabVal()
            cur_const  = mi.GetSrcVar().value
            next_index = self._FindVarDefine(next_var)
            if next_index == None:
                raise RuntimeError('panic : var [%s] is not defined' % str(next_var))
            
            next_instr = self.mlils[next_index]
            level += 1
            namelist.append(cur_const)
            return self._SolveVarChain51(next_instr, next_var, namelist, level)
        
        #NODE_GETGLOBAL
        elif mi.GetOperation() == LuaMiddleOperation.NODE_MOVE:
            cur_const = mi.GetSrcVar()
            if not isinstance(cur_const, LuaGlobalVal):
                return False
            cur_const = cur_const.name.value
            namelist.append(cur_const)
            return True
        
        return False

    def _TraceOffset51(self, mi):
        func_ssa = mi.GetFunctionVar()
        next_offset = self._FindVarDefine(func_ssa)
        if next_offset == None:
            raise RuntimeError('panic : var [%s] is not defined' % str(func_ssa))
        #print(mi)
        #print (next_offset)
        #print(self.mlils[next_offset])

        next_instr = self.mlils[next_offset]
        next_var   = None
        cur_const  = None
        
        if next_instr.GetOperation() == LuaMiddleOperation.NODE_GETTABLEC:
            next_var   = next_instr.GetTabVal()
            cur_const  = next_instr.GetSrcVar().value
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_GETTABLER:
            next_var   = next_instr.GetTabVal()
            cur_var    = next_instr.GetSrcVar()
            cprint("NODE_GETTABLER", 'red', attrs=['bold'], file=sys.stderr)
            return False, None, None, None
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_SELFC:
            next_var   = next_instr.GetSrcVar()
            cur_const  = next_instr.GetKeyVar().value
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_SELFR:
            next_var   = next_instr.GetSrcVar()
            cur_var    = next_instr.GetKeyVar()
            cprint("NODE_SELFR", 'red', attrs=['bold'], file=sys.stderr)
            return False, None, None, None
        
        #NODE_GETGLOBAL
        elif next_instr.GetOperation() == LuaMiddleOperation.NODE_MOVE:
            next_var   = None
            cur_const  = next_instr.GetSrcVar()
            if not isinstance(cur_const, LuaGlobalVal):
                return False, None, None, None
            cur_const = cur_const.name.value
        #elif next_instr.GetOperation() == LuaMiddleOperation.NODE_MOVE:
        else:
            message = 'error opcode : %s' % (next_instr.GetOperation())
            cprint(message, 'red', attrs=['bold'], file=sys.stderr)
            return False, None, None, None
        return True, next_instr, cur_const, next_var


    def OptimizateOld(self):
        '''
        lua 5.1 only
        '''
        for mi in self.mlils:
            if mi.GetOperation() == LuaMiddleOperation.NODE_CALLU:
                address = mi.GetAddress()
                if address == None:
                    raise RuntimeError('panic : address is None')
                if address == 0:
                    raise RuntimeError('panic : address == 0')
                success, next_instr, cur_const, next_var = self._TraceOffset51(mi)
                if success == False:
                    continue
                else:
                    #NODE_GETGLOBAL
                    if next_instr.GetOperation() == LuaMiddleOperation.NODE_MOVE:
                        #CALLN, already reach the domination node
                        self._ReplaceWithNormalCall(mi, cur_const)
                        message = 'solved : normal function -> [%s]' % cur_const
                        cprint(message, 'green', attrs=['bold'], file=sys.stderr)
                    elif next_instr.GetOperation() in (
                        LuaMiddleOperation.NODE_SELFC,
                        LuaMiddleOperation.NODE_SELFR
                        ):
                        #CALLT, already reach the domination node
                        self._ReplaceWithThisCall(mi, cur_const)
                        message = 'solved : class method function -> [%s]' % cur_const
                        cprint(message, 'green', attrs=['bold'], file=sys.stderr)
                    else:
                        #only can be imported function (eg : os.execute)
                        namelist = []
                        level    = 0
                        result = self._SolveVarChain51(next_instr, next_var, namelist, level)
                        if result:
                            if len(namelist) == 0:
                                raise RuntimeError('namelist is empty')
                            namelist.reverse()
                            name = '.'.join(namelist)
                            self._ReplaceWithImportedCall(mi, name)
    
    def Optimizate(self, version):
        if version == LuaVersion.LuaVersion51:
            return self.OptimizateOld()
        
        return self.OptimizateNew()
                            
                
                
    