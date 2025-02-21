from __future__ import print_function
import os
import sys
from struct import unpack
from LnEnum import *


SIZE_B = 9
BITRK  = (1 << (SIZE_B - 1))

def ISK(x):
    return ((x) & BITRK)

def INDEXK(r):
    return ((int)(r) & ~BITRK)

def CC(r):
    if ISK(r) != 0:
        return True
    return False

def CV(r):
    if ISK(r) != 0:
        return INDEXK(r)
    return r

'''
instruction types:
'''

iABC = 0
iA = 5
iAB = 1
iAC = 2
iABx = 3
iAsBx = 4
isBx = 6

def GetInstructionVar(s, l, data):
    '''
    le byte order
    '''
    val = 0
    mask = int((2**l) - 1) << s
    val = ((data & mask) >> s)
    return val


#TPLink
Lua51ByteCodeTPLink = {
    0: 'GETTABLE',
    1: 'GETGLOBAL',
    2: 'SETGLOBAL',
    3: 'SETUPVAL',
    4: 'SETTABLE',
    5: 'NEWTABLE',
    6: 'SELF',
    7: 'LOADNIL',
    8: 'LOADK',
    9: 'LOADBOOL',
    10: 'GETUPVAL',
    11: 'LT',
    12: 'LE',
    13: 'EQ',
    14: 'DIV',
    15: 'MUL',
    16: 'SUB',
    17: 'ADD',
    18: 'MOD',
    19: 'POW',
    20: 'UNM',
    21: 'NOT',
    22: 'LEN',
    23: 'CONCAT',
    24: 'JMP',
    25: 'TEST',
    26: 'TESTSET',
    27: 'MOVE',
    28: 'FORLOOP',
    29: 'FORPREP',
    30: 'TFORLOOP',
    31: 'SETLIST',
    32: 'CLOSE',
    33: 'CLOSURE',
    34: 'CALL',
    35: 'RETURN',
    36: 'TAILCALL',
    37: 'VARARG'
}


UnofficialLuaList51 = [
    {
        'name' : 'TP-Link',
        'ref'  : 'Touch P5 V1',
        'code' : Lua51ByteCodeTPLink
    }
]


Lua51ByteCode = {
    0: 'MOVE',  #Copy a value between registers
    1: 'LOADK',  #Load a constant into a register
    2: 'LOADBOOL',  #Load a boolean into a register
    3: 'LOADNIL',  #Load nil values into a range of registers
    4: 'GETUPVAL',  #Read an upvalue into a register
    5: 'GETGLOBAL',  #Read a global variable into a register
    6: 'GETTABLE',  #Read a table element into a register
    7: 'SETGLOBAL',  #Write a register value into a global variable
    8: 'SETUPVAL',  #Write a register value into an upvalue
    9: 'SETTABLE',  #Write a register value into a table element
    10: 'NEWTABLE',  #Create a new table
    11: 'SELF',  #Prepare an object method for calling
    12: 'ADD',  #Addition operator
    13: 'SUB',  #Subtraction operator
    14: 'MUL',  #Multiplication operator
    15: 'DIV',  #Division operator
    16: 'MOD',  #Modulus (remainder) operator
    17: 'POW',  #Exponentiation operator
    18: 'UNM',  #Unary minus operator
    19: 'NOT',  #Logical NOT operator
    20: 'LEN',  #Length operator
    21: 'CONCAT',  #Concatenate a range of registers
    22: 'JMP',  #Unconditional jump
    23: 'EQ',  #Equality test
    24: 'LT',  #Less than test
    25: 'LE',  #Less than or equal to test
    26: 'TEST',  #Boolean test, with conditional jump
    27: 'TESTSET',  #Boolean test, with conditional jump and assignment
    28: 'CALL',  #Call a closure
    29: 'TAILCALL',  #Perform a tail call
    30: 'RETURN',  #Return from function call
    31: 'FORLOOP',  #Iterate a numeric for loop
    32: 'FORPREP',  #Initialization for a numeric for loop
    33: 'TFORLOOP',  #Iterate a generic for loop
    34: 'SETLIST',  #Set a range of array elements for a table
    35: 'CLOSE',  #Close a range of locals being used as upvalues
    36: 'CLOSURE',  #Create a closure of a function prototype
    37: 'VARARG'  #Assign vararg function arguments to registers
}


Lua52ByteCode = {
    0 : 'MOVE',  #	A B	R(A) := R(B)
    1 : 'LOADK',  #	A Bx	R(A) := Kst(Bx)	
    2 : 'LOADKX',  #	A 	R(A) := Kst(extra arg)
    3 : 'LOADBOOL',  #	A B C	R(A) := (Bool)B; if (C) pc++
    4 : 'LOADNIL',  #	A B	R(A), R(A+1), ..., R(A+B) := nil
    5 : 'GETUPVAL',  #	A B	R(A) := UpValue[B]
    6 : 'GETTABUP',  #	A B C	R(A) := UpValue[B][RK(C)]			
    7 : 'GETTABLE',  #	A B C	R(A) := R(B)[RK(C)]				
    8 : 'SETTABUP',  #	A B C	UpValue[A][RK(B)] := RK(C)			
    9 : 'SETUPVAL',  #	A B	UpValue[B] := R(A)
    10 : 'SETTABLE', #	A B C	R(A)[RK(B)] := RK(C)
    11 : 'NEWTABLE', #	A B C	R(A) := {} (size = B,C)	
    12 : 'SELF', #	A B C	R(A+1) := R(B); R(A) := R(B)[RK(C)]
    13 : 'ADD', #	A B C	R(A) := RK(B) + RK(C)
    14 : 'SUB', #	A B C	R(A) := RK(B) - RK(C)
    15 : 'MUL', #	A B C	R(A) := RK(B) * RK(C)
    16 : 'DIV', #	A B C	R(A) := RK(B) / RK(C)
    17 : 'MOD', #	A B C	R(A) := RK(B) % RK(C)
    18 : 'POW', #	A B C	R(A) := RK(B) ^ RK(C)
    19 : 'UNM', #	A B	R(A) := -R(B)
    20 : 'NOT', #	A B	R(A) := not R(B)
    21 : 'LEN', #	A B	R(A) := length of R(B)
    22 : 'CONCAT', #	A B C	R(A) := R(B).. ... ..R(C)
    23 : 'JMP', #	A sBx	pc+=sBx; if (A) close all upvalues >= R(A - 1)
    24 : 'EQ', #	A B C	if ((RK(B) == RK(C)) ~= A) then pc++
    25 : 'LT', #	A B C	if ((RK(B) <  RK(C)) ~= A) then pc++
    26 : 'LE', #	A B C	if ((RK(B) <= RK(C)) ~= A) then pc++
    27 : 'TEST', #	A C	if not (R(A) <=> C) then pc++
    28 : 'TESTSET', #	A B C	if (R(B) <=> C) then R(A) := R(B) else pc++
    29 : 'CALL', #	A B C	R(A), ... ,R(A+C-2) := R(A)(R(A+1), ... ,R(A+B-1))
    30 : 'TAILCALL', #	A B C	return R(A)(R(A+1), ... ,R(A+B-1))
    31 : 'RETURN', #	A B	return R(A), ... ,R(A+B-2)	(see note)
    32 : 'FORLOOP', #	A sBx	R(A)+=R(A+2); if R(A) <?= R(A+1) then { pc+=sBx; R(A+3)=R(A) }
    33 : 'FORPREP', #	A sBx	R(A)-=R(A+2); pc+=sBx
    34 : 'TFORCALL', #	A C	R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2));
    35 : 'TFORLOOP', #	A sBx	if R(A+1) ~= nil then { R(A)=R(A+1); pc += sBx }
    36 : 'SETLIST', #	A B C	R(A)[(C-1)*FPF+i] := R(A+i), 1 <= i <= B
    37 : 'CLOSURE', #	A Bx	R(A) := closure(KPROTO[Bx])
    38 : 'VARARG', #	A B	R(A), R(A+1), ..., R(A+B-2) = vararg
    39 : 'EXTRAARG' #	Ax	extra (larger) argument for previous opcode
}

Lua53ByteCode = {
    0 : 'MOVE',    #A B	R(A) := R(B)
    1 : 'LOADK',    #A Bx	R(A) := Kst(Bx)
    2 : 'LOADKX',    #A 	R(A) := Kst(extra arg)
    3 : 'LOADBOOL',    #A B C	R(A) := (Bool)B; if (C) pc++
    4 : 'LOADNIL',    #A B	R(A), R(A+1), ..., R(A+B) := nil
    5 : 'GETUPVAL',    #A B	R(A) := UpValue[B]
    6 : 'GETTABUP',    #A B C	R(A) := UpValue[B][RK(C)]
    7 : 'GETTABLE',    #A B C	R(A) := R(B)[RK(C)]
    8 : 'SETTABUP',    #A B C	UpValue[A][RK(B)] := RK(C)
    9 : 'SETUPVAL',    #A B	UpValue[B] := R(A)
    10 : 'SETTABLE',   #A B C	R(A)[RK(B)] := RK(C)
    11 : 'NEWTABLE',   #A B C	R(A) := {} (size = B,C)
    12 : 'SELF',   #A B C	R(A+1) := R(B); R(A) := R(B)[RK(C)]
    13 : 'ADD',   #A B C	R(A) := RK(B) + RK(C)
    14 : 'SUB',   #A B C	R(A) := RK(B) - RK(C)
    15 : 'MUL',   #A B C	R(A) := RK(B) * RK(C)
    16 : 'MOD',   #A B C	R(A) := RK(B) % RK(C)
    17 : 'POW',   #A B C	R(A) := RK(B) ^ RK(C)
    18 : 'DIV',   #A B C	R(A) := RK(B) / RK(C)
    19 : 'IDIV',   #A B C	R(A) := RK(B) // RK(C)
    20 : 'BAND',   #A B C	R(A) := RK(B) & RK(C)
    21 : 'BOR',   #A B C	R(A) := RK(B) | RK(C)
    22 : 'BXOR',   #A B C	R(A) := RK(B) ~ RK(C)
    23 : 'SHL',   #A B C	R(A) := RK(B) << RK(C)
    24 : 'SHR',   #A B C	R(A) := RK(B) >> RK(C)
    25 : 'UNM',   #A B	R(A) := -R(B)	
    26 : 'BNOT',   #A B	R(A) := ~R(B)	
    27 : 'NOT',   #A B	R(A) := not R(B)
    28 : 'LEN',   #A B	R(A) := length of R(B)
    29 : 'CONCAT',   #A B C	R(A) := R(B).. ... ..R(C)
    30 : 'JMP',   #A sBx	pc+=sBx; if (A) close all upvalues >= R(A - 1)
    31 : 'EQ',   #A B C	if ((RK(B) == RK(C)) ~= A) then pc++
    32 : 'LT',   #A B C	if ((RK(B) <  RK(C)) ~= A) then pc++
    33 : 'LE',   #A B C	if ((RK(B) <= RK(C)) ~= A) then pc++
    34 : 'TEST',   #A C	if not (R(A) <=> C) then pc++
    35 : 'TESTSET',   #A B C	if (R(B) <=> C) then R(A) := R(B) else pc++
    36 : 'CALL',   #A B C	R(A), ... ,R(A+C-2) := R(A)(R(A+1), ... ,R(A+B-1))
    37 : 'TAILCALL',   #A B C	return R(A)(R(A+1), ... ,R(A+B-1))
    38 : 'RETURN',   #A B	return R(A), ... ,R(A+B-2)	(see note)
    39 : 'FORLOOP',   #A sBx	R(A)+=R(A+2); if R(A) <?= R(A+1) then { pc+=sBx; R(A+3)=R(A) }
    40 : 'FORPREP',   #A sBx	R(A)-=R(A+2); pc+=sBx
    41 : 'TFORCALL',   #A C	R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2));
    42 : 'TFORLOOP',   #A sBx	if R(A+1) ~= nil then { R(A)=R(A+1); pc += sBx }
    43 : 'SETLIST',   # B C	R(A)[(C-1)*FPF+i] := R(A+i), 1 <= i <= B
    44 : 'CLOSURE',   #A ABx	R(A) := closure(KPROTO[Bx])
    45 : 'VARARG',   #A B	R(A), R(A+1), ..., R(A+B-2) = vararg
    46 : 'EXTRAARG'   #Ax	extra (larger) argument for previous opcode
}




class LuaByteCodeInstruction(object):
    def MASK1(self, n,p):
        return ((~((~0)<<(n)))<<(p))
    
    def MASK0(self, n,p):
        return (~self.MASK1(n,p))

    def getint(self, ins, bitness, isbe):
        if bitness == 32:
            if isbe:
                return unpack('>l', ins[0:4])[0]
            else:
                return unpack('<l', ins[0:4])[0]
        else:
            if isbe:
                return unpack('>q', ins[0:8])[0]
            else:
                return unpack('<q', ins[0:8])[0]
        
        raise RuntimeError('unsupported mode : be(%s), bitness(%d)' % (isbe, bitness))


    def GET_OPCODE(self, ins, bitness, isbe):
        i = ins
        return (i>> self.POS_OP) & self.MASK1(self.SIZE_OP,0)
    
    def getarg(self, ins, pos, size, bitness, isbe):
        i = ins
        return int((i>>pos) & self.MASK1(size, 0))
    
    def GETARG_A(self, i, bitness, isbe):
        return self.getarg(i, self.POS_A, self.SIZE_A, bitness, isbe)
    
    def GETARG_B(self, i, bitness, isbe):
        return self.getarg(i, self.POS_B, self.SIZE_B, bitness, isbe)
    
    def GETARG_C(self, i, bitness, isbe):
        return self.getarg(i, self.POS_C, self.SIZE_C, bitness, isbe)
    
    def GETARG_Bx(self, i, bitness, isbe):
        return self.getarg(i, self.POS_Bx, self.SIZE_Bx, bitness, isbe)
    
    def GETARG_Ax(self, i, bitness, isbe):
        return self.getarg(i, self.POS_Ax, self.SIZE_Ax, bitness, isbe)
    
    def GETARG_sBx(self, i, bitness, isbe):
        return (self.GETARG_Bx(i, bitness, isbe) - self.MAXARG_sBx)
    
    #for lua 5.1 SetList
    def GetCode(self):
        return self._code

    def __init__(self, code, bitness, isbe):
        self._code = code
        self.op = 0
        self.a  = 0
        self.b  = 0
        self.c  = 0
        self.bx = 0
        self.sbx= 0
        self.ax = 0 # since lua 5.2
        self.SIZE_C = 9
        self.SIZE_B	= 9
        self.SIZE_Bx = (self.SIZE_C + self.SIZE_B)
        self.SIZE_A = 8
        self.SIZE_Ax = (self.SIZE_C + self.SIZE_B + self.SIZE_A)
        self.SIZE_OP = 6
        self.POS_OP	= 0
        self.POS_A = (self.POS_OP + self.SIZE_OP)
        self.POS_C = (self.POS_A + self.SIZE_A)
        self.POS_B = (self.POS_C + self.SIZE_C)
        self.POS_Bx	= self.POS_C
        self.POS_Ax = self.POS_A

        self.MAXARG_Bx  = ((1<<self.SIZE_Bx)-1)
        self.MAXARG_sBx = (self.MAXARG_Bx>>1)
        self.__SafeDecode(bitness, isbe)
    
    def __SafeDecode(self, bitness, isbe):
        self.op = self.GET_OPCODE(self._code, bitness, isbe)
        self.a  = self.GETARG_A(self._code, bitness, isbe)
        self.b  = self.GETARG_B(self._code, bitness, isbe)
        self.c  = self.GETARG_C(self._code, bitness, isbe)
        self.bx = self.GETARG_Bx(self._code, bitness, isbe)
        self.sbx= self.GETARG_sBx(self._code, bitness, isbe)
        self.ax = self.GETARG_Ax(self._code, bitness, isbe)
        

def get_opcode(b):
    return b & 0x3f


class LuaByteCode():
    def __init__(self, instruction_len, version = LuaVersion.LuaVersion53, is_be = False):
        self._instruction_len = instruction_len
        self._is_be  = is_be
        self.version = version
    
    def Decode(self, data, addr, idx = None):
        if self.version == LuaVersion.LuaVersion51:
            return self.Decode51(data, addr, idx)
        elif self.version == LuaVersion.LuaVersion52:
            return self.Decode52(data, addr)
        elif self.version == LuaVersion.LuaVersion53:
            return self.Decode53(data, addr)
        else:
            raise RuntimeError('unsupported version : %s' % self.version)
    
    def Decode53(self, data, addr):
        '''
        default : lua 5.3
        '''
        if len(data) < self._instruction_len:
            return None, None, None
        
        unpack_type = '<L'
        if self._is_be == False:
            if self._instruction_len == 8:
                unpack_type = '<Q'
        else:
            if self._instruction_len == 4:
                unpack_type = '>L'
            else:
                unpack_type = '>Q'
        
        bitness = 32
        if self._instruction_len == 8:
            bitness = 64
        
        instruction_bytes = unpack(unpack_type, data[0:self._instruction_len])[0]
        opcode_id = get_opcode(instruction_bytes)
        opcode_name = None
        if opcode_id in Lua53ByteCode:
            opcode_name = Lua53ByteCode[opcode_id]
        
        instr = LuaByteCodeInstruction(instruction_bytes, bitness, self._is_be)
        return opcode_name, self._instruction_len, instr

    def Decode52(self, data, addr):
        if len(data) < self._instruction_len:
            return None, None, None
        
        unpack_type = '<L'
        if self._is_be == False:
            if self._instruction_len == 8:
                unpack_type = '<Q'
        else:
            if self._instruction_len == 4:
                unpack_type = '>L'
            else:
                unpack_type = '>Q'
        
        bitness = 32
        if self._instruction_len == 8:
            bitness = 64
        
        instruction_bytes = unpack(unpack_type, data[0:self._instruction_len])[0]
        opcode_id = get_opcode(instruction_bytes)
        opcode_name = None
        if opcode_id in Lua52ByteCode:
            opcode_name = Lua52ByteCode[opcode_id]
        
        instr = LuaByteCodeInstruction(instruction_bytes, bitness, self._is_be)
        return opcode_name, self._instruction_len, instr


    def Decode51(self, data, addr, idx = None):
        if len(data) < self._instruction_len:
            return None, None, None
        
        unpack_type = '<L'
        if self._is_be == False:
            if self._instruction_len == 8:
                unpack_type = '<Q'
        else:
            if self._instruction_len == 4:
                unpack_type = '>L'
            else:
                unpack_type = '>Q'
        
        bitness = 32
        if self._instruction_len == 8:
            bitness = 64

        
        instruction_bytes = unpack(unpack_type, data[0:self._instruction_len])[0]
        opcode_id = get_opcode(instruction_bytes)
        opcode_name = None
        ByteCodeList = Lua51ByteCode
        if idx != None:
            ByteCodeList = UnofficialLuaList51[idx]['code']
        

        if opcode_id in ByteCodeList:
            opcode_name = ByteCodeList[opcode_id]
        
        instr = LuaByteCodeInstruction(instruction_bytes, bitness, self._is_be)
        return opcode_name, self._instruction_len, instr


class LuaByteCodeVarargFlag(enum.Enum):
    VARARG_NONE     = 0
    VARARG_HASARG   = 1
    VARARG_ISVARARG = 2
    VARARG_NEEDSARG = 4

'''
Lua function object
'''

LUA_TNIL = 0
LUA_TBOOLEAN = 1
LUA_TLIGHTUSERDATA = 2
LUA_TNUMBER	= 3
LUA_TSTRING	= 4
LUA_TTABLE = 5
LUA_TFUNCTION = 6
LUA_TUSERDATA = 7
LUA_TTHREAD	= 8
LUA_NUMTAGS	= 9

#Variant tags for strings
LUA_TSHRSTR = (LUA_TSTRING | (0 << 4))
LUA_TLNGSTR = (LUA_TSTRING | (1 << 4))


#Variant tags for numbers
LUA_TNUMFLT = (LUA_TNUMBER | (0 << 4))  #float numbers
LUA_TNUMINT	= (LUA_TNUMBER | (1 << 4))  #integer numbers

