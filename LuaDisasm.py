from __future__ import print_function
import logging
from LuaInstruction import *
from LuaByteCode import *
from LnEnum import Endianness, LuaVersion
from LuaError import *

logger = logging.getLogger(__name__)
logger.propagate = False

def disasm_invopstr(opcode):
    if opcode == LuaInstructionOperation.NODE_EQ:
        return '~='
    elif opcode == LuaInstructionOperation.NODE_LE:
        return '>'
    elif opcode == LuaInstructionOperation.NODE_LT:
        return '>='
    else:
        raise RuntimeError('invopstr : invalid opcode (%s)' % str(opcode))

def disasm_opstr(opcode):
    if opcode == LuaInstructionOperation.NODE_EQ:
        return '=='
    elif opcode == LuaInstructionOperation.NODE_LE:
        return '<='
    elif opcode == LuaInstructionOperation.NODE_LT:
        return '<'
    else:
        raise RuntimeError('opstr : invalid opcode (%s)' % str(opcode))
    

class LuaDisasm(object):
    def __init__(self, stream, instructionSize, codeSize, constants, isBE, version = LuaVersion.LuaVersion53):
        self.instructions = []
        self.stream       = stream
        self.codeSize     = codeSize
        self.instructionSize = instructionSize
        self.isBE         = isBE
        self.constants    = constants
        self.version      = version
        self.enableLog    = False

    def DisassembleCode(self, current_pos, nextCodeIndex = None):
        pc_offset = 0

        while pc_offset < self.codeSize:
            next_code_str = None

            current_code_str = self.stream.read(self.instructionSize)
            instr = LuaByteCode(self.instructionSize, self.version, self.isBE)
            cur_opcode_name, cur_instruction_len, cur_instr = instr.Decode(current_code_str, current_pos, nextCodeIndex)

            if cur_opcode_name == None:
                raise RuntimeError('Unable to decode Lua instruction @ %x' % current_pos)
            current_pos = current_pos + self.instructionSize
            
            if pc_offset + 1 < self.codeSize:
                next_code_str = self.stream.read(self.instructionSize)
                self.stream.seek(current_pos)
            
            #dispatch
            decoded_array = None
            forced        = False

            if   cur_opcode_name == 'MOVE':
                decoded_array, forced = self._DecodeMove(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'LOADK':
                decoded_array, forced = self._DecodeLoadK(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'LOADKX':
                decoded_array, forced = self._DecodeLoadKx(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'LOADBOOL':
                decoded_array, forced = self._DecodeLoadBool(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'LOADNIL':
                decoded_array, forced = self._DecodeLoadNil(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'VARARG':
                decoded_array, forced = self._DecodeVararg(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'GETUPVAL':
                decoded_array, forced = self._DecodeGetUpValue(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'GETTABUP':
                decoded_array, forced = self._DecodeGetTabup(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'GETTABLE':
                decoded_array, forced = self._DecodeGetTable(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SETTABUP':
                decoded_array, forced = self._DecodeSetTabup(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SETUPVAL':
                decoded_array, forced = self._DecodeSetUpVal(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SETTABLE':
                decoded_array, forced = self._DecodeSetTable(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'NEWTABLE':
                decoded_array, forced = self._DecodeNewTable(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SELF':
                decoded_array, forced = self._DecodeSelf(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'ADD':
                decoded_array, forced = self._DecodeAdd(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SUB':
                decoded_array, forced = self._DecodeSub(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'MUL':
                decoded_array, forced = self._DecodeMul(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'DIV':
                decoded_array, forced = self._DecodeDiv(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'POW':
                decoded_array, forced = self._DecodePow(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'MOD':
                decoded_array, forced = self._DecodeMod(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'IDIV':
                decoded_array, forced = self._DecodeIdiv(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'BAND':
                decoded_array, forced = self._DecodeBand(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'BOR':
                decoded_array, forced = self._DecodeBor(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'BXOR':
                decoded_array, forced = self._DecodeBxor(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SHL':
                decoded_array, forced = self._DecodeShl(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SHR':
                decoded_array, forced = self._DecodeShr(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'UNM':
                decoded_array, forced = self._DecodeUnm(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'NOT':
                decoded_array, forced = self._DecodeNot(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'LEN':
                decoded_array, forced = self._DecodeLen(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'BNOT':
                decoded_array, forced = self._DecodeBnot(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'CONCAT':
                decoded_array, forced = self._DecodeConcat(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'JMP':
                decoded_array, forced = self._DecodeJmp(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'EQ':
                decoded_array, forced = self._DecodeEq(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'LT':
                decoded_array, forced = self._DecodeLt(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'LE':
                decoded_array, forced = self._DecodeLe(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'TEST':
                decoded_array, forced = self._DecodeTest(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'TESTSET':
                decoded_array, forced = self._DecodeTestSet(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'CALL':
                decoded_array, forced = self._DecodeCall(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'TAILCALL':
                decoded_array, forced = self._DecodeTailCall(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'RETURN':
                decoded_array, forced = self._DecodeReturn(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'FORLOOP':
                decoded_array, forced = self._DecodeForLoop(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'FORPREP':
                decoded_array, forced = self._DecodeForRep(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'TFORCALL':
                decoded_array, forced = self._DecodeTForCall(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'TFORLOOP':
                    decoded_array, forced = self._DecodeTForLoop(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SETLIST':
                decoded_array, forced = self._DecodeSetList(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'CLOSURE':
                decoded_array, forced = self._DecodeClosure(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'GETGLOBAL':
                decoded_array, forced = self._DecodeGetGlobal(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'SETGLOBAL':
                decoded_array, forced = self._DecodeSetGlobal(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            elif cur_opcode_name == 'CLOSE':
                decoded_array, forced = self._DecodeClose(pc_offset, cur_instr, next_code_str, nextCodeIndex)
            #should never reach here...
            elif cur_opcode_name in ('EXTRAARG', 'RAW'):
                raise RuntimeError('_DisassembleCode : should never reach EXTRAARG')
            else:
                raise RuntimeError('_DisassembleCode : Unknown bytecode (%s) @ pc offset -> %x' % (cur_opcode_name, pc_offset))
            
            if decoded_array == None or len(decoded_array) == 0:
                raise RuntimeError('_DisassembleCode : empty result')
            
            if len(decoded_array) > 1:
                current_pos = current_pos + self.instructionSize
                self.stream.seek(current_pos)
                if forced == True:
                    pc_offset = pc_offset + len(decoded_array)
                    self.instructions.extend(decoded_array)
                else:
                    raise RuntimeError('should never reach here!!!!!!!')
                    self.instructions.append(decoded_array[0])
            else:
                pc_offset = pc_offset + 1
                self.instructions.append(decoded_array[0])
        
        return self.stream.tell()


    def _DecodeGetGlobal(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = GetGlobalInstruction()
        node.A  = current_code.a
        node.Bx = current_code.bx

        if self.enableLog: logger.info('\t>> GETGLOBAL R%d, G%d' % (current_code.a, current_code.bx))

        return [node], False
    
    def _DecodeSetGlobal(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = SetGlobalInstruction()
        node.Bx = current_code.bx
        node.A  = current_code.a

        if self.enableLog: logger.info('\t>> SETGLOBAL R%d, G%d (G = %s)' % (
            current_code.a, current_code.bx, str(self.constants[current_code.bx])
        ))
        return [node], False
    

    def _DecodeMove(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = MoveInstruction()
        node.A = current_code.a
        node.B = current_code.b
        
        if self.enableLog: logger.info('\t>> MOVE R%d, R%d' % (current_code.a, current_code.b))
        return [node], False

    def _DecodeLoadK(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        '''
        load constant to register
        '''
        node = LoadkInstruction()
        node.A  = current_code.a
        node.Bx = current_code.bx

        if self.enableLog: logger.info('\t>> LOADK R%d, K%d (%s)' % (current_code.a, current_code.bx, 
            str(self.constants[current_code.bx])))
        return [node], False
    
    #ignore OP_EXTRAARG
    def _DecodeLoadKx(self, current_pc, current_code, next_code_str, nextCodeIndex = None):
        if next_code_str == None:
            raise RuntimeError('next_code cannot be None in _DecodeLOADKX')
        
        next_code_ins = LuaByteCode(self.instructionSize, self.isBE)
        next_opcode_name, next_instruction_len, next_code = next_code_ins.Decode(next_code_str, 0, nextCodeIndex)

        node = LoadkxInstruction()
        node.A = current_code.a
        node.B = next_code.ax
        node.SetSkipNext(True)
        
        subnode = ExtraargInstruction()
        subnode.Ax = next_code.ax

        if self.enableLog: logger.info('\t>> LOADKX R%d, K%d (%s)' % (current_code.a, current_code.bx, 
            str(self.constants[next_code.ax])))
        
        if self.enableLog: logger.info('\t>> EXTRAARG %d' % next_code.ax)
        
        return [node, subnode], True
    
    def _DecodeClose(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = CloseInstruction()

        return [node], False
    
    def _DecodeLoadBool(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = LoadboolInstruction()
        node.B = current_code.b
        node.A = current_code.a
        node.C = current_code.c

        if current_code.c != 0:
            node.SetLikelyPCOffset(current_pc + 2)
        else:
            node.SetLikelyPCOffset(current_pc + 1)
        
        node.SetUnlikelyPCOffset(current_pc + 1)
        
        if self.enableLog: logger.info('\t>> LOADBOOL (A, B, C) = %d, %d, %d (Likely = %d, UnLikely = %d)' % (
            current_code.a, current_code.b, current_code.c, current_pc + 2, current_pc + 1
        ))

        return [node], False
    
    def _DecodeLoadNil(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = LoadNilInstruction()
        node.A = current_code.a
        node.B = current_code.b

        begin = current_code.a
        end   = current_code.a + current_code.b

        if self.enableLog: logger.info('\t>> LOADNIL R%d - R%d' % (begin, end))
        
        return [node], False
    
    def _DecodeVararg(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = VarargInstruction()
        node.A = current_code.a
        node.B = current_code.b

        if current_code.b > 2:
            if self.enableLog: logger.info('\t>> VARARG R%d - R%d = ...' % (current_code.a, (current_code.a + current_code.b - 2)))
        elif current_code.b == 2:
            if self.enableLog: logger.info('\t>> VARARG R%d = ...' % current_code.a)
        elif current_code.b == 0:
            if self.enableLog: logger.info('\t>> VARARG R%d to top = ...' % current_code.a)
        else:
            raise RuntimeError('_DecodeVararg : invaild b value = %d' % current_code.b)
        
        return [node], False
    
    def _DecodeGetUpValue(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = GetUpvalInstruction()
        node.A = current_code.a
        node.B = current_code.b

        if self.enableLog: logger.info('\t>> GETUPVALUE R%d, U%d' % (current_code.a, current_code.b))

        return [node], False
    
    
    def _DecodeGetTabup(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = GettabupInstruction()
        node.A = current_code.a
        node.B = current_code.b
        node.C = CV(current_code.c)

        if CC(current_code.c):
            node.CConstMode = True
        else:
            node.CConstMode = False

        if CC(current_code.c):
            if self.enableLog: logger.info('\t>> GETTABUP R%d, U%d[K%d] (K = %s)' % (
                current_code.a, current_code.b, CV(current_code.c),
                str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> GETTABUP R%d, U%d[R%d]' % (
                current_code.a, current_code.b, CV(current_code.c)
            ))
        
        return [node], False
    
    def _DecodeGetTable(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = GettableInstruction()
        node.A = current_code.a
        node.B = current_code.b
        node.C = CV(current_code.c)

        if CC(current_code.c):
            node.CConstMode = True
        else:
            node.CConstMode = False

        if CC(current_code.c):
            if self.enableLog: logger.info('\t>> GETTABLE R%d, R%d[K%d] (K = %s)' % (
                current_code.a, current_code.b, CV(current_code.c),
                self.constants[CV(current_code.c)]
            ))
        else:
            if self.enableLog: logger.info('\t>> GETTABLE R%d, R%d[R%d]' % (
                current_code.a, current_code.b, CV(current_code.c)
            ))

        return [node], False
    
    def _DecodeSetTabup(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = SettabupInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False

        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SETTABUP U%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> SETTABUP U%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SETTABUP U%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> SETTABUP U%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))

        return [node], False
    
    def _DecodeSetUpVal(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = SetUpvalInstruction()
        node.A = current_code.a
        node.B = current_code.b

        if self.enableLog: logger.info('\t>> SETUPVAL R%d, U%d' % (current_code.a, current_code.b))

        return [node], False
    
    def _DecodeSetTable(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = SettableInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.BConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SETTABLE U%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> SETTABLE U%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SETTABLE U%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> SETTABLE U%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))

        return [node], False
    
    def _DecodeNewTable(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = NewtableInstruction()
        node.A = current_code.a
        
        if self.enableLog: logger.info('\t>> NEWTABLE R%d (size = %d, %d)' % (
            current_code.a, current_code.b, current_code.c
            ))
        
        return [node], False
    
    def _DecodeSelf(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = SelfInstruction()
        node.A = current_code.a
        node.B = current_code.b
        node.C = CV(current_code.c)

        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if (CC(current_code.c)):
            if self.enableLog: logger.info('\t>> SELF R%d, R%d, K%d (K = %s)' % (
                current_code.a, current_code.b, CV(current_code.c),
                self.constants[CV(current_code.c)]
            ))
        else:
            if self.enableLog: logger.info('\t>> SELF R%d, R%d, R%d' % (
                current_code.a, current_code.b, CV(current_code.c)
            ))
        
        return [node], False
    
    def _DecodeAdd(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = AddInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> ADD R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> ADD R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> ADD R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> ADD R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))

        return [node], False
    
    def _DecodeSub(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = SubInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SUB R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> SUB R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SUB R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> SUB R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False


    def _DecodeMul(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = MulInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> MUL R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> MUL R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> MUL R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> MUL R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False

    def _DecodeDiv(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = DivInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> DIV R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> DIV R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> DIV R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> DIV R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False
    
    def _DecodePow(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = PowInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> POW R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> POW R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> POW R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> POW R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False

    def _DecodeMod(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = ModInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> MOD R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> MOD R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> MOD R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> MOD R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False

    def _DecodeIdiv(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = IdivInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> IDIV R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> IDIV R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> IDIV R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> IDIV R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False

    def _DecodeBand(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = BandInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> BAND R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> BAND R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> BAND R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> BAND R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False

    def _DecodeBor(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = BorInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> BOR R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> BOR R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> BOR R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> BOR R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False

    def _DecodeBxor(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = BxorInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> BXOR R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> BXOR R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> BXOR R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> BXOR R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False

    def _DecodeShl(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = ShlInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SHL R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> SHL R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SHL R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> SHL R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False

    def _DecodeShr(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = ShrInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if (CC(current_code.b)):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if (CC(current_code.c)):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SHR R%d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> SHR R%d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)])
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> SHR R%d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)])
            ))
        else:
            if self.enableLog: logger.info('\t>> SHR R%d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        return [node], False
    
    def _DecodeUnm(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = UnmInstruction()
        node.A = current_code.a
        node.B = current_code.b

        if self.enableLog: logger.info('\t>> UNM R%d, R%d' % (current_code.a, current_code.b))
        return [node], False
    
    def _DecodeNot(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = NotInstruction()
        node.A = current_code.a
        node.B = current_code.b

        if self.enableLog: logger.info('\t>> NOT R%d, R%d' % (current_code.a, current_code.b))
        return [node], False
    
    def _DecodeLen(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = LenInstruction()
        node.A = current_code.a
        node.B = current_code.b

        if self.enableLog: logger.info('\t>> LEN R%d, R%d' % (current_code.a, current_code.b))
        return [node], False
    
    def _DecodeBnot(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = BnotInstruction()
        node.A = current_code.a
        node.B = current_code.b

        if self.enableLog: logger.info('\t>> BNOT R%d, R%d' % (current_code.a, current_code.b))
        return [node], False
    
    def _DecodeConcat(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = ConcatInstruction()
        node.A = current_code.a
        node.B = current_code.b
        node.C = current_code.c

        if self.enableLog: logger.info('\t>> CONCAT R%d, R%d, R%d' % (
            current_code.a, current_code.b, current_code.c
            ))
        
        return [node], False
    
    def _DecodeJmp(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = JmpInstruction()
        node.A = current_code.a
        node.sBx = current_code.sbx
        node.SetJmpOffset(current_pc + current_code.sbx + 1)
        
        if self.enableLog: logger.info('\t>> JMP %d (Offset : %d)' % (
            current_pc + current_code.sbx + 1, current_code.sbx
        ))
        
        return [node], False
    
    def _DecodeEq(self, current_pc, current_code, next_code_str, nextCodeIndex = None):
        if next_code_str == None:
            raise ValueError('next_code cannot be none in _DecodeEq')
        
        next_code_ins = LuaByteCode(self.instructionSize, self.isBE)
        next_opcode_name, next_instruction_len, next_code = next_code_ins.Decode(next_code_str, 0, nextCodeIndex)

        node = EqInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if CC(current_code.b):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if CC(current_code.c):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        subnode = ExtraargInstruction()
        subnode.sBx = next_code.sbx

        node.SetLikelyPCOffset(current_pc + 2)
        node.SetUnlikelyPCOffset(next_code.sbx + current_pc + 2)

        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> EQ %d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)]),
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> EQ %d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)]),
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> EQ %d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
            ))
        else:
            if self.enableLog: logger.info('\t>> EQ %d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))

        current_op = None
        if current_code.a != 0:
            current_op = disasm_invopstr(LuaInstructionOperation.NODE_EQ)
        else:
            current_op = disasm_opstr(LuaInstructionOperation.NODE_EQ)
        
        opstr_1 = None
        if CC(current_code.b):
            opstr_1 = 'K%d' % CV(current_code.b)
        else:
            opstr_1 = 'R%d' % CV(current_code.b)
        
        opstr_2 = None
        if CC(current_code.b):
            opstr_2 = 'K%d' % CV(current_code.c)
        else:
            opstr_2 = 'R%d' % CV(current_code.c)
        
        if self.enableLog: logger.info('\t>>>> if %s %s %s then goto %d else goto %d' % (
            opstr_1, current_op, opstr_2, current_pc + 2, current_pc + 2 + next_code.sbx
        ))

        if self.enableLog: logger.info('\t>> EXTRAARG %d' % next_code.sbx)

        return [node, subnode], True

    def _DecodeLt(self, current_pc, current_code, next_code_str, nextCodeIndex = None):
        if next_code_str == None:
            raise ValueError('next_code cannot be none in _DecodeLt')
        
        next_code_ins = LuaByteCode(self.instructionSize, self.isBE)
        next_opcode_name, next_instruction_len, next_code = next_code_ins.Decode(next_code_str, 0, nextCodeIndex)
    
        node = LtInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if CC(current_code.b):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if CC(current_code.c):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        subnode = ExtraargInstruction()
        subnode.sBx = next_code.sbx

        node.SetLikelyPCOffset(current_pc + 2)
        node.SetUnlikelyPCOffset(next_code.sbx + current_pc + 2)


        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> LT %d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)]),
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            print(CV(current_code.c), current_code.c)
            if self.enableLog: logger.info('\t>> LT %d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)]),
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> LT %d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
            ))
        else:
            if self.enableLog: logger.info('\t>> LT %d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))

        current_op = None
        if current_code.a != 0:
            current_op = disasm_invopstr(LuaInstructionOperation.NODE_LT)
        else:
            current_op = disasm_opstr(LuaInstructionOperation.NODE_LT)
        
        opstr_1 = None
        if CC(current_code.b):
            opstr_1 = 'K%d' % CV(current_code.b)
        else:
            opstr_1 = 'R%d' % CV(current_code.b)
        
        opstr_2 = None
        if CC(current_code.b):
            opstr_2 = 'K%d' % CV(current_code.c)
        else:
            opstr_2 = 'R%d' % CV(current_code.c)
        
        if self.enableLog: logger.info('\t>>>> if %s %s %s then goto %d else goto %d' % (
            opstr_1, current_op, opstr_2, current_pc + 2, current_pc + 2 + next_code.sbx
        ))

        if self.enableLog: logger.info('\t>> EXTRAARG %d' % next_code.sbx)

        return [node, subnode], True

    def _DecodeLe(self, current_pc, current_code, next_code_str, nextCodeIndex = None):
        if next_code_str == None:
            raise ValueError('next_code cannot be none in _DecodeLe')
        
        next_code_ins = LuaByteCode(self.instructionSize, self.isBE)
        next_opcode_name, next_instruction_len, next_code = next_code_ins.Decode(next_code_str, 0, nextCodeIndex)

        node = EqInstruction()
        node.A = current_code.a
        node.B = CV(current_code.b)
        node.C = CV(current_code.c)

        if CC(current_code.b):
            node.BConstMode = True
        else:
            node.BConstMode = False
        
        if CC(current_code.c):
            node.CConstMode = True
        else:
            node.CConstMode = False
        
        subnode = ExtraargInstruction()
        subnode.sBx = next_code.sbx

        node.SetLikelyPCOffset(current_pc + 2)
        node.SetUnlikelyPCOffset(next_code.sbx + current_pc + 2)

        if   CC(current_code.b) and CC(current_code.c):
            if self.enableLog: logger.info('\t>> LE %d, K%d, K%d (K%d = %s, K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
                CV(current_code.c), str(self.constants[CV(current_code.c)]),
            ))
        elif CC(current_code.b) == False and CC(current_code.c):
            if self.enableLog: logger.info('\t>> LE %d, R%d, K%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.c), str(self.constants[CV(current_code.c)]),
            ))
        elif CC(current_code.b) and CC(current_code.c) == False:
            if self.enableLog: logger.info('\t>> LE %d, K%d, R%d (K%d = %s)' % (
                current_code.a, CV(current_code.b), CV(current_code.c),
                CV(current_code.b), str(self.constants[CV(current_code.b)]),
            ))
        else:
            if self.enableLog: logger.info('\t>> LE %d, R%d, R%d' % (
                current_code.a, CV(current_code.b), CV(current_code.c)
            ))
        
        current_op = None
        if current_code.a != 0:
            current_op = disasm_invopstr(LuaInstructionOperation.NODE_LE)
        else:
            current_op = disasm_opstr(LuaInstructionOperation.NODE_LE)
        
        opstr_1 = None
        if CC(current_code.b):
            opstr_1 = 'K%d' % CV(current_code.b)
        else:
            opstr_1 = 'R%d' % CV(current_code.b)
        
        opstr_2 = None
        if CC(current_code.b):
            opstr_2 = 'K%d' % CV(current_code.c)
        else:
            opstr_2 = 'R%d' % CV(current_code.c)
        
        if self.enableLog: logger.info('\t>>>> if %s %s %s then goto %d else goto %d' % (
            opstr_1, current_op, opstr_2, current_pc + 2, current_pc + 2 + next_code.sbx
        ))

        if self.enableLog: logger.info('\t>> EXTRAARG %d' % next_code.sbx)
        
        return [node, subnode], True

    def _DecodeTest(self, current_pc, current_code, next_code_str, nextCodeIndex = None):
        if next_code_str == None:
            raise ValueError('next_code cannot be none in _DecodeTest')
        
        next_code_ins = LuaByteCode(self.instructionSize, self.isBE)
        next_opcode_name, next_instruction_len, next_code = next_code_ins.Decode(next_code_str, 0, nextCodeIndex)

        node = TestInstruction()
        node.A = current_code.a
        node.C = current_code.c
        
        subnode = ExtraargInstruction()
        subnode.sBx = next_code.sbx

        node.SetLikelyPCOffset(current_pc + 2)
        node.SetUnlikelyPCOffset(next_code.sbx + current_pc + 2)
        
        if self.enableLog: logger.info('\t>> TEST R%d, %d' % (current_code.a, current_code.c))

        opstr = ''
        if current_code.c != 0:
            opstr = 'not '

        if self.enableLog: logger.info('\t>>>> if %sR%d then goto %d else goto %d' % (
            opstr, current_code.a, current_pc + 2, current_pc + 2 + next_code.sbx
        ))
        if self.enableLog: logger.info('\t>> EXTRAARG %d' % next_code.sbx)

        return [node, subnode], True
    
    def _DecodeTestSet(self, current_pc, current_code, next_code_str, nextCodeIndex = None):
        '''
        if (R(B) <=> C) then R(A) := R(B) else pc++
        '''
        if next_code_str == None:
            raise ValueError('next_code cannot be none in _DecodeTestSet')
        
        next_code_ins = LuaByteCode(self.instructionSize, self.isBE)
        next_opcode_name, next_instruction_len, next_code = next_code_ins.Decode(next_code_str, 0, nextCodeIndex)

        node = TestsetInstruction()
        node.A = current_code.a
        node.B = current_code.b
        node.C = current_code.c
        
        subnode = ExtraargInstruction()
        subnode.sBx = next_code.sbx
        
        node.SetLikelyPCOffset(current_pc + 2)
        node.SetUnlikelyPCOffset(next_code.sbx + current_pc + 2)
        
        if self.enableLog: logger.info('\t>> TESTSET R%d, R%d, %d' % (current_code.a, current_code.b, current_code.c))
        
        opstr = ''
        if current_code.c != 0:
            opstr = 'not '
        
        if self.enableLog: logger.info('\t>>>> if %sR%d then R%d := R%d ; goto %d else goto %d' % (
            opstr, current_code.b, current_code.a, current_code.b,
            current_pc + next_code.sbx + 2, current_pc + 2
        ))

        if self.enableLog: logger.info('\t>> EXTRAARG %d' % next_code.sbx)
        
        return [node, subnode], True
        
    def _DecodeCall(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = CallInstruction()
        
        node.A = current_code.a
        node.B = current_code.b
        node.C = current_code.c

        if self.enableLog: logger.info('\t>> CALL R%d, %d, %d' % (
            current_code.a, current_code.b, current_code.c
        ))

        call_str = None
        if current_code.b > 2:
            call_str = 'R%d to R%d' % (current_code.a + 1, 
            current_code.a + current_code.b - 1)
        #only one
        elif current_code.b == 2:
            call_str = 'R%d' % (current_code.a + 1)
        #none
        elif current_code.b == 1:
            call_str = 'void'
        #from a+1 to top
        elif current_code.b == 0:
            call_str = 'R%d to top' % (current_code.a + 1)
        
        result_str = None
        if current_code.c > 2:
            result_str = 'R%d to R%d' % (current_code.a, 
            current_code.a + current_code.c - 2)
        elif current_code.c == 2:
            result_str = 'R%d' % (current_code.a)
        elif current_code.c == 1:
            result_str = 'void'
        elif current_code.c == 0:
            result_str = 'R%d to top' % (current_code.a)

        if self.enableLog: logger.info('\t>>>> %s = R%d(%s)' % (
            result_str, current_code.a, call_str
        ))
        
        return [node], False

    def _DecodeTailCall(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        return self._DecodeCall(current_pc, current_code, next_code_str, nextCodeIndex)
    
    def _DecodeReturn(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = ReturnInstruction()
        
        node.A = current_code.a
        node.B = current_code.b
        
        if self.enableLog: logger.info('\t>> RETURN R%d %d' % (
            current_code.a, current_code.a + current_code.b - 2
        ))

        result_str = None
        if current_code.b > 2:
            result_str = 'R%d to R%d' % (
                current_code.a, current_code.a + current_code.b - 2
            )
        elif current_code.b == 2:
            result_str = 'R%d' % current_code.a
        elif current_code.b == 1:
            result_str = 'void'
        elif current_code.b == 0:
            result_str = 'R%d to top' % current_code.a
        
        if self.enableLog: logger.info('\t>>>> return %s' % result_str)

        return [node], False
    
    def _DecodeForLoop(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = ForloopInstruction()
        
        node.A   = current_code.a
        node.sBx = current_code.sbx

        node.SetLikelyPCOffset(current_code.sbx + current_pc + 1)
        node.SetUnlikelyPCOffset(current_pc + 1)

        if self.enableLog: logger.info('\t>> FORLOOP R%d, %d' % (current_code.a, current_code.sbx))
        if self.enableLog: logger.info('\t>>>>> R%d += R%d; if R%d <= R%d then R%d := R%d; PC += %d , goto %d end' % (
            current_code.a, current_code.a+2, current_code.a, 
            current_code.a+1, current_code.a+3, current_code.a, 
            current_code.sbx, current_pc + current_code.sbx + 1
        ))

        return [node], False
    
    def _DecodeForRep(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = ForrepInstruction()

        node.A   = current_code.a
        node.sBx = current_code.sbx

        node.SetJmpOffset(current_pc + current_code.sbx + 1)

        if self.enableLog: logger.info('\t>> FORREP R%d, %d' % (current_code.a, current_code.sbx))
        if self.enableLog: logger.info('\t>>>> R%d -= R%d; pc += %d (goto %d)' % (
            current_code.a, current_code.a+2, current_code.sbx,
            current_pc + current_code.sbx + 1
        ))
        return [node], False
    
    # TFORCALL
    def _DecodeTForCall(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = None

        if self.enableLog: logger.info('TFORCALL R%d, %d' % (current_code.a, current_code.c))

        iter_list_str = None
        node = TforcallInstruction()
        node.A = current_code.a
        node.C = current_code.c

        if self.enableLog: logger.info('\t>>>> %s := R%d(R%d,R%d)' % (
            iter_list_str, current_code.a, current_code.a + 1, current_code.a + 2
        ))
    
        return [node], False
    
    def _DecodeTForLoop_OLD(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        '''
        similar to TFORCALL in lua5.2 or higher
        == Lua 5.1 ==
        generic for loop
        A C	R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2));
        if R(A+3) ~= nil then R(A+2)=R(A+3) else pc++
        '''
        node = TforloopXInstruction()
        node.A = current_code.a
        node.C = current_code.c

        node.SetLikelyPCOffset(current_pc + 1)
        node.SetUnlikelyPCOffset(current_pc + 2) #end of the loop
        return [node], False
    
    def _DecodeTForLoop_NEW(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = TforloopInstruction()

        node.A   = current_code.a
        node.sBx = current_code.sbx

        node.SetLikelyPCOffset(current_pc + current_code.sbx + 1)
        node.SetUnlikelyPCOffset(current_pc + 1)

        if self.enableLog: logger.info('\t>> TFORCALL R%d %d' % (current_code.a, current_code.sbx))
        if self.enableLog: logger.info('\t>>>> if R%d ~= nil then { R%d := R%d ; pc += %d (goto %d) }' % (
            current_code.a + 1, current_code.a, current_code.a+1, 
            current_code.sbx, current_pc + current_code.sbx + 1
        ))
        return [node], False
    
    def _DecodeTForLoop(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        if self.version == LuaVersion.LuaVersion51:
            return self._DecodeTForLoop_OLD(current_pc, current_code, next_code_str)
        
        return self._DecodeTForLoop_NEW(current_pc, current_code, next_code_str)
    
    def _DecodeSetList_OLD(self, current_pc, current_code, next_code_str):
        node    = SetlistInstruction()
        subnode = None
        value_c = current_code.c

        node.A = current_code.a
        node.B = current_code.b
        node.C = current_code.c

        if self.enableLog: logger.info('\t>> SETLIST R%d %d %d' % (
            current_code.a, current_code.b, current_code.c
        ))

        if value_c == 0:
            if next_code_str == None:
                raise RuntimeError('_DecodeSetList : c -> 0, but next_code_str -> None')
            
            subnode = RawInstruction()
            nextValue = 0
            if self.instructionSize == 4:
                if self.isBE == False:
                    nextValue = unpack('<L', next_code_str[0:4])[0]
                else:
                    nextValue = unpack('>L', next_code_str[0:4])[0]
            else:
                if self.isBE == False:
                    nextValue = unpack('<Q', next_code_str[0:8])[0]
                else:
                    nextValue = unpack('>Q', next_code_str[0:8])[0]
                
            subnode.Value = nextValue
            value_c = nextValue
            node.C  = nextValue
        
        if subnode:
            node.SetSkipNext(True)
            return [node, subnode], True
        
        return [node], False
    
    def _DecodeSetList_NEW(self, current_pc, current_code, next_code_str):
        node    = SetlistInstruction()
        subnode = None
        value_c = current_code.c

        node.A = current_code.a
        node.B = current_code.b
        node.C = current_code.c

        if self.enableLog: logger.info('\t>> SETLIST R%d %d %d' % (
            current_code.a, current_code.b, current_code.c
        ))

        if value_c == 0:
            if next_code_str == None:
                raise RuntimeError('_DecodeSetList : c -> 0, but next_code_str -> None')
            
            subnode = ExtraargInstruction()
            
            next_code_ins = LuaByteCode(self.instructionSize, self.isBE)
            next_opcode_name, next_instruction_len, next_code = next_code_ins.Decode(next_code_str, 0)
            subnode.sBx = (next_code.ax)
            value_c = next_code.ax
            node.C  = next_code.ax
        
        if subnode:
            node.SetSkipNext(True)
            return [node, subnode], True
        
        return [node], False
    
    def _DecodeSetList(self, current_pc, current_code, next_code_str, nextCodeIndex = None):
        if self.version == LuaVersion.LuaVersion51:
            return self._DecodeSetList_OLD(current_pc, current_code, next_code_str)
        
        return self._DecodeSetList_NEW(current_pc, current_code, next_code_str)
    
    def _DecodeClosure(self, current_pc, current_code, next_code_str = None, nextCodeIndex = None):
        node = ClosureInstruction()
        node.A  = current_code.a
        node.Bx = current_code.bx
        
        if self.enableLog: logger.info('\t>> CLOSURE R%d, %d' % (
            current_code.a, current_code.bx
        ))
        return [node], False