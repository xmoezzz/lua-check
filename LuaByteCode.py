#raw input bytecode

from __future__ import print_function
import enum


class LuaInstructionOperation(enum.Enum):
    NODE_MOVE      = 0
    NODE_LOADK     = 1
    NODE_LOADKX    = 2
    NODE_LOADBOOL  = 3
    NODE_LOADNIL   = 4
    NODE_GETUPVAL  = 5
    NODE_GETTABUP  = 6
    NODE_GETTABLE  = 7
    NODE_SETTABUP  = 8
    NODE_SETUPVAL  = 9
    NODE_SETTABLE  = 10
    NODE_NEWTABLE  = 11
    NODE_SELF      = 12
    NODE_ADD       = 13
    NODE_SUB       = 14
    NODE_MUL       = 15
    NODE_MOD       = 16
    NODE_POW       = 17
    NODE_DIV       = 18
    NODE_IDIV      = 19
    NODE_BAND      = 20
    NODE_BOR       = 21
    NODE_BXOR      = 22
    NODE_SHL       = 23
    NODE_SHR       = 24
    NODE_UNM       = 25
    NODE_BNOT      = 26
    NODE_NOT       = 27
    NODE_LEN       = 28
    NODE_CONCAT    = 29
    NODE_JMP       = 30
    NODE_EQ        = 31
    NODE_LT        = 32
    NODE_LE        = 33
    NODE_TEST      = 34
    NODE_TESTSET   = 35
    NODE_CALL      = 36
    NODE_TAILCALL  = 37
    NODE_RETURN    = 38
    NODE_FORLOOP   = 39
    NODE_FORREP    = 40
    NODE_TFORCALL  = 41
    NODE_TFORLOOP  = 42
    NODE_SETLIST   = 43
    NODE_CLOSURE   = 44
    NODE_VARARG    = 45
    NODE_EXTRAARG  = 46
    NODE_RAW       = 47 #dummy
    NODE_GETGLOBAL = 48
    NODE_SETGLOBAL = 49
    NODE_TFORLOOPX = 50 #lua 5.1
    NODE_CLOSE     = 51 #lua 5.1


class BasicNodeNextType(enum.Enum):
    NODE_NEXT_NORMAL = 0 #following instruction is the next instruction
    NODE_NEXT_JMP    = 1 #next instruction is stored in jmp_offset
    NODE_NEXT_BRANCH = 2 #likely or unlikely


class LuaInstruction(object):
    def __init__(self, ntype, node_next_type):
        self._ntype = ntype

        #normal node
        if not isinstance(node_next_type, BasicNodeNextType):
            raise TypeError('type of node_next_type must be BasicNodeNextType')
        
        self._next_node_type = node_next_type #only in constructor
        self._next_node = None

        #if ... else ...
        '''
        likely   node : true statement(if (...) or for ())
        unlikely node : false statement (else(...) or for end )
        '''
        self._likely_node    = None
        self._unlinkely_node = None

        #ending field
        self._is_end = False #return?

        self._pc_offset = 0
        self._src_line  = -1
        self._skip_next = False
        self._mlil      = None #only this first one
        self._force_skip = False #fuck lua5.1
    
    def SetMlil(self, mlil):
        self._mlil = mlil
    
    def GetMlil(self):
        return self._mlil
    
    def SetForceSkip(self):
        self._force_skip = True
    
    def IsForceSkip(self):
        return self._force_skip
    
    def GetSrcLine(self, line):
        return self._src_line
    
    def SetSrcLine(self, line):
        self._src_line = line
    
    def SetSkipNext(self, bval):
        self._skip_next = bval
    
    def GetSkipNext(self):
        return self._skip_next
    
    def GetPCOffset(self):
        return self._pc_offset
    
    def SetPCOffset(self, pc):
        self._pc_offset = pc
    
    def _NodeTypeTestMethod(self):
        pass
    
    def SetEnd(self):
        self._is_end = True

    def SetNotEnd(self):
        self._is_end = False
    
    def IsEndInstruction(self):
        return self._is_end == True
    
    def IsNormalInstruction(self):
        return self._next_node_type == BasicNodeNextType.NODE_NEXT_NORMAL
    
    def IsJmpInstruction(self):
        return self._next_node_type == BasicNodeNextType.NODE_NEXT_JMP
    
    def IsBranchInstruction(self):
        return self._next_node_type == BasicNodeNextType.NODE_NEXT_BRANCH
    
    def SetNextInstruction(self, node):
        if self._next_node_type != BasicNodeNextType.NODE_NEXT_NORMAL:
            raise RuntimeError('SetNextNode is not vaild for branch node or jmp node')
        if hasattr(node, '_NodeTypeTestMethod') == False and node != None:
            raise RuntimeError('SetNextNode : node != NodeType')
        self._next_node = node
    
    def GetNextInstruction(self):
        if self._next_node_type != BasicNodeNextType.NODE_NEXT_NORMAL:
            raise RuntimeError('GetNextNode is not vaild for branch node or jmp node')
        return self._next_node
    
    def GetLikelyInstruction(self):
        if self._next_node_type != BasicNodeNextType.NODE_NEXT_BRANCH:
            raise RuntimeError('GetLikelyNode is not vaild for normal node or jmp node')
        return self._likely_node
    
    def SetLikelyInstruction(self, node):
        if self._next_node_type != BasicNodeNextType.NODE_NEXT_BRANCH:
            raise RuntimeError('SetLikelyNode is not vaild for normal node or jmp node')
        if hasattr(node, '_NodeTypeTestMethod') == False and node != None:
            raise RuntimeError('SetLikelyNode : node != NodeType')
        self._likely_node = node
    
    def GetUnlikelyInstruction(self):
        if self._next_node_type != BasicNodeNextType.NODE_NEXT_BRANCH:
            raise RuntimeError('GetUnlikelyNode is not vaild for normal node or jmp node')
        return self._unlinkely_node
    
    def SetUnlikelyInstruction(self, node):
        if self._next_node_type != BasicNodeNextType.NODE_NEXT_BRANCH:
            raise RuntimeError('SetUnlikelyNode is not vaild for normal node or jmp node')
        if hasattr(node, '_NodeTypeTestMethod') == False and node != None:
            raise RuntimeError('SetUnlikelyNode : node != NodeType')
        self._unlinkely_node = node
    
    def GetJmpInstruction(self):
        if self._next_node_type != BasicNodeNextType.NODE_NEXT_JMP:
            raise RuntimeError('SetJmpNode is not vaild for normal node or branch node')
        return self._next_node
    
    def SetJmpInstruction(self, node):
        if self._next_node_type != BasicNodeNextType.NODE_NEXT_JMP:
            raise RuntimeError('GetJmpNode is not vaild for normal node or branch node')
        if hasattr(node, '_NodeTypeTestMethod') == False and node != None:
            raise RuntimeError('SetJmpNode : node != NodeType')
        self._next_node = node

class TforloopXInstruction(LuaInstruction):
    '''
    == lua51 ==
    generic for loop
    A C	R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2));
    if R(A+3) ~= nil then R(A+2)=R(A+3) else pc++
    '''
    def __init__(self):
        super(TforloopXInstruction, self).__init__(LuaInstructionOperation.NODE_TFORLOOPX, BasicNodeNextType.NODE_NEXT_BRANCH)
        self.A = None
        self.C = None
        self._likely_pc_offset  = None
        self._unlikely_pc_offset = None

    def SetLikelyPCOffset(self, offset):
        self._likely_pc_offset = offset

    def GetLikelyPCOffset(self):
        return self._likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self._unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self._unlikely_pc_offset
    
    def GetOpCode(self):
        return 'TFORLOOPX'

class CloseInstruction(LuaInstruction):
    def __init__(self):
        super(CloseInstruction, self).__init__(LuaInstructionOperation.NODE_CLOSE, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
    
    def GetOpCode(self):
        return 'CLOSE'

class RawInstruction(LuaInstruction):
    '''
    raw value
    '''
    def __init__(self):
        super(RawInstruction, self).__init__(LuaInstructionOperation.NODE_RAW, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.Value = None
    
    def GetOpCode(self):
        return 'RAW'

class GetGlobalInstruction(LuaInstruction):
    '''
    GETGLOBAL A Bx
    '''
    def __init__(self):
        super(GetGlobalInstruction, self).__init__(LuaInstructionOperation.NODE_GETGLOBAL, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A  = None
        self.Bx = None
    
    def GetOpCode(self):
        return 'GETGLOBAL'

class SetGlobalInstruction(LuaInstruction):
    '''
    SetGlobal A Bx
    '''
    def __init__(self):
        super(SetGlobalInstruction, self).__init__(LuaInstructionOperation.NODE_SETGLOBAL, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A  = None
        self.Bx = None
    
    def GetOpCode(self):
        return 'SETGLOBAL'

class MoveInstruction(LuaInstruction):
    '''
    MOVE A B
    '''
    def __init__(self):
        super(MoveInstruction, self).__init__(LuaInstructionOperation.NODE_MOVE, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A  = None
        self.B   = None
    
    def GetOpCode(self):
        return 'MOVE'

class LoadkInstruction(LuaInstruction):
    '''
    LOADK A Bx
    '''
    def __init__(self):
        super(LoadkInstruction, self).__init__(LuaInstructionOperation.NODE_LOADK, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A  = None
        self.Bx = None
    
    def GetOpCode(self):
        return 'LOADK'

class LoadkxInstruction(LuaInstruction):
    '''
    LOADKX A Ax(next)
    '''
    def __init__(self):
        super(LoadkxInstruction, self).__init__(LuaInstructionOperation.NODE_LOADKX, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A   = None
        self.Ax  = None
    
    def GetOpCode(self):
        return 'LOADKX'

class LoadboolInstruction(LuaInstruction):
    '''
    LOADBOOL A B C
    '''
    def __init__(self):
        super(LoadboolInstruction, self).__init__(LuaInstructionOperation.NODE_LOADBOOL, BasicNodeNextType.NODE_NEXT_BRANCH)
        self.A = None
        self.B = None
        self.C = None
        self._likely_pc_offset  = None
        self._unlikely_pc_offset = None
    
    def SetLikelyPCOffset(self, offset):
        self._likely_pc_offset = offset

    def GetLikelyPCOffset(self):
        return self._likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self._unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self._unlikely_pc_offset
    
    def GetOpCode(self):
        return 'LOADBOOL'

class LoadNilInstruction(LuaInstruction):
    '''
    LOADNIL A B
    '''
    def __init__(self):
        super(LoadNilInstruction, self).__init__(LuaInstructionOperation.NODE_LOADNIL, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
    
    def GetOpCode(self):
        return 'LOADNIL'

class VarargInstruction(LuaInstruction):
    '''
    VARARG  A B
    '''
    def __init__(self):
        super(VarargInstruction, self).__init__(LuaInstructionOperation.NODE_VARARG, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A  = None
        self.B = None
    
    def GetOpCode(self):
        return 'VARARG'

class GetUpvalInstruction(LuaInstruction):
    '''
    GETUPVAL A B
    '''
    def __init__(self):
        super(GetUpvalInstruction, self).__init__(LuaInstructionOperation.NODE_GETUPVAL, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
    
    def GetOpCode(self):
        return 'GETUPVAL'


class GettabupInstruction(LuaInstruction):
    '''
    GETTABUP A B C
    '''
    def __init__(self):
        super(GettabupInstruction, self).__init__(LuaInstructionOperation.NODE_GETTABUP, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
        self.CConstMode = None

    def GetOpCode(self):
        return 'GETTABUP'


class GettableInstruction(LuaInstruction):
    '''
    GETTABLE A B C
    '''
    def __init__(self):
        super(GettableInstruction, self).__init__(LuaInstructionOperation.NODE_GETTABLE, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
        self.CConstMode = None
    
    def GetOpCode(self):
        return 'GETTABLE'


class SettabupInstruction(LuaInstruction):
    '''
    SETTABUP A B C
    '''
    def __init__(self):
        super(SettabupInstruction, self).__init__(LuaInstructionOperation.NODE_SETTABUP, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
        self.BConstMode = None
        self.CConstMode = None
    
    def GetOpCode(self):
        return 'SETTABUP'

class SetUpvalInstruction(LuaInstruction):
    '''
    SETUPVAL  A B
    '''
    def __init__(self):
        super(SetUpvalInstruction, self).__init__(LuaInstructionOperation.NODE_SETUPVAL, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
    
    def GetOpCode(self):
        return 'SETUPVAL'

class SettableInstruction(LuaInstruction):
    '''
    SETTABLE A B C
    '''
    def __init__(self):
        super(SettableInstruction, self).__init__(LuaInstructionOperation.NODE_SETTABLE, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
        self.BConstMode = None
        self.CConstMode = None
    
    def GetOpCode(self):
        return 'SETTABLE'
    
class NewtableInstruction(LuaInstruction):
    '''
    NEWTABLE A
    '''
    def __init__(self):
        super(NewtableInstruction, self).__init__(LuaInstructionOperation.NODE_NEWTABLE, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
    
    def GetOpCode(self):
        return 'NEWTABLE'
    
class SelfInstruction(LuaInstruction):
    '''
    SELF  A B C
    '''
    def __init__(self):
        super(SelfInstruction, self).__init__(LuaInstructionOperation.NODE_SELF, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
        self.CConstMode = None

    def GetOpCode(self):
        return 'SELF'

class MathBaseInstruction(LuaInstruction):
    def __init__(self, ntype):
        super(MathBaseInstruction, self).__init__(ntype, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
        self.BConstMode   = None
        self.CConstMode   = None

class AddInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) + RK(C)
    '''
    def __init__(self):
        super(AddInstruction, self).__init__(LuaInstructionOperation.NODE_ADD)
    
    def GetOpCode(self):
        return 'ADD'

class SubInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) - RK(C)
    '''
    def __init__(self):
        super(SubInstruction, self).__init__(LuaInstructionOperation.NODE_SUB)

    def GetOpCode(self):
        return 'SUB'

class MulInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) * RK(C)
    '''
    def __init__(self):
        super(MulInstruction, self).__init__(LuaInstructionOperation.NODE_MUL)
    
    def GetOpCode(self):
        return 'MUL'

class DivInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) / RK(C)
    '''
    def __init__(self):
        super(DivInstruction, self).__init__(LuaInstructionOperation.NODE_DIV)
    
    def GetOpCode(self):
        return 'DIV'

class PowInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) % RK(C)
    '''
    def __init__(self):
        super(PowInstruction, self).__init__(LuaInstructionOperation.NODE_POW)
    
    def GetOpCode(self):
        return 'POW'

class ModInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) ^ RK(C)
    '''
    def __init__(self):
        super(ModInstruction, self).__init__(LuaInstructionOperation.NODE_MOD)
    
    def GetOpCode(self):
        return 'MOD'

class IdivInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) // RK(C)
    '''
    def __init__(self):
        super(IdivInstruction, self).__init__(LuaInstructionOperation.NODE_IDIV)
    
    def GetOpCode(self):
        return 'IDIV'

class BandInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) & RK(C)
    '''
    def __init__(self):
        super(BandInstruction, self).__init__(LuaInstructionOperation.NODE_BAND)
    
    def GetOpCode(self):
        return 'BAND'

class BorInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) | RK(C)
    '''
    def __init__(self):
        super(BorInstruction, self).__init__(LuaInstructionOperation.NODE_BOR)
    
    def GetOpCode(self):
        return 'BOR'

class BxorInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) ~ RK(C)
    '''
    def __init__(self):
        super(BxorInstruction, self).__init__(LuaInstructionOperation.NODE_BXOR)
    
    def GetOpCode(self):
        return 'BXOR'

class ShlInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) << RK(C)
    '''
    def __init__(self):
        super(ShlInstruction, self).__init__(LuaInstructionOperation.NODE_SHL)
    
    def GetOpCode(self):
        return 'SHL'

class ShrInstruction(MathBaseInstruction):
    '''
    R(A) := RK(B) >> RK(C)
    '''
    def __init__(self):
        super(ShrInstruction, self).__init__(LuaInstructionOperation.NODE_SHR)
    
    def GetOpCode(self):
        return 'SHR'

class UnaryBaseInstruction(LuaInstruction):
    def __init__(self, ntype):
        super(UnaryBaseInstruction, self).__init__(ntype, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A  = None
        self.B = None

class UnmInstruction(UnaryBaseInstruction):
    '''
    R(A) := -R(B)
    '''
    def __init__(self):
        super(UnmInstruction, self).__init__(LuaInstructionOperation.NODE_UNM)
    
    def GetOpCode(self):
        return 'UNM'

class NotInstruction(UnaryBaseInstruction):
    '''
    R(A) := not R(B)
    '''
    def __init__(self):
        super(NotInstruction, self).__init__(LuaInstructionOperation.NODE_NOT)
    
    def GetOpCode(self):
        return 'NOT'

class LenInstruction(UnaryBaseInstruction):
    '''
    R(A) := length of R(B)
    '''
    def __init__(self):
        super(LenInstruction, self).__init__(LuaInstructionOperation.NODE_LEN)
    
    def GetOpCode(self):
        return 'LEN'

class BnotInstruction(UnaryBaseInstruction):
    '''
    R(A) := ~R(B)
    '''
    def __init__(self):
        super(BnotInstruction, self).__init__(LuaInstructionOperation.NODE_BNOT)
    
    def GetOpCode(self):
        return 'BNOT'

class ConcatInstruction(LuaInstruction):
    '''
    CONCAT A B C
    R(A) := R(B).. ... ..R(C)
    '''
    def __init__(self):
        super(ConcatInstruction, self).__init__(LuaInstructionOperation.NODE_BNOT, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
    
    def GetOpCode(self):
        return 'CONCAT' 


class JmpInstruction(LuaInstruction):
    '''
    JMP A sBx
    '''
    def __init__(self):
        super(JmpInstruction, self).__init__(LuaInstructionOperation.NODE_JMP, BasicNodeNextType.NODE_NEXT_JMP)
        self.jmp_offset = None
        self.A   = None
        self.sBx = None
    
    def SetJmpOffset(self, offset):
        self.jmp_offset = offset
    
    def GetJmpOffset(self):
        return self.jmp_offset
    
    def GetOpCode(self):
        return 'JMP'

class ConditionBranchBaseInstruction(LuaInstruction):
    '''
    if ((RK(B) <op> RK(C)) ~= A) then pc++
    '''
    def __init__(self, ntype):
        super(ConditionBranchBaseInstruction, self).__init__(ntype, BasicNodeNextType.NODE_NEXT_BRANCH)
        self.likely_pc_offset   = None
        self.unlikely_pc_offset = None
        self.A = None
        self.B = None
        self.C = None
        self.BConstMode = None
        self.CConstMode = None
    
    def SetA(self, value):
        self._a_condition = value
    
    def GetResultCondition(self):
        return self._a_condition
    
    def SetLikelyPCOffset(self, offset):
        self.likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self.likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self.unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self.unlikely_pc_offset
    
    
class EqInstruction(ConditionBranchBaseInstruction):
    '''
    if ((RK(B) == RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(EqInstruction, self).__init__(LuaInstructionOperation.NODE_EQ)
    
    def GetOpCode(self):
        return 'EQ'

class LtInstruction(ConditionBranchBaseInstruction):
    '''
    if ((RK(B) <  RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LtInstruction, self).__init__(LuaInstructionOperation.NODE_LT)
    
    def GetOpCode(self):
        return 'LT'

class LeInstruction(ConditionBranchBaseInstruction):
    '''
    if ((RK(B) <= RK(C)) ~= A) then pc++
    '''
    def __init__(self):
        super(LeInstruction, self).__init__(LuaInstructionOperation.NODE_LE)
    
    def GetOpCode(self):
        return 'LE'

class TestInstruction(LuaInstruction):
    '''
    TEST        A C
    if not (R(A) <=> C) then pc++
    '''
    def __init__(self):
        super(TestInstruction, self).__init__(LuaInstructionOperation.NODE_TEST, BasicNodeNextType.NODE_NEXT_BRANCH)
        self.A = True
        self.C = None
        self._likely_pc_offset  = None
        self._unlikely_pc_offset = None
    
    def SetLikelyPCOffset(self, offset):
        self._likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self._likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self._unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self._unlikely_pc_offset
    
    def GetOpCode(self):
        return 'TEST'


class TestsetInstruction(LuaInstruction):
    '''
    TESTSET     A B C
    if (R(B) <=> C) then R(A) := R(B) else pc++
    '''
    def __init__(self):
        super(TestsetInstruction, self).__init__(LuaInstructionOperation.NODE_TESTSET, BasicNodeNextType.NODE_NEXT_BRANCH)
        self.A = None
        self.B = None
        self.C = None
        self._likely_pc_offset  = None
        self._unlikely_pc_offset = None
    
    def SetLikelyPCOffset(self, offset):
        self._likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self._likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self._unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self._unlikely_pc_offset
    
    def GetOpCode(self):
        return 'TESTSET'    

class CallInstruction(LuaInstruction):
    '''
    CALL A B C
    R(A), ... ,R(A+C-2) := R(A)(R(A+1), ... ,R(A+B-1))
    '''
    def __init__(self):
        super(CallInstruction, self).__init__(LuaInstructionOperation.NODE_CALL, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
    
    def GetOpCode(self):
        return 'CALL'    


class ReturnInstruction(LuaInstruction):
    '''
    RETURN  A B
    return R(A), ... ,R(A+B-2)
    '''
    def __init__(self):
        super(ReturnInstruction, self).__init__(LuaInstructionOperation.NODE_RETURN, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.SetEnd()
    
    def GetOpCode(self):
        return 'RETURN'

class ForloopInstruction(LuaInstruction):
    '''
    FORLOOP    A sBx
    numeric for loop
    likely branch   : back to loop
    unlikely branch : jump out of the loop
    FORLOOP    A sBx   R(A)+=R(A+2);
               if R(A) <?= R(A+1) then { pc+=sBx; R(A+3)=R(A) }
    '''
    def __init__(self):
        super(ForloopInstruction, self).__init__(LuaInstructionOperation.NODE_FORLOOP, BasicNodeNextType.NODE_NEXT_BRANCH)
        self.likely_pc_offset   = None
        self.unlikely_pc_offset = None
        self.A    = None
        self.sBx  = None
        
    def SetLikelyPCOffset(self, offset):
        self.likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self.likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self.unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self.unlikely_pc_offset
    
    def GetOpCode(self):
        return 'FORLOOP'

class ForrepInstruction(LuaInstruction):
    '''
    FORPREP    A sBx
    numeric for loop
    prepare the Initialization state for a loop
    FORPREP    A sBx   R(A)-=R(A+2); pc+=sBx
    '''
    def __init__(self):
        super(ForrepInstruction, self).__init__(LuaInstructionOperation.NODE_FORREP, BasicNodeNextType.NODE_NEXT_JMP)
        self.A   = None
        self.sBx = None
        self.jmp_offset= None
    
    def SetJmpOffset(self, offset):
        self._jmp_offset = offset
    
    def GetJmpOffset(self):
        return self._jmp_offset
    
    def GetOpCode(self):
        return 'FORREP'

class TforloopInstruction(LuaInstruction):
    '''
    TFORLOOP    A sBx
    >= Lua 5.2
    generic for loop
    if R%d ~= nil then { R%d := R%d ; pc += %d (goto %d) } % (a+1, a, a+1, sbc, dest)
    if R(src) ~= nil then {R(dest) := R(src); goto _likely_pc_offset} else goto _unlikely_pc_offset (next)
    '''
    def __init__(self):
        super(TforloopInstruction, self).__init__(LuaInstructionOperation.NODE_TFORLOOP, BasicNodeNextType.NODE_NEXT_BRANCH)
        self.likely_pc_offset   = None
        self.unlikely_pc_offset = None
        self.A   = None
        self.sBx = None
        
    def SetLikelyPCOffset(self, offset):
        self.likely_pc_offset = offset
    
    def GetLikelyPCOffset(self):
        return self.likely_pc_offset
    
    def SetUnlikelyPCOffset(self, offset):
        self.unlikely_pc_offset = offset
    
    def GetUnlikelyPCOffset(self):
        return self.unlikely_pc_offset
    
    def GetOpCode(self):
        return 'TFORLOOP'

class TforcallInstruction(LuaInstruction):
    '''
    TFORCALL    A C
    >= Lua 5.2
    generic for loop
    A C	R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2));
    '''
    def __init__(self):
        super(TforcallInstruction, self).__init__(LuaInstructionOperation.NODE_TFORCALL, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.C = None
    
    def GetOpCode(self):
        return 'TFORCALL'    


class SetlistInstruction(LuaInstruction):
    '''
    SETLIST A B C
    R(A)[(C-1)*FPF+i] := R(A+i), 1 <= i <= B
    b == 0 : R%d[%d] to R%d[top] := R%d to top
    b == 1 : R%d[%d] := R%d
    b > 1  : R%d[%d] to R%d[%d] := R%d to R%d
    '''
    def __init__(self):
        super(SetlistInstruction, self).__init__(LuaInstructionOperation.NODE_SETLIST, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A = None
        self.B = None
        self.C = None
    
    def GetOpCode(self):
        return 'SETLIST'

class ClosureInstruction(LuaInstruction):
    '''
    CLOSURE A Bx
    '''
    def __init__(self):
        super(ClosureInstruction, self).__init__(LuaInstructionOperation.NODE_CLOSURE, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.A  = None
        self.Bx = None
    
    def GetOpCode(self):
        return 'CLOSURE'

class ExtraargInstruction(LuaInstruction):
    def __init__(self):
        super(ExtraargInstruction, self).__init__(LuaInstructionOperation.NODE_EXTRAARG, BasicNodeNextType.NODE_NEXT_NORMAL)
        self.sBx = None
    
    def GetOpCode(self):
        return 'EXTRAARG'


