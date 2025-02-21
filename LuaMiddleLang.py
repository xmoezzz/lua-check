from __future__ import print_function
import os
import sys
import enum


#lua recompiler

class LuaMiddleOperation(enum.Enum):
    NODE_MOVE        = 0
    NODE_JMPC        = 1 #jmp if condition
    NODE_GETUPVAL    = 2
    NODE_GETTABUPR   = 3
    NODE_GETTABUPC   = 4
    NODE_GETTABLER   = 5
    NODE_GETTABLEC   = 6 
    NODE_SETTABUPRR  = 7
    NODE_SETTABUPCC  = 8
    NODE_SETTABUPCR  = 9
    NODE_SETTABUPRC  = 10
    NODE_SETUPVAL    = 11
    NODE_SETTABLECC  = 12
    NODE_SETTABLERR  = 13
    NODE_SETTABLECR  = 14
    NODE_SETTABLERC  = 15
    NODE_NEWTABLE    = 16
    NODE_SELFR       = 17
    NODE_SELFC       = 18
    NODE_ADDCC       = 19
    NODE_ADDRR       = 20
    NODE_ADDCR       = 21
    NODE_ADDRC       = 22
    NODE_SUBCC       = 23
    NODE_SUBRR       = 24
    NODE_SUBCR       = 25
    NODE_SUBRC       = 26
    NODE_MULCC       = 27
    NODE_MULRR       = 28
    NODE_MULCR       = 29
    NODE_MULRC       = 30
    NODE_DIVCC       = 31
    NODE_DIVRR       = 32
    NODE_DIVCR       = 33
    NODE_DIVRC       = 34
    NODE_POWCC       = 35
    NODE_POWRR       = 36
    NODE_POWCR       = 37
    NODE_POWRC       = 38
    NODE_MODCC       = 39
    NODE_MODRR       = 40
    NODE_MODCR       = 41
    NODE_MODRC       = 42
    NODE_IDIVCC      = 43
    NODE_IDIVRR      = 44
    NODE_IDIVCR      = 45
    NODE_IDIVRC      = 46
    NODE_BANDCC      = 47
    NODE_BANDRR      = 48
    NODE_BANDCR      = 49
    NODE_BANDRC      = 50
    NODE_BORCC       = 51
    NODE_BORRR       = 52
    NODE_BORCR       = 53
    NODE_BORRC       = 54
    NODE_BXORCC      = 55
    NODE_BXORRR      = 56
    NODE_BXORCR      = 57
    NODE_BXORRC      = 58
    NODE_SHLCC       = 59
    NODE_SHLRR       = 60
    NODE_SHLCR       = 61
    NODE_SHLRC       = 62
    NODE_SHRCC       = 63
    NODE_SHRRR       = 64
    NODE_SHRCR       = 65
    NODE_SHRRC       = 66
    NODE_UNM         = 67
    NODE_NOT         = 68
    NODE_LEN         = 69
    NODE_BNOT        = 70
    NODE_CONCAT      = 71
    NODE_JMP         = 72
    NODE_EQCC        = 73
    NODE_EQRR        = 74
    NODE_EQCR        = 75
    NODE_EQRC        = 76
    NODE_LTCC        = 77
    NODE_LTRR        = 78
    NODE_LTCR        = 79
    NODE_LTRC        = 80
    NODE_LECC        = 81
    NODE_LERR        = 82
    NODE_LECR        = 83
    NODE_LERC        = 84
    NODE_TEST        = 85
    NODE_RETURN      = 86
    NODE_TFORCALL    = 87
    NODE_SETLIST     = 88
    NODE_CLOSURE     = 89
    NODE_CALLI       = 90 #call imported function
    NODE_CALLT       = 91 #thiscall
    NODE_CALLN       = 92 #call normal function
    NODE_CALLU       = 93 #unable to get function name
    NODE_PHI         = 94 #phi
    NODE_LE          = 95 #less or eq (for FORLOOP)
    NODE_NN          = 96 #not none (for TFORLOOP)
    NODE_MOVV        = 97
    NODE_CLOSE       = 98
    NODE_LOADPARAM   = 99
    

def invopstr(opcode):
    if opcode in (
        LuaMiddleOperation.NODE_EQCC, 
        LuaMiddleOperation.NODE_EQCR,
        LuaMiddleOperation.NODE_EQRC,
        LuaMiddleOperation.NODE_EQRR):
        return '~='
    elif opcode in (
        LuaMiddleOperation.NODE_LECC,
        LuaMiddleOperation.NODE_LECR,
        LuaMiddleOperation.NODE_LERC,
        LuaMiddleOperation.NODE_LERR):
        return '>'
    elif opcode in (
        LuaMiddleOperation.NODE_LTCC,
        LuaMiddleOperation.NODE_LTCR,
        LuaMiddleOperation.NODE_LTRC,
        LuaMiddleOperation.NODE_LTRR):
        return '>='
    else:
        raise RuntimeError('invopstr : invalid opcode (%s)' % str(opcode))

def opstr(opcode):
    if opcode in (
        LuaMiddleOperation.NODE_EQCC, 
        LuaMiddleOperation.NODE_EQCR,
        LuaMiddleOperation.NODE_EQRC,
        LuaMiddleOperation.NODE_EQRR):
        return '=='
    elif opcode in (
        LuaMiddleOperation.NODE_LECC,
        LuaMiddleOperation.NODE_LECR,
        LuaMiddleOperation.NODE_LERC,
        LuaMiddleOperation.NODE_LERR):
        return '<='
    elif opcode in (
        LuaMiddleOperation.NODE_LTCC,
        LuaMiddleOperation.NODE_LTCR,
        LuaMiddleOperation.NODE_LTRC,
        LuaMiddleOperation.NODE_LTRR):
        return '<'
    else:
        raise RuntimeError('opstr : invalid opcode (%s)' % str(opcode))

class MiddleBasicBlock(object):
    def __init__(self, function, address):
        self.instructions = []
        self.function     = function
        self.address      = address
        self.incoming_edges = []
        self.outgoing_edges = []
        self.phi_calced     = False
        self.processed      = False
        self.num            = None
    
    def IsPhiCalculated(self):
        return self.phi_calced
    
    def SetPhiCalculated(self):
        self.phi_calced = True
    
    def Insert(self, instr):
        self.instructions.append(instr)
    
    def Print(self):
        print('================================')
        print('current :', self)
        print('incoming edges:')
        for bb in self.incoming_edges:
            print(bb)
        print('outgoing edges:')
        for bb in self.outgoing_edges:
            print(bb)
        print('--------------------------------')
        for ins in self.instructions:
            print(ins)
        print('================================')
        


class MiddleInstructionType(enum.Enum):
    NODE_NEXT_NORMAL = 0 #following instruction is the next instruction
    NODE_NEXT_JMP    = 1 #next instruction is stored in jmp_offset
    NODE_NEXT_BRANCH = 2 #likely or unlikely

class BasicMiddleInstruction(object):
    def __init__(self, ntype, node_type):
        self._ntype = ntype

        if not isinstance(node_type, MiddleInstructionType):
            raise TypeError('type of node_type must be MiddleInstructionType(')
        
        self._node_type = node_type #only in constructor
        self._next_bb = None

        self._likely_bb    = None
        self._unlinkely_bb = None

        #ending field
        self._is_end = False #return?
        self._idx    = None
        self._address= None
        self._bb     = None
    
    def SetBasicBlock(self, bb):
        if not isinstance(bb, MiddleBasicBlock):
            raise TypeError('the type of bb must be MiddleBasicBlock')
        self._bb = bb
    
    def GetBasicBlock(self):
        return self._bb
    
    def SetIndex(self, idx):
        self._idx = idx
    
    def GetIndex(self):
        return self._idx
    
    def SetAddress(self, address):
        '''
        the address for orignal instruction
        '''
        self._address = address
    
    def GetOperation(self):
        return self._ntype

    def GetAddress(self):
        return self._address        
    
    def SetEnd(self, value):
        self._is_end = value
    
    def IsEndNode(self):
        return self._is_end == True
    
    def IsNormalNode(self):
        return self._node_type == MiddleInstructionType.NODE_NEXT_NORMAL
    
    def IsJmpNode(self):
        return self._node_type == MiddleInstructionType.NODE_NEXT_JMP
    
    def IsBranchNode(self):
        return self._node_type == MiddleInstructionType.NODE_NEXT_BRANC
    
    def GetLikelyBlock(self):
        if self._node_type != MiddleInstructionType.NODE_NEXT_BRANCH:
            raise RuntimeError('GetLikelyNode is not vaild for normal node or jmp node')
        return self._likely_bb
    
    def SetLikelyBlock(self, node):
        if self._node_type != MiddleInstructionType.NODE_NEXT_BRANCH:
            raise RuntimeError('SetLikelyNode is not vaild for normal node or jmp node')
        if not isinstance(node, MiddleBasicBlock) and node != None:
            raise RuntimeError('SetLikelyNode : node != MiddleBasicBlock')
        self._likely_bb = node
    
    def GetUnlikelyBlock(self):
        if self._node_type != MiddleInstructionType.NODE_NEXT_BRANCH:
            raise RuntimeError('GetUnlikelyNode is not vaild for normal node or jmp node')
        return self._unlinkely_bb
    
    def SetUnlikelyBlock(self, node):
        if self._node_type != MiddleInstructionType.NODE_NEXT_BRANCH:
            raise RuntimeError('SetUnlikelyNode is not vaild for normal node or jmp node')
        if not isinstance(node, MiddleBasicBlock) and node != None:
            raise RuntimeError('SetUnlikelyNode : node != MiddleBasicBlock')
        self._unlinkely_bb = node
    
    def GetJmpNode(self):
        if self._node_type != MiddleInstructionType.NODE_NEXT_JMP:
            raise RuntimeError('SetJmpNode is not vaild for normal node or branch node')
        return self._next_bb
    
    def SetJmpNode(self, node):
        if self._node_type != MiddleInstructionType.NODE_NEXT_JMP:
            raise RuntimeError('GetJmpNode is not vaild for normal node or branch node')
        if not isinstance(node, MiddleBasicBlock) and node != None:
            raise RuntimeError('SetJmpNode : node != MiddleBasicBlock')
        self._next_bb = node


class LoadParamMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(LoadParamMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LOADPARAM, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest  = None
        self.idx   = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetIndex(self, value):
        self.idx = value
    
    def GetIndex(self):
        return self.idx
    
    def GetOpCode(self):
        return 'LOADPARAM'
    
    def __str__(self):
        return 'LOADPARAM %s, %s' % (self.dest, self.idx)
    
    def __repr__(self):
        return 'LOADPARAM %s, %s' % (self.dest, self.idx)

class MoveMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(MoveMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MOVE, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest  = None
        self.src   = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetSrcVar(self, reg):
        self.src = reg

    def GetSrcVar(self):
        return self.src

    def GetOpCode(self):
        return 'MOVE'
    
    def __str__(self):
        return 'MOVE %s, %s' % (self.dest, self.src)
    
    def __repr__(self):
        return 'MOVE %s, %s' % (self.dest, self.src)


class LeMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(LeMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LE, MiddleInstructionType.NODE_NEXT_BRANCH)
        self.left  = None
        self.right = None
        self.likely_pc_offset = None
        self.unlikely_pc_offset = None
    
    def SetLikelyPCOffset(self, offset):
        self.likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self.likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self.unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self.unlikely_pc_offset
    
    def SetLeftVal(self, value):
        self.left = value
    
    def GetLeftVal(self):
        return self.left
    
    def SetRightVal(self, value):
        self.right = value
    
    def GetRightVal(self):
        return self.right

class JmpCMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(JmpCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_JMPC, MiddleInstructionType.NODE_NEXT_BRANCH)
        self.condition = None
        self.likely_pc_offset = None
        self.unlikely_pc_offset = None

    
    def SetCondition(self, bval):
        self.condition = bval
    
    def GetCondition(self):
        return self.condition
    
    def SetLikelyPCOffset(self, offset):
        self.likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self.likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self.unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self.unlikely_pc_offset
    
    def GetOpCode(self):
        return 'JMPC'
    
    def __str__(self):
        return 'JMPC %s' % (self.condition)
    
    def __repr__(self):
        return 'JMPC %s' % (self.condition)


class CloseMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(CloseMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_CLOSE, MiddleInstructionType.NODE_NEXT_NORMAL)
    
    def __str__(self):
        return 'CLOSE'
    
    def __repr__(self):
        return 'CLOSE'

'''
VARARG : (-> mov or movv instruction)
_var_cnt = None : mov Rx, arg
_var_cnt = 1    : movv Rx, arg(0)
_var_cnt > 1    : for R(a) to R(b): movv R(i), arg(i)
'''

class MovvMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(MovvMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MOVV, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.vidx = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetVarargIndex(self, value):
        self.vidx = value
    
    def GetVarargIndex(self):
        return self.vidx

    def GetOpCode(self):
        return 'MOVV'
    
    def __str__(self):
        return 'MOVV %s, (%d)' % (self.dest, self.vidx)
    
    def __repr__(self):
        return 'MOVV %s, (%d)' % (self.dest, self.vidx)

class GetUpvalMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(GetUpvalMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_GETUPVAL, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.up   = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetUpval(self, value):
        self.up = value
    
    def GetUpval(self):
        return self.up
    
    def GetOpCode(self):
        return 'GETUPVAL'
    
    def __str__(self):
        return 'GETUPVAL %s, %s' % (self.dest, self.up)


'''
R : var(register)
C : constant
'''

class GettabupRMiddleInstruction(BasicMiddleInstruction):
    '''
    R%d := U%d[Src = R/C]
    '''
    def __init__(self):
        super(GettabupRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_GETTABUPR, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.src  = None
        self.up   = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetUpVal(self, value):
        self.up = value
    
    def GetUpVal(self):
        return self.up

    def GetOpCode(self):
        return 'GETTABUPR'
    
    def __str__(self):
        return 'GETTABUPR %s, %s, %s' % (self.dest, self.up, self.src)

    def __repr__(self):
        return 'GETTABUPR %s, %s, %s' % (self.dest, self.up, self.src)


class GettabupCMiddleInstruction(BasicMiddleInstruction):
    '''
    R%d := U%d[Src = R/C]
    '''
    def __init__(self):
        super(GettabupCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_GETTABUPC, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.src  = None
        self.up   = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetUpVal(self, value):
        self.up = value
    
    def GetUpVal(self):
        return self.up
    
    def GetOpCode(self):
        return 'GETTABUPC'

    def __str__(self):
        return 'GETTABUPC %s, %s, %s' % (self.dest, self.up, self.src)

    def __repr__(self):
        return 'GETTABUPC %s, %s, %s' % (self.dest, self.up, self.src)


class GettableRMiddleInstruction(BasicMiddleInstruction):
    '''
    R%d := R%d[Src = R/C]
    '''
    def __init__(self):
        super(GettableRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_GETTABLER, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.src  = None
        self.tab  = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetTabVal(self, value):
        self.tab = value
    
    def GetTabVal(self):
        return self.tab
    
    def GetOpCode(self):
        return 'GETTABLER'
    
    def __str__(self):
        return 'GETTABLER %s, %s, %s' % (self.dest, self.tab, self.src)
    
    def __repr__(self):
        return 'GETTABLER %s, %s, %s' % (self.dest, self.tab, self.src)

class GettableCMiddleInstruction(BasicMiddleInstruction):
    '''
    R%d := R%d[Src = R/C]
    '''
    def __init__(self):
        super(GettableCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_GETTABLEC, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.src  = None
        self.tab  = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetTabVal(self, value):
        self.tab = value
    
    def GetTabVal(self):
        return self.tab
    
    def GetOpCode(self):
        return 'GETTABLEC'
    
    def __str__(self):
        return 'GETTABLEC %s, %s, %s' % (self.dest, self.tab, self.src)
    
    def __repr__(self):
        return 'GETTABLER %s, %s, %s' % (self.dest, self.tab, self.src)


class SettabupRRMiddleInstruction(BasicMiddleInstruction):
    '''
    U%d[Dest = R/C] := (Src = R/C)
    '''
    def __init__(self):
        super(SettabupRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETTABUPRR, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src  = None
        self.dest = None
        self.up   = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetUpVal(self, value):
        self.up = value
    
    def GetUpVal(self):
        return self.up
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def GetOpCode(self):
        return 'SETTABUPRR'
    
    def __str__(self):
        return 'SETTABUPRR %s, %s, %s' % (self.up, self.dest, self.src)
    
    def __repr__(self):
        return 'SETTABUPRR %s, %s, %s' % (self.up, self.dest, self.src)




class SettabupCCMiddleInstruction(BasicMiddleInstruction):
    '''
    U%d[Dest = R/C] := (Src = R/C)
    '''
    def __init__(self):
        super(SettabupCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETTABUPCC, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src  = None
        self.dest = None
        self.up   = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetUpVal(self, value):
        self.up = value
    
    def GetUpVal(self):
        return self.up
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def GetOpCode(self):
        return 'SETTABUPCC'
    
    def __str__(self):
        return 'SETTABUPCC %s, %s, %s' % (self.up, self.dest, self.src)
    
    def __repr__(self):
        return 'SETTABUPCC %s, %s, %s' % (self.up, self.dest, self.src)




class SettabupRCMiddleInstruction(BasicMiddleInstruction):
    '''
    U%d[Dest = R/C] := (Src = R/C)
    '''
    def __init__(self):
        super(SettabupRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETTABUPRC, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src  = None
        self.dest = None
        self.up   = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetUpVal(self, value):
        self.up = value
    
    def GetUpVal(self):
        return self.up
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def GetOpCode(self):
        return 'SETTABUPRC'
    
    def __str__(self):
        return 'SETTABUPRC %s, %s, %s' % (self.up, self.dest, self.src)
    
    def __repr__(self):
        return 'SETTABUPRC %s, %s, %s' % (self.up, self.dest, self.src)




class SettabupCRMiddleInstruction(BasicMiddleInstruction):
    '''
    U%d[Dest = R/C] := (Src = R/C)
    '''
    def __init__(self):
        super(SettabupCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETTABUPCR, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src  = None
        self.dest = None
        self.up   = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetUpVal(self, value):
        self.up = value
    
    def GetUpVal(self):
        return self.up
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def GetOpCode(self):
        return 'SETTABUPCR'
    
    def __str__(self):
        return 'SETTABUPCR %s, %s, %s' % (self.up, self.dest, self.src)
    
    def __repr__(self):
        return 'SETTABUPCR %s, %s, %s' % (self.up, self.dest, self.src)


class SetUpvalMiddleInstruction(BasicMiddleInstruction):
    '''
    U%d := R%d
    '''
    def __init__(self):
        super(SetUpvalMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETUPVAL, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.up  = None
        self.dst = None
    
    def SetUpVal(self, value):
        self.up = value
    
    def GetUpVal(self):
        return self.up
    
    def SetDestVar(self, value):
        self.dst = value
    
    def GetDestVar(self):
        return self.dst
    
    def GetOpCode(self):
        return 'SETUPVAL'
    
    def __str__(self):
        return 'SETUPVAL %s, %s' % (self.up, self.dst)
    
    def __repr__(self):
        return 'SETUPVAL %s, %s' % (self.up, self.dst)


class SettableCCMiddleInstruction(BasicMiddleInstruction):
    '''
    R%d[Dest = R/C] := (Src = R/C)
    '''
    def __init__(self):
        super(SettableCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETTABLECC, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.reg  = None
        self.tab  = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetTabVal(self, value):
        self.tab = value
    
    def GetTabVal(self):
        return self.tab
    
    def GetOpCode(self):
        return 'SETTABLECC'
    
    def __str__(self):
        return 'SETTABLECC %s, %s, %s' % (self.tab, self.dest, self.src)
    
    def __repr__(self):
        return 'SETTABLECC %s, %s, %s' % (self.tab, self.dest, self.src)




class SettableRRMiddleInstruction(BasicMiddleInstruction):
    '''
    R%d[Dest = R/C] := (Src = R/C)
    '''
    def __init__(self):
        super(SettableRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETTABLERR, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.reg  = None
        self.tab  = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetTabVal(self, value):
        self.tab = value
    
    def GetTabVal(self):
        return self.tab
    
    def GetOpCode(self):
        return 'SETTABLERR'
    
    def __str__(self):
        return 'SETTABLERR %s, %s, %s' % (self.tab, self.dest, self.src)
    
    def __repr__(self):
        return 'SETTABLERR %s, %s, %s' % (self.tab, self.dest, self.src)




class SettableCRMiddleInstruction(BasicMiddleInstruction):
    '''
    R%d[Dest = R/C] := (Src = R/C)
    '''
    def __init__(self):
        super(SettableCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETTABLECR, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.reg  = None
        self.tab  = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetTabVal(self, value):
        self.tab = value
    
    def GetTabVal(self):
        return self.tab
    
    def GetOpCode(self):
        return 'SETTABLECR'
    
    def __str__(self):
        return 'SETTABLECR %s, %s, %s' % (self.tab, self.dest, self.src)
    
    def __repr__(self):
        return 'SETTABLECR %s, %s, %s' % (self.tab, self.dest, self.src)


class SettableRCMiddleInstruction(BasicMiddleInstruction):
    '''
    R%d[Dest = R/C] := (Src = R/C)
    '''
    def __init__(self):
        super(SettableRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETTABLERC, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
        self.reg  = None
        self.tab  = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetTabVal(self, value):
        self.tab = value
    
    def GetTabVal(self):
        return self.tab
    
    def GetOpCode(self):
        return 'SETTABLERC'
    
    def __str__(self):
        return 'SETTABLERC %s, %s, %s' % (self.tab, self.dest, self.src)
    
    def __repr__(self):
        return 'SETTABLERC %s, %s, %s' % (self.tab, self.dest, self.src)


class NewtableMiddleInstruction(BasicMiddleInstruction):
    '''
    ignore hash size and item size?
    '''
    def __init__(self):
        super(NewtableMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_NEWTABLE, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest = None
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def GetOpCode(self):
        return 'NEWTABLE'
    
    def __str__(self):
        return 'NEWTABLE %s' % (self.dest)
    
    def __repr__(self):
        return 'NEWTABLE %s' % (self.dest)


class SelfRMiddleInstruction(BasicMiddleInstruction):
    '''
    R(A+1) := R(B); R(A) := R(B)[RK(C)]
    '''
    def __init__(self):
        super(SelfRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SELFR, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src  = None #b
        self.dest = None #a
        self.idx  = None #c
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetKeyVar(self, value):
        self.idx = value
    
    def GetKeyVar(self):
        return self.idx

    def GetOpCode(self):
        return 'SELFR'
    
    def __str__(self):
        return 'SELFR %s, %s, %s' % (self.dest, self.src, self.idx)
    
    def __repr__(self):
        return 'SELFR %s, %s, %s' % (self.dest, self.src, self.idx)



class SelfCMiddleInstruction(BasicMiddleInstruction):
    '''
    R(A+1) := R(B); R(A) := R(B)[RK(C)]
    '''
    def __init__(self):
        super(SelfCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SELFC, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src  = None #b
        self.dest = None #a
        self.key  = None #c
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetKeyVar(self, value):
        self.key = value
    
    def GetKeyVar(self):
        return self.key

    def GetOpCode(self):
        return 'SELFC'
    
    def __str__(self):
        return 'SELFC %s, %s, %s' % (self.dest, self.src, self.key)
    
    def __repr__(self):
        return 'SELFC %s, %s, %s' % (self.dest, self.src, self.key)


class MathBaseMiddleInstruction(BasicMiddleInstruction):
    '''
    R(A) := RK(B) <op> RK(C)
    '''
    def __init__(self, ntype):
        super(MathBaseMiddleInstruction, self).__init__(ntype, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.dest  = None
        self.left  = None
        self.right = None
    
    def SetDestVal(self, value):
        self.dest = value
    
    def GetDestVal(self):
        return self.dest
    
    def SetLeftVal(self, value):
        self.left = value
    
    def GetLeftVal(self):
        return self.left
    
    def SetRightVal(self, value):
        self.right = value
    
    def GetRightVal(self):
        return self.right

class AddCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) + RK(C)
    '''
    def __init__(self):
        super(AddCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_ADDCC)
    
    def GetOpCode(self):
        return 'ADDCC'
    
    def __str__(self):
        return 'ADDCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'ADDCC %s, %s, %s' % (self.dest, self.left, self.right)


class AddRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) + RK(C)
    '''
    def __init__(self):
        super(AddRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_ADDRR)
    
    def GetOpCode(self):
        return 'ADDRR'
    
    def __str__(self):
        return 'ADDRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'ADDRR %s, %s, %s' % (self.dest, self.left, self.right)


class AddRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) + RK(C)
    '''
    def __init__(self):
        super(AddRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_ADDRC)
    
    def GetOpCode(self):
        return 'ADDRC'
    
    def __str__(self):
        return 'ADDRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'ADDRC %s, %s, %s' % (self.dest, self.left, self.right)

class AddCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) + RK(C)
    '''
    def __init__(self):
        super(AddCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_ADDCR)
    
    def GetOpCode(self):
        return 'ADDCR'
    
    def __str__(self):
        return 'ADDCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'ADDCR %s, %s, %s' % (self.dest, self.left, self.right)

class SubCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) - RK(C)
    '''
    def __init__(self):
        super(SubCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SUBCC)

    def GetOpCode(self):
        return 'SUBCC'
    
    def __str__(self):
        return 'SUBCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SUBCC %s, %s, %s' % (self.dest, self.left, self.right)

class SubRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) - RK(C)
    '''
    def __init__(self):
        super(SubRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SUBRR)

    def GetOpCode(self):
        return 'SUBRR'
    
    def __str__(self):
        return 'SUBRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SUBRR %s, %s, %s' % (self.dest, self.left, self.right)

class SubCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) - RK(C)
    '''
    def __init__(self):
        super(SubCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SUBCR)

    def GetOpCode(self):
        return 'SUBCR'
    
    def __str__(self):
        return 'SUBCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SUBCR %s, %s, %s' % (self.dest, self.left, self.right)


class SubRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) - RK(C)
    '''
    def __init__(self):
        super(SubRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SUBRC)

    def GetOpCode(self):
        return 'SUBRC'
    
    def __str__(self):
        return 'SUBRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SUBRC %s, %s, %s' % (self.dest, self.left, self.right)

class MulCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) * RK(C)
    '''
    def __init__(self):
        super(MulCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MULCC)
    
    def GetOpCode(self):
        return 'MULCC'

    def __str__(self):
        return 'MULCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'MULCC %s, %s, %s' % (self.dest, self.left, self.right)


class MulRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) * RK(C)
    '''
    def __init__(self):
        super(MulRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MULRR)
    
    def GetOpCode(self):
        return 'MULRR'

    def __str__(self):
        return 'MULRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'MULRR %s, %s, %s' % (self.dest, self.left, self.right)


class MulCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) * RK(C)
    '''
    def __init__(self):
        super(MulCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MULCR)
    
    def GetOpCode(self):
        return 'MULCR'

    def __str__(self):
        return 'MULCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'MULCR %s, %s, %s' % (self.dest, self.left, self.right)

class MulRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) * RK(C)
    '''
    def __init__(self):
        super(MulRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MULRC)
    
    def GetOpCode(self):
        return 'MULRC'

    def __str__(self):
        return 'MULRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'MULRC %s, %s, %s' % (self.dest, self.left, self.right)


class DivCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) / RK(C)
    '''
    def __init__(self):
        super(DivCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_DIVCC)
    
    def GetOpCode(self):
        return 'DIVCC'

    def __str__(self):
        return 'DIVCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'DIVCC %s, %s, %s' % (self.dest, self.left, self.right)



class DivRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) / RK(C)
    '''
    def __init__(self):
        super(DivRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_DIVRR)
    
    def GetOpCode(self):
        return 'DIVRR'

    def __str__(self):
        return 'DIVRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'DIVRR %s, %s, %s' % (self.dest, self.left, self.right)


class DivCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) / RK(C)
    '''
    def __init__(self):
        super(DivCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_DIVCR)
    
    def GetOpCode(self):
        return 'DIVCR'

    def __str__(self):
        return 'DIVCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'DIVCR %s, %s, %s' % (self.dest, self.left, self.right)


class DivRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) / RK(C)
    '''
    def __init__(self):
        super(DivRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_DIVRC)
    
    def GetOpCode(self):
        return 'DIVRC'

    def __str__(self):
        return 'DIVRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'DIVRC %s, %s, %s' % (self.dest, self.left, self.right)

class PowCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(PowCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_POWCC)
    
    def GetOpCode(self):
        return 'POWCC'
    
    def __str__(self):
        return 'POWCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'POWCC %s, %s, %s' % (self.dest, self.left, self.right)


class PowRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(PowRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_POWRR)
    
    def GetOpCode(self):
        return 'POWRR'
    
    def __str__(self):
        return 'POWRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'POWRR %s, %s, %s' % (self.dest, self.left, self.right)


class PowCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(PowCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_POWCR)
    
    def GetOpCode(self):
        return 'POWCR'
    
    def __str__(self):
        return 'POWCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'POWCR %s, %s, %s' % (self.dest, self.left, self.right)


class PowRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(PowRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_POWRC)
    
    def GetOpCode(self):
        return 'POWRC'
    
    def __str__(self):
        return 'POWRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'POWRC %s, %s, %s' % (self.dest, self.left, self.right)

class ModCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(ModCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MODCC)
    
    def GetOpCode(self):
        return 'MODCC'
    
    def __str__(self):
        return 'MODCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'MODCC %s, %s, %s' % (self.dest, self.left, self.right)


class ModRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(ModRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MODRR)
    
    def GetOpCode(self):
        return 'MODRR'
    
    def __str__(self):
        return 'MODRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'MODRR %s, %s, %s' % (self.dest, self.left, self.right)

class ModRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(ModRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MODRC)
    
    def GetOpCode(self):
        return 'MODRC'
    
    def __str__(self):
        return 'MODRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'MODRC %s, %s, %s' % (self.dest, self.left, self.right)

class ModCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(ModCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_MODCR)
    
    def GetOpCode(self):
        return 'MODCR'
    
    def __str__(self):
        return 'MODCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'MODCR %s, %s, %s' % (self.dest, self.left, self.right)

class IdivCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) // RK(C)
    '''
    def __init__(self):
        super(IdivCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_IDIVCC)
    
    def GetOpCode(self):
        return 'IDIVCC'
    
    def __str__(self):
        return 'IDIVCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'IDIVCC %s, %s, %s' % (self.dest, self.left, self.right)


class IdivRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) // RK(C)
    '''
    def __init__(self):
        super(IdivRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_IDIVRR)
    
    def GetOpCode(self):
        return 'IDIVRR'
    
    def __str__(self):
        return 'IDIVRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'IDIVRR %s, %s, %s' % (self.dest, self.left, self.right)


class IdivCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) // RK(C)
    '''
    def __init__(self):
        super(IdivCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_IDIVCR)
    
    def GetOpCode(self):
        return 'IDIVCR'
    
    def __str__(self):
        return 'IDIVCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'IDIVCR %s, %s, %s' % (self.dest, self.left, self.right)

class IdivRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) // RK(C)
    '''
    def __init__(self):
        super(IdivRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_IDIVRC)
    
    def GetOpCode(self):
        return 'IDIVRC'
    
    def __str__(self):
        return 'IDIVRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'IDIVRC %s, %s, %s' % (self.dest, self.left, self.right)

class BandCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) & RK(C)
    '''
    def __init__(self):
        super(BandCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BANDCC)
    
    def GetOpCode(self):
        return 'BANDCC'
    
    def __str__(self):
        return 'BANDCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BANDCC %s, %s, %s' % (self.dest, self.left, self.right)


class BandRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) & RK(C)
    '''
    def __init__(self):
        super(BandRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BANDRR)
    
    def GetOpCode(self):
        return 'BANDRR'
    
    def __str__(self):
        return 'BANDRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BANDRR %s, %s, %s' % (self.dest, self.left, self.right)

class BandCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) & RK(C)
    '''
    def __init__(self):
        super(BandCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BANDCR)
    
    def GetOpCode(self):
        return 'BANDCR'
    
    def __str__(self):
        return 'BANDCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BANDCR %s, %s, %s' % (self.dest, self.left, self.right)


class BandRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) & RK(C)
    '''
    def __init__(self):
        super(BandRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BANDRC)
    
    def GetOpCode(self):
        return 'BANDRC'
    
    def __str__(self):
        return 'BANDRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BANDRC %s, %s, %s' % (self.dest, self.left, self.right)

class BorCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) | RK(C)
    '''
    def __init__(self):
        super(BorCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BORCC)
    
    def GetOpCode(self):
        return 'BORCC'

    def __str__(self):
        return 'BORCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BORCC %s, %s, %s' % (self.dest, self.left, self.right)

class BorRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) | RK(C)
    '''
    def __init__(self):
        super(BorRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BORRR)
    
    def GetOpCode(self):
        return 'BORRR'

    def __str__(self):
        return 'BORRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BORRR %s, %s, %s' % (self.dest, self.left, self.right)

class BorCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) | RK(C)
    '''
    def __init__(self):
        super(BorCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BORCR)
    
    def GetOpCode(self):
        return 'BORCR'

    def __str__(self):
        return 'BORCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BORCR %s, %s, %s' % (self.dest, self.left, self.right)


class BorRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) | RK(C)
    '''
    def __init__(self):
        super(BorRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BORRC)
    
    def GetOpCode(self):
        return 'BORRC'

    def __str__(self):
        return 'BORRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BORRC %s, %s, %s' % (self.dest, self.left, self.right)

class BxorCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) ~ RK(C)
    '''
    def __init__(self):
        super(BxorCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BXORCC)
    
    def GetOpCode(self):
        return 'BXORCC'

    def __str__(self):
        return 'BXORCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BXORCC %s, %s, %s' % (self.dest, self.left, self.right)
    

class BxorRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) ~ RK(C)
    '''
    def __init__(self):
        super(BxorRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BXORRR)
    
    def GetOpCode(self):
        return 'BXORRR'
    
    def __str__(self):
        return 'BXORRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BXORRR %s, %s, %s' % (self.dest, self.left, self.right)


class BxorCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) ~ RK(C)
    '''
    def __init__(self):
        super(BxorCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BXORCR)
    
    def GetOpCode(self):
        return 'BXORCR'
    
    def __str__(self):
        return 'BXORCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BXORCR %s, %s, %s' % (self.dest, self.left, self.right)


class BxorRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) ~ RK(C)
    '''
    def __init__(self):
        super(BxorRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BXORRC)
    
    def GetOpCode(self):
        return 'BXORRC'
    
    def __str__(self):
        return 'BXORRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'BXORRC %s, %s, %s' % (self.dest, self.left, self.right)


class ShlCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) << RK(C)
    '''
    def __init__(self):
        super(ShlCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SHLCC)
    
    def GetOpCode(self):
        return 'SHLCC'

    def __str__(self):
        return 'SHLCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SHLCC %s, %s, %s' % (self.dest, self.left, self.right)


class ShlRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) << RK(C)
    '''
    def __init__(self):
        super(ShlRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SHLRR)
    
    def GetOpCode(self):
        return 'SHLRR'

    def __str__(self):
        return 'SHLRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SHLRR %s, %s, %s' % (self.dest, self.left, self.right)


class ShlCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) << RK(C)
    '''
    def __init__(self):
        super(ShlCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SHLCR)
    
    def GetOpCode(self):
        return 'SHLCR'

    def __str__(self):
        return 'SHLCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SHLCR %s, %s, %s' % (self.dest, self.left, self.right)


class ShlRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) << RK(C)
    '''
    def __init__(self):
        super(ShlRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SHLRC)
    
    def GetOpCode(self):
        return 'SHLRC'

    def __str__(self):
        return 'SHLRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SHLRC %s, %s, %s' % (self.dest, self.left, self.right)


class ShrCCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) >> RK(C)
    '''
    def __init__(self):
        super(ShrCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SHRCC)
    
    def GetOpCode(self):
        return 'SHRCC'
    
    def __str__(self):
        return 'SHRCC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SHRCC %s, %s, %s' % (self.dest, self.left, self.right)



class ShrRRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) >> RK(C)
    '''
    def __init__(self):
        super(ShrRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SHRRR)
    
    def GetOpCode(self):
        return 'SHRRR'
    
    def __str__(self):
        return 'SHRRR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SHRRR %s, %s, %s' % (self.dest, self.left, self.right)


class ShrCRMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) >> RK(C)
    '''
    def __init__(self):
        super(ShrCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SHRCR)
    
    def GetOpCode(self):
        return 'SHRCR'
    
    def __str__(self):
        return 'SHRCR %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SHRCR %s, %s, %s' % (self.dest, self.left, self.right)


class ShrRCMiddleInstruction(MathBaseMiddleInstruction):
    '''
    R(A) := RK(B) >> RK(C)
    '''
    def __init__(self):
        super(ShrRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SHRRC)
    
    def GetOpCode(self):
        return 'SHRRC'
    
    def __str__(self):
        return 'SHRRC %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'SHRRC %s, %s, %s' % (self.dest, self.left, self.right)

class UnaryBaseMiddleInstruction(BasicMiddleInstruction):
    def __init__(self, ntype):
        super(UnaryBaseMiddleInstruction, self).__init__(ntype, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src  = None
        self.dest = None
    
    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest

class UnmMiddleInstruction(UnaryBaseMiddleInstruction):
    '''
    R(A) := -R(B)
    '''
    def __init__(self):
        super(UnmMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_UNM)
    
    def GetOpCode(self):
        return 'UNM'
    
    def __str__(self):
        return 'UNM %s, %s' % (self.dest, self.src)
    
    def __repr__(self):
        return 'UNM %s, %s' % (self.dest, self.src)

class NotMiddleInstruction(UnaryBaseMiddleInstruction):
    '''
    R(A) := not R(B)
    '''
    def __init__(self):
        super(NotMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_NOT)
    
    def GetOpCode(self):
        return 'NOT'
    
    def __str__(self):
        return 'NOT %s, %s' % (self.dest, self.src)
    
    def __repr__(self):
        return 'NOT %s, %s' % (self.dest, self.src)

class LenMiddleInstruction(UnaryBaseMiddleInstruction):
    '''
    R(A) := length of R(B)
    '''
    def __init__(self):
        super(LenMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LEN)
    
    def GetOpCode(self):
        return 'LEN'

    def __str__(self):
        return 'LEN %s, %s' % (self.dest, self.src)
    
    def __repr__(self):
        return 'LEN %s, %s' % (self.dest, self.src)

class BnotMiddleInstruction(UnaryBaseMiddleInstruction):
    '''
    R(A) := ~R(B)
    '''
    def __init__(self):
        super(BnotMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_BNOT)
    
    def GetOpCode(self):
        return 'BNOT'

    def __str__(self):
        return 'BNOT %s, %s' % (self.dest, self.src)
    
    def __repr__(self):
        return 'BNOT %s, %s' % (self.dest, self.src)


# dest += src -> unary op
class ConcatMiddleInstruction(BasicMiddleInstruction):
    '''
    R(A) := R(B).. ... ..R(C)
    '''
    def __init__(self):
        super(ConcatMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_CONCAT, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src  = None
        self.dest = None
    
    def SetSrcVal(self, value):
        self.src = value
    
    def GetSrcVal(self):
        return self.src
    
    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest
    
    def GetOpCode(self):
        return 'CONCAT'

    def __str__(self):
        src = ','.join([str(p) for p in self.src])
        return 'CONCAT %s, (%s)' % (self.dest, src)
    
    def __repr__(self):
        src = ','.join([str(p) for p in self.src])
        return 'CONCAT %s, (%s)' % (self.dest, src)


class JmpMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(JmpMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_JMP, MiddleInstructionType.NODE_NEXT_JMP)
        self.jmp_offset = None
    
    def SetJmpOffset(self, offset):
        self.jmp_offset = offset
    
    def GetJmpOffset(self):
        return self.jmp_offset
    
    def GetOpCode(self):
        return 'JMP'
    
    def __str__(self):
        return 'JMP %d' % (self.jmp_offset)

class ConditionBranchBaseMiddleInstruction(BasicMiddleInstruction):
    '''
    if ((RK(B) op RK(C)) ~= A) then pc++
    '''
    def __init__(self, ntype):
        super(ConditionBranchBaseMiddleInstruction, self).__init__(ntype, MiddleInstructionType.NODE_NEXT_BRANCH)
        self.likely_pc_offset   = None
        self.unlikely_pc_offset = None
        self.bvar = None
        self.cvar = None
        self.condition = True #or not?
    
    #c value
    def SetCondition(self, bval):
        self.condition = bval
    
    def GetCondition(self):
        return self.condition
    
    def SetLikelyPCOffset(self, offset):
        self.likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self.likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self.unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self.unlikely_pc_offset
    
    def SetBVar(self, val):
        self.bvar = val
    
    def GetBVar(self):
        return self.bvar

    def SetCVar(self, val):
        self.cvar = val
    
    def GetCVar(self):
        return self.cvar


class EqCCMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) == RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(EqCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_EQCC)
    
    def GetOpCode(self):
        return 'EQCC'
    
    def __str__(self):
        return 'EQCC %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'EQCC %s, %s, %d' % (self.bvar, self.cvar, self.condition)


class EqRRMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) == RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(EqRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_EQRR)
    
    def GetOpCode(self):
        return 'EQRR'
    
    def __str__(self):
        return 'EQRR %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'EQRR %s, %s, %d' % (self.bvar, self.cvar, self.condition)


class EqCRMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) == RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(EqCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_EQCR)
    
    def GetOpCode(self):
        return 'EQCR'
    
    def __str__(self):
        return 'EQCR %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'EQCR %s, %s, %d' % (self.bvar, self.cvar, self.condition)


class EqRCMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) == RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(EqRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_EQRC)
    
    def GetOpCode(self):
        return 'EQRC'
    
    def __str__(self):
        return 'EQRC %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'EQRC %s, %s, %d' % (self.bvar, self.cvar, self.condition)

class LtCCMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) <  RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LtCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LTCC)
    
    def GetOpCode(self):
        return 'LTCC'
    
    def __str__(self):
        return 'LTCC %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'LTCC %s, %s, %d' % (self.bvar, self.cvar, self.condition)


class LtRRMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) <  RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LtRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LTRR)
    
    def GetOpCode(self):
        return 'LTRR'

    def __str__(self):
        return 'LTRR %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'LTRR %s, %s, %d' % (self.bvar, self.cvar, self.condition)


class LtCRMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) <  RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LtCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LTCR)
    
    def GetOpCode(self):
        return 'LTCR'

    def __str__(self):
        return 'LTCR %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'LTCR %s, %s, %d' % (self.bvar, self.cvar, self.condition)


class LtRCMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) <  RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LtRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LTRC)
    
    def GetOpCode(self):
        return 'LTRC'

    def __str__(self):
        return 'LTRC %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'LTRC %s, %s, %d' % (self.bvar, self.cvar, self.condition)

class LeCCMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) <= RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LeCCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LECC)
    
    def GetOpCode(self):
        return 'LECC'
    
    def __str__(self):
        return 'LECC %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'LECC %s, %s, %d' % (self.bvar, self.cvar, self.condition)



class LeRRMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) <= RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LeRRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LERR)
    
    def GetOpCode(self):
        return 'LERR'
    
    def __str__(self):
        return 'LERR %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'LERR %s, %s, %d' % (self.bvar, self.cvar, self.condition)



class LeCRMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) <= RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LeCRMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LECR)
    
    def GetOpCode(self):
        return 'LECR'
    
    def __str__(self):
        return 'LECR %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'LECR %s, %s, %d' % (self.bvar, self.cvar, self.condition)


class LeRCMiddleInstruction(ConditionBranchBaseMiddleInstruction):
    '''
    if ((RK(B) <= RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LeRCMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_LERC)
    
    def GetOpCode(self):
        return 'LERC'
    
    def __str__(self):
        return 'LERC %s, %s, %d' % (self.bvar, self.cvar, self.condition)
    
    def __repr__(self):
        return 'LERC %s, %s, %d' % (self.bvar, self.cvar, self.condition)


class TestMiddleInstruction(BasicMiddleInstruction):
    '''
    TEST        A C     if not (R(A) <=> C) then pc++
    '''
    def __init__(self):
        super(TestMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_TEST, MiddleInstructionType.NODE_NEXT_BRANCH)
        self.likely_pc_offset   = None
        self.unlikely_pc_offset = None
        self.condition = None
        self.var       = None
    
    def SetCondition(self, bval):
        self.condition = bval
    
    def GetCondition(self):
        return self.condition
    
    def SetLikelyPCOffset(self, offset):
        self.likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self.likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self.unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self.unlikely_pc_offset
    
    def SetTestVar(self, value):
        self.var = value
    
    def GetTestVar(self):
        return self.var
    
    def GetOpCode(self):
        return 'TEST'
    
    def __str__(self):
        return 'TEST %s, %d' % (self.var, self.condition)
    
    def __repr__(self):
        return 'TEST %s, %d' % (self.var, self.condition)


class CallNMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(CallNMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_CALLN, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.func  = None
        self.ret   = []
        self.param = []
        self.name  = None
    
    def SetName(self, name):
        self.name = name
    
    def GetName(self):
        return self.name

    def SetFunctionVar(self, value):
        self.func = value
    
    def GetFunctionVar(self):
        return self.func
    
    def SetReturn(self, ret):
        self.ret = ret
    
    def GetReturn(self):
        return self.ret
        
    def SetParam(self, param):
        self.param = param
    
    def GetParam(self):
        return self.param

    def GetOpCode(self):
        return 'CALLN'
    
    def __str__(self):
        ret   = ','.join([str(p) for p in self.ret])
        param = ','.join([str(p) for p in self.param])
        name  = ''
        if self.name != None:
            name = ' =>[' + self.name + ']'
        return 'CALLN %s, (%s), (%s)%s' % (self.func, ret, param, name)
    
    def __repr__(self):
        ret   = ','.join([str(p) for p in self.ret])
        param = ','.join([str(p) for p in self.param])
        name  = ''
        if self.name != None:
            name = ' =>[' + self.name + ']'
        return 'CALLN %s, (%s), (%s)%s' % (self.func, ret, param, name)



class CallIMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(CallIMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_CALLI, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.func  = None
        self.ret   = []
        self.param = []
        self.name  = None
    
    def SetName(self, name):
        self.name = name
    
    def GetName(self):
        return self.name

    def SetFunctionVar(self, value):
        self.func = value
    
    def GetFunctionVar(self):
        return self.func
    
    def SetReturn(self, ret):
        self.ret = ret
    
    def GetReturn(self):
        return self.ret
        
    def SetParam(self, param):
        self.param = param
    
    def GetParam(self):
        return self.param

    def GetOpCode(self):
        return 'CALLI'
    
    def __str__(self):
        ret   = ','.join([str(p) for p in self.ret])
        param = ','.join([str(p) for p in self.param])
        name  = ''
        if self.name != None:
            name = ' =>[' + self.name + ']'
        return 'CALLI %s, (%s), (%s)%s' % (self.func, ret, param, name)
    
    def __repr__(self):
        ret   = ','.join([str(p) for p in self.ret])
        param = ','.join([str(p) for p in self.param])
        if self.name != None:
            name = ' =>[' + self.name + ']'
        return 'CALLI %s, (%s), (%s)%s' % (self.func, ret, param, name)



class CallTMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(CallTMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_CALLT, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.func  = None
        self.ret   = []
        self.param = []
        self.name  = None
    
    def SetName(self, name):
        self.name = name
    
    def GetName(self):
        return self.name

    def SetFunctionVar(self, value):
        self.func = value
    
    def GetFunctionVar(self):
        return self.func
    
    def SetReturn(self, ret):
        self.ret = ret
    
    def GetReturn(self):
        return self.ret
        
    def SetParam(self, param):
        self.param = param
    
    def GetParam(self):
        return self.param

    def GetOpCode(self):
        return 'CALLT'
    
    def __str__(self):
        ret   = ','.join([str(p) for p in self.ret])
        param = ','.join([str(p) for p in self.param])
        name  = ''
        if self.name != None:
            name = ' =>[' + self.name + ']'
        return 'CALLT %s, (%s), (%s)%s' % (self.func, ret, param, name)
    
    def __repr__(self):
        ret   = ','.join([str(p) for p in self.ret])
        param = ','.join([str(p) for p in self.param])
        name  = ''
        if self.name != None:
            name = ' =>[' + self.name + ']'
        return 'CALLT %s, (%s), (%s)%s' % (self.func, ret, param, name)



class CallUMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(CallUMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_CALLU, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.func  = None
        self.ret   = []
        self.param = []
        self.is_param_vararg = False
        self.param_begin_idx = None
        self.is_ret_vararg   = False
        self.ret_var         = None
    
    def SetParamVararg(self):
        self.is_param_vararg = True
    
    def GetParamVararg(self):
        return self.is_param_vararg
    
    def SetRetVararg(self):
        self.is_ret_vararg = True
    
    def GetRetVararg(self):
        return self.is_ret_vararg
    
    def SetParamVarargBegin(self, idx):
        self.param_begin_idx
    
    def GetParamVarargBegin(self):
        return self.param_begin_idx
    
    def SetRetVarargVar(self, var):
        self.ret_var = var
    
    def GetRetVarargVar(self):
        return self.ret_var

    def SetFunctionVar(self, value):
        self.func = value
    
    def GetFunctionVar(self):
        return self.func
    
    def SetReturn(self, ret):
        self.ret = ret
    
    def GetReturn(self):
        return self.ret
        
    def SetParam(self, param):
        self.param = param
    
    def GetParam(self):
        return self.param

    def GetOpCode(self):
        return 'CALLU'
    
    def __str__(self):
        ret   = ','.join([str(p) for p in self.ret])
        param = ','.join([str(p) for p in self.param])
        return 'CALLU %s, (%s), (%s)' % (self.func, ret, param)
    
    def __repr__(self):
        ret   = ','.join([str(p) for p in self.ret])
        param = ','.join([str(p) for p in self.param])
        return 'CALLU %s, (%s), (%s)' % (self.func, ret, param)



class ReturnMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(ReturnMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_RETURN, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.SetEnd(True)
        self.ret = []

    def SetReturn(self, ret):
        self.ret = ret
    
    def GetReturn(self):
        return self.ret
    
    def GetOpCode(self):
        return 'RETURN'
    
    def __str__(self):
        ret = ','.join([str(p) for p in self.ret])
        return 'RETURN (%s)' % (ret)
    
    def __repr__(self):
        ret = ','.join([str(p) for p in self.ret])
        return 'RETURN (%s)' % (ret)


class NnMiddleInstruction(BasicMiddleInstruction):
    '''
    NN R%d
    '''
    def __init__(self):
        super(NnMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_NN, MiddleInstructionType.NODE_NEXT_BRANCH)
        self.var = None
        self.likely_pc_offset   = None
        self.unlikely_pc_offset = None

    def SetVar(self, value):
        self.var = value
    
    def GetVar(self):
        return self.var

    def SetLikelyPCOffset(self, offset):
        self.likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self.likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self.unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self.unlikely_pc_offset
    
    def GetOpCode(self):
        return 'NN'
    
    def __str__(self):
        return 'NN %s' % (self.var)
    
    def __repr__(self):
        return 'NN %s' % (self.var)


class TforcallMiddleInstruction(BasicMiddleInstruction):
    '''
    >= Lua 5.2
    generic for loop
    A C	R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2));
    '''
    def __init__(self):
        super(TforcallMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_TFORCALL, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.ret   = []
        self.func  = None #call who
        '''
        %s := R%d(R%d,R%d)
        '''
        self.func_arg1 = None
        self.func_arg2 = None
    
    def SetReturn(self, ret):
        self.ret = ret
    
    def GetReturn(self):
        return self.ret
    
    def SetFunctionVar(self, value):
        self.func = value
    
    def GetFunctionVar(self):
        return self.func
    
    def SetFunctionArg1Var(self, value):
        self.func_arg1 = value
    
    def GetFunctionArg1Var(self):
        return self.func_arg1
    
    def SetFunctionArg2Var(self, value):
        self.func_arg2 = value
    
    def GetFunctionArg2Var(self):
        return self.func_arg2
    
    def GetOpCode(self):
        return 'TFORCALL'

    def __str__(self):
        ret = ','.join([str(p) for p in self.ret])
        return 'TFORCALL %s, (%s), (%s, %s)' % (self.func, ret, self.func_arg1, self.func_arg2)
    
    def __repr__(self):
        ret = ','.join([str(p) for p in self.ret])
        return 'TFORCALL %s, (%s), (%s, %s)' % (self.func, ret, self.func_arg1, self.func_arg2)
    

class SetlistMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(SetlistMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_SETLIST, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.src   = None
        self.tabidx= None
        self.tab   = None

    def SetSrcVar(self, value):
        self.src = value
    
    def GetSrcVar(self):
        return self.src
    
    def SetTabIndex(self, value):
        self.tabidx = value
    
    def GetTabIndex(self):
        return self.tabidx
    
    def SetTabVar(self, value):
        self.tab = value
    
    def GetTabVar(self):
        return self.tab
    
    def GetOpCode(self):
        return 'SETLIST'

    def __str__(self):
        return 'SETLIST %s, %s, %s' % (self.tab, self.tabidx, self.src)
    
    def __repr__(self):
        return 'SETLIST %s, %s, %s' % (self.tab, self.tabidx, self.src)


class ClosureMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(ClosureMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_CLOSURE, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.func = None
        self.dest = None
    
    def SetFunction(self, idx):
        self.func = idx
    
    def GetFunction(self):
        return self.func
    
    def SetDestVar(self, reg):
        self.dest = reg
    
    def GetDestVar(self):
        return self.dest
    
    def GetOpCode(self):
        return 'CLOSURE'
    
    def __str__(self):
        return 'CLOSURE %s, %d' % (self.dest, self.func)
    
    def __repr__(self):
        return 'CLOSURE %s, %d' % (self.dest, self.func)


class PhiMiddleInstruction(BasicMiddleInstruction):
    def __init__(self):
        super(PhiMiddleInstruction, self).__init__(LuaMiddleOperation.NODE_PHI, MiddleInstructionType.NODE_NEXT_NORMAL)
        self.left  = None
        self.right = None
        self.dest  = None

    def SetDestVar(self, value):
        self.dest = value
    
    def GetDestVar(self):
        return self.dest

    def SetLeftVar(self, value):
        self.left = value
    
    def GetLeftVar(self):
        return self.left

    def SetRightVar(self, value):
        self.right = value
    
    def GetRightVar(self):
        return self.right

    def GetOpCode(self):
        return 'PHI'
    
    def __str__(self):
        return 'PHI %s, %s, %s' % (self.dest, self.left, self.right)
    
    def __repr__(self):
        return 'PHI %s, %s, %s' % (self.dest, self.left, self.right)
