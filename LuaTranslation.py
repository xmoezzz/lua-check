#bytecode -> ssa form

from __future__ import print_function
import logging
import copy
from LuaByteCode import *
from LuaMiddleLang import *
from LuaVar import *
from VarEngine import VarEngine
from Graph import GraphStep
from LnEnum import LuaVersion
from LuaLinearOptimizer import LuaLinearOptimizer
from LuaLinearBackend   import LuaLinearBackend

class VarHashObject(object):
    def __init__(self, var, ref = 1):
        self.var = var
        self.ref = ref

class LuaTranslate(object):
    def __init__(self, instructions, constants, upvalues, function, version):
        self.instructions = instructions
        self.constants    = constants
        self.upvalues     = upvalues
        self.function     = function
        self.version      = version
        self.mlils    = []
        self._ssaCalc = {}
        self._ssaUpvalCalc = {}
        self._ssaGCalc= {}
        self._bbCache = {}
        self._curIdx  = 0
        self.VarEngine = VarEngine()
        self.rootBlock = None
        self.basicBlocks = []
        self.varDefine = {}
        self.varUsage  = {}
        
    
    def _InsertBasicBlockCache(self, offset, bb):
        if not isinstance(bb, MiddleBasicBlock):
            raise TypeError('the type of bb must be MiddleBasicBlock')
        if offset in self._bbCache:
            return False
        
        self._bbCache[offset] = bb
        return True
    
    def _OverrideBasicBlockCache(self, offset, bb):
        if not isinstance(bb, MiddleBasicBlock):
            raise TypeError('the type of bb must be MiddleBasicBlock')
        self._bbCache[offset] = bb
    
    def _FindBasicBlockCache(self, offset):
        if offset in self._bbCache:
            return self._bbCache[offset]
        return None
    
    def _FindBasicBlockOffset(self, goffset):
        '''
        return value:
        bool   : found or not
        object : BasicBlock
        int    : offset (in current bb)
        '''

        instr = self.instructions[goffset]
        first_mlil = instr.GetMlil()
        if first_mlil == None:
            return False, None, None
        
        bb = first_mlil.GetBasicBlock()
        idx = 0
        success = False
        for mi in bb.instructions:
            if mi == first_mlil:
                success = True
                break
            idx += 1
        
        if success == False:
            raise RuntimeError('Unable to find instruction offset in current basic block')
        
        return True, bb, idx
    
    def _BasicBlockIsNotProcessed(self, offset):
        bb = self._FindBasicBlockCache(offset)
        if bb == None:
            return True
        
        if bb.processed == False:
            return True
        
        return False
    
    def _SplitBasicBlock(self, bb, offset, goffset):
        '''
        |       |     |    |
        |       | ==> |____|
        |       |       |
        |_______|     |____|
        '''
        if offset == 0:
            raise RuntimeError('offset cannot be zero...')
        
        up_parts  = bb.instructions[:offset]
        down_parts= bb.instructions[offset:]
        
        if len(up_parts) == 0:
            raise RuntimeError('up part is empty')
        if len(down_parts) == 0:
            raise RuntimeError('down part is empty')
        
        up_bb = MiddleBasicBlock(self.function, bb.address)
        up_bb.instructions = up_parts
        up_bb.function     = self.function
        up_bb.address      = bb.address
        up_bb.incoming_edges = bb.incoming_edges
        up_bb.processed    = True
        
        down_bb = MiddleBasicBlock(self.function, goffset)
        down_bb.instructions = down_parts
        down_bb.function     = self.function
        down_bb.address      = goffset
        down_bb.outgoing_edges = bb.outgoing_edges
        down_bb.processed    = True

        down_bb.incoming_edges.append(up_bb)
        up_bb.outgoing_edges.append(down_bb)

        self._OverrideBasicBlockCache(bb.address, up_bb)
        self._OverrideBasicBlockCache(goffset,    down_bb)
        
        self.basicBlocks.remove(bb)
        if self.rootBlock == bb:
            self.rootBlock = up_bb
        
        self.basicBlocks.extend([up_bb, down_bb])

        return down_bb
        
    
    def _BasicBlockFrontInsert(self, bb, intr):
        '''
        for phi instruction generation
        '''
        pass
    
    def _InsertBasicBlockWithSech(self, current_bb, current_instr, one_node_offset, right_node_offset):
        '''
        LOADBOOL Only

        for LOODBOOL-like ops
               |___________|
                /        \\
            |_1 node_| --> |______|
        '''
        
        #left_bb = self._FindBasicBlockCache(one_node_offset)
        #if left_bb == None:

        #DO NOT ADD IT TO CACHE
        left_bb = MiddleBasicBlock(self.function, one_node_offset)
        self.basicBlocks.append(left_bb)
        self._InsertBasicBlockCache(one_node_offset, left_bb)

        current_bb.outgoing_edges.append(left_bb)
        left_bb.incoming_edges.append(current_bb)
        self._ConvertCodeWithSech(left_bb, one_node_offset, 1)

        right_bb = self._FindBasicBlockCache(right_node_offset)
        if right_bb == None:
            success, ori_bb, mi_offset = self._FindBasicBlockOffset(right_node_offset)
            if success == False:
                right_bb = MiddleBasicBlock(self.function, right_node_offset)
                self.basicBlocks.append(right_bb)
                self._InsertBasicBlockCache(right_node_offset, right_bb)

                right_bb.incoming_edges.append(current_bb)
            else:
                right_bb = self._SplitBasicBlock(ori_bb, mi_offset, right_node_offset)
                right_bb.incoming_edges.append(current_bb)

        current_bb.outgoing_edges.append(right_bb)
        left_bb.outgoing_edges.append(right_bb)

        current_instr.SetLikelyBlock(left_bb)
        current_instr.SetUnlikelyBlock(right_bb)

        if self._BasicBlockIsNotProcessed(right_node_offset):
            self._ConvertCodeWithSech(right_bb, right_node_offset)
    
    def _InsertBasicBlockForNode(self, current_bb, current_pc, current_instr, dangling_instr, left_offset, right_offset):
        
        #DO NOT ADD IT TO CACHE!!!
        dangling_bb = MiddleBasicBlock(self.function, current_pc)
        dangling_instr.SetBasicBlock(dangling_bb)
        self.basicBlocks.append(dangling_bb)
        dangling_instr.SetAddress(current_pc)
        dangling_instr.SetIndex(self._curIdx)
        self._curIdx += 1

        self.mlils.append(dangling_instr)
        dangling_bb.instructions.append(dangling_instr)

        jmp_instr = JmpMiddleInstruction()
        jmp_instr.SetBasicBlock(current_bb)
        jmp_instr.SetJmpOffset(left_offset)
        jmp_instr.SetAddress(current_pc)
        jmp_instr.SetIndex(self._curIdx)
        jmp_instr.SetBasicBlock(dangling_bb)
        self._curIdx += 1

        left_bb = self._FindBasicBlockCache(left_offset)
        if left_bb == None:
            success, ori_bb, mi_offset = self._FindBasicBlockOffset(left_offset)
            if success == False:
                left_bb = MiddleBasicBlock(self.function, left_offset)
                self.basicBlocks.append(left_bb)
                self._InsertBasicBlockCache(left_offset, left_bb)

                left_bb.incoming_edges.append(dangling_bb)
            else:
                left_bb = self._SplitBasicBlock(ori_bb, mi_offset, left_offset)
                left_bb.incoming_edges.append(dangling_bb)
        
        jmp_instr.SetJmpNode(left_bb)

        self.mlils.append(jmp_instr)
        dangling_bb.instructions.append(jmp_instr)

        current_bb.outgoing_edges.append(dangling_bb)
        dangling_bb.incoming_edges.append(current_bb)
        
        dangling_bb.outgoing_edges.append(left_bb)

        right_bb = self._FindBasicBlockCache(right_offset)
        if right_bb == None:
            success, ori_bb, mi_offset = self._FindBasicBlockOffset(right_offset)
            if success == False:
                right_bb = MiddleBasicBlock(self.function, right_offset)
                self.basicBlocks.append(right_bb)
                self._InsertBasicBlockCache(right_offset, right_bb)

                right_bb.incoming_edges.append(current_bb)
            else:
                right_bb = self._SplitBasicBlock(ori_bb, mi_offset, right_offset)
                right_bb.incoming_edges.append(current_bb)
        
        current_bb.outgoing_edges.append(right_bb)

        current_instr.SetLikelyBlock(dangling_bb)
        current_instr.SetUnlikelyBlock(right_bb)

        if self._BasicBlockIsNotProcessed(left_offset):
            self._ConvertCodeWithSech(left_bb,  left_offset)
        
        if self._BasicBlockIsNotProcessed(right_offset):
            self._ConvertCodeWithSech(right_bb, right_offset)
    
    def _InsertBasicBlockSetNode(self, current_bb, current_pc, current_instr, dangling_instr, left_offset, right_offset):
        '''
        if (R(B) <=> C) then R(A) := R(B) else pc++
        
                |________|
                /        \\
            |_MOV_|     |_____|
               |
            |_____|
        '''

        #DO NOT ADD IT TO CACHE!!!
        dangling_bb = MiddleBasicBlock(self.function, current_pc)
        self.basicBlocks.append(dangling_bb)

        dangling_instr.SetAddress(current_pc)
        dangling_instr.SetIndex(self._curIdx)
        dangling_instr.SetBasicBlock(dangling_bb)
        self._curIdx += 1
        
        self.mlils.append(dangling_instr)

        dangling_bb.instructions.append(dangling_instr)
        dangling_bb.incoming_edges.append(current_bb)
        current_bb.outgoing_edges.append(dangling_bb)

        left_bb = self._FindBasicBlockCache(left_offset)
        if left_bb == None:
            success, ori_bb, mi_offset = self._FindBasicBlockOffset(left_offset)
            if success == False:
                left_bb = MiddleBasicBlock(self.function, left_offset)
                self.basicBlocks.append(left_bb)
                self._InsertBasicBlockCache(left_offset, left_bb)

                left_bb.incoming_edges.append(dangling_bb)
            else:
                left_bb = self._SplitBasicBlock(ori_bb, mi_offset, left_offset)
                left_bb.incoming_edges.append(dangling_bb)
        
        dangling_bb.outgoing_edges.append(left_bb)
        
        right_bb = self._FindBasicBlockCache(right_offset)
        if right_bb == None:
            success, ori_bb, mi_offset = self._FindBasicBlockOffset(right_offset)
            if success == False:
                right_bb = MiddleBasicBlock(self.function, right_offset)
                self.basicBlocks.append(right_bb)
                self._InsertBasicBlockCache(right_offset, right_bb)

                right_bb.incoming_edges.append(current_bb)
            else:
                right_bb = self._SplitBasicBlock(ori_bb, mi_offset, right_offset)
                right_bb.incoming_edges.append(current_bb)
        
        current_bb.outgoing_edges.append(right_bb)

        current_instr.SetLikelyBlock(dangling_bb)
        current_instr.SetUnlikelyBlock(right_bb)

        if self._BasicBlockIsNotProcessed(left_offset):
            self._ConvertCodeWithSech(left_bb,  left_offset)
        
        if self._BasicBlockIsNotProcessed(right_offset):
            self._ConvertCodeWithSech(right_bb, right_offset)

    def _InsertBasicBlockNormal(self, current_bb, current_instr, left_offset, right_offset):
        '''
        for je-like ops
                |__________|
                /         \\
            |_likely_|  |_unlikely_|
        '''
        
        left_bb = self._FindBasicBlockCache(left_offset)
        if left_bb == None:
            success, ori_bb, mi_offset = self._FindBasicBlockOffset(left_offset)
            if success == False:
                left_bb = MiddleBasicBlock(self.function, left_offset)
                self.basicBlocks.append(left_bb)
                self._InsertBasicBlockCache(left_offset, left_bb)
            
                left_bb.incoming_edges.append(current_bb)
            else:
                left_bb = self._SplitBasicBlock(ori_bb, mi_offset, left_offset)
                left_bb.incoming_edges.append(current_bb)
        
        current_bb.outgoing_edges.append(left_bb)

        right_bb = self._FindBasicBlockCache(right_offset)
        if right_bb == None:
            success, ori_bb, mi_offset = self._FindBasicBlockOffset(right_offset)
            if success == False:
                right_bb = MiddleBasicBlock(self.function, right_offset)
                self.basicBlocks.append(right_bb)
                self._InsertBasicBlockCache(right_offset, right_bb)
            
                right_bb.incoming_edges.append(current_bb)
            else:
                right_bb = self._SplitBasicBlock(ori_bb, mi_offset, right_offset)
                right_bb.incoming_edges.append(current_bb)
        
        current_bb.outgoing_edges.append(right_bb)

        current_instr.SetLikelyBlock(left_bb)
        current_instr.SetUnlikelyBlock(right_bb)

        if self._BasicBlockIsNotProcessed(left_offset):
            self._ConvertCodeWithSech(left_bb,  left_offset)
        
        if self._BasicBlockIsNotProcessed(right_offset):
            self._ConvertCodeWithSech(right_bb, right_offset)
    
    def _InsertBasicBlockJmp(self, CurrentBB, next_offset):
        next_bb = self._FindBasicBlockCache(next_offset)
        if next_bb == None:
            success, ori_bb, mi_offset = self._FindBasicBlockOffset(next_offset)
            if success == False:
                next_bb = MiddleBasicBlock(self.function, next_offset)
                self.basicBlocks.append(next_bb)
                self._InsertBasicBlockCache(next_offset, next_bb)
            
                next_bb.incoming_edges.append(CurrentBB)
            else:
                next_bb = self._SplitBasicBlock(ori_bb, mi_offset, next_offset)
                next_bb.incoming_edges.append(CurrentBB)
        
        CurrentBB.outgoing_edges.append(next_bb)

        if self._BasicBlockIsNotProcessed(next_offset):
            self._ConvertCodeWithSech(next_bb, next_offset)

    def CollectLeftBodyVariable(self, bb, varlist):
        #in 2pass
        for instr in bb.instructions:
            op = instr.GetOperation()

            left = None
            left_list = []
            is_left_list = False
            if op in (
                    LuaMiddleOperation.NODE_MOVE,
                    LuaMiddleOperation.NODE_MOVV,
                    LuaMiddleOperation.NODE_GETUPVAL,
                    LuaMiddleOperation.NODE_GETTABUPR,
                    LuaMiddleOperation.NODE_GETTABUPC,
                    LuaMiddleOperation.NODE_GETTABLER,
                    LuaMiddleOperation.NODE_GETTABLEC,
                    LuaMiddleOperation.NODE_SETTABUPRR,
                    LuaMiddleOperation.NODE_SETTABUPCC,
                    LuaMiddleOperation.NODE_SETTABUPCR,
                    LuaMiddleOperation.NODE_SETTABUPRC,
                    LuaMiddleOperation.NODE_SETUPVAL,
                    LuaMiddleOperation.NODE_SETTABLECC,
                    LuaMiddleOperation.NODE_SETTABLERR,
                    LuaMiddleOperation.NODE_SETTABLECR,
                    LuaMiddleOperation.NODE_SETTABLERC,
                    LuaMiddleOperation.NODE_SELFR,
                    LuaMiddleOperation.NODE_UNM,
                    LuaMiddleOperation.NODE_NOT,
                    LuaMiddleOperation.NODE_LEN,
                    LuaMiddleOperation.NODE_BNOT,
                    LuaMiddleOperation.NODE_CONCAT,
                    LuaMiddleOperation.NODE_CLOSURE
                    ):
                left = instr.GetDestVar()
            elif op in (
                    LuaMiddleOperation.NODE_ADDCC,
                    LuaMiddleOperation.NODE_ADDRR,
                    LuaMiddleOperation.NODE_ADDCR,
                    LuaMiddleOperation.NODE_ADDRC,
                    LuaMiddleOperation.NODE_SUBCC,
                    LuaMiddleOperation.NODE_SUBRR,
                    LuaMiddleOperation.NODE_SUBCR,
                    LuaMiddleOperation.NODE_SUBRC,
                    LuaMiddleOperation.NODE_MULCC,
                    LuaMiddleOperation.NODE_MULRR,
                    LuaMiddleOperation.NODE_MULCR,
                    LuaMiddleOperation.NODE_MULRC,
                    LuaMiddleOperation.NODE_DIVCC,
                    LuaMiddleOperation.NODE_DIVRR,
                    LuaMiddleOperation.NODE_DIVCR,
                    LuaMiddleOperation.NODE_DIVRC,
                    LuaMiddleOperation.NODE_POWCC,
                    LuaMiddleOperation.NODE_POWRR,
                    LuaMiddleOperation.NODE_POWCR,
                    LuaMiddleOperation.NODE_POWRC,
                    LuaMiddleOperation.NODE_MODCC,
                    LuaMiddleOperation.NODE_MODRR,
                    LuaMiddleOperation.NODE_MODCR,
                    LuaMiddleOperation.NODE_MODRC,
                    LuaMiddleOperation.NODE_IDIVCC,
                    LuaMiddleOperation.NODE_IDIVRR,
                    LuaMiddleOperation.NODE_IDIVCR,
                    LuaMiddleOperation.NODE_IDIVRC,
                    LuaMiddleOperation.NODE_BANDCC,
                    LuaMiddleOperation.NODE_BANDRR,
                    LuaMiddleOperation.NODE_BANDCR,
                    LuaMiddleOperation.NODE_BANDRC,
                    LuaMiddleOperation.NODE_BORCC,
                    LuaMiddleOperation.NODE_BORRR,
                    LuaMiddleOperation.NODE_BORCR,
                    LuaMiddleOperation.NODE_BORRC,
                    LuaMiddleOperation.NODE_BXORCC,
                    LuaMiddleOperation.NODE_BXORRR,
                    LuaMiddleOperation.NODE_BXORCR,
                    LuaMiddleOperation.NODE_BXORRC,
                    LuaMiddleOperation.NODE_SHLCC,
                    LuaMiddleOperation.NODE_SHLRR,
                    LuaMiddleOperation.NODE_SHLCR,
                    LuaMiddleOperation.NODE_SHLRC,
                    LuaMiddleOperation.NODE_SHRCC,
                    LuaMiddleOperation.NODE_SHRRR,
                    LuaMiddleOperation.NODE_SHRCR,
                    LuaMiddleOperation.NODE_SHRRC
                    ):
                left = instr.GetDestVal()
            elif op in (
                    LuaMiddleOperation.NODE_CALLU,
                    LuaMiddleOperation.NODE_TFORCALL
                    ):
                is_left_list = True
                left_list = instr.GetDest()
            
            if is_left_list:
                for left_item in left_list:
                    if str(left_item) in varlist:
                        varlist[str(left_item)].ref += 1
                    else:
                        h = VarHashObject(left_item)
                        varlist[str(left_item)] = h
            else:
                if left == None:
                    continue
                
                if str(left) in varlist:
                    varlist[str(left)].ref += 1
                else:
                    h = VarHashObject(left)
                    varlist[str(left)] = h
        #end for
        #lazy (linear) algorithm, i don't know variable wiil be used in 
        #TODO
    
    def InsertPhiNode(self, CurrentBB):
        if len(CurrentBB.incoming_edges) < 2:
            return
        
        if len(CurrentBB.incoming_edges) > 2:
            #panic
            raise RuntimeError('panic : len(incoming_edges) > 2')
        
        if CurrentBB.IsPhiCalculated():
            return
        
        varlist = {}
        for bb in CurrentBB.incoming_edges:
            self.CollectLeftBodyVariable(bb, varlist)
        
        CurrentBB.SetPhiCalculated()
    
    def _LinkWithChildBasicBlock(self, CurrentBB, child_bb):
        '''
        only called from _ConvertCodeWithSech
        '''
        CurrentBB.outgoing_edges.append(child_bb)

    def _ConvertCodeWithSech(self, CurrentBB, offset, limit = -1):

        if CurrentBB.processed == True:
            raise RuntimeError('offset : 0x%0x, basic block is processed!!!' % offset)
        
        CurrentBB.processed = True
        instruction = self.instructions[offset]
        if limit == 0:
            raise RuntimeError('Invalid limit')

        parsedCnt = 0
        if limit == -1:
            while True:
                status = False
                next_offset = -1
                if instruction.IsForceSkip() == False:
                    status, next_offset = self._ConvertCode(CurrentBB, instruction, offset)
                    parsedCnt += 1
                else:
                    next_offset = offset + 1
                    status = True
                
                if status == False:
                    break
                offset = next_offset
                instruction = self.instructions[offset]

                #at least one instruction is decoded
                child_bb = self._FindBasicBlockCache(offset)
                if child_bb != None:
                    self._LinkWithChildBasicBlock(CurrentBB, child_bb)
                    #exit this loop because we reach the terminal node
                    break
                
        else:
            #will not reach terminal node here?
            while limit > 0:
                status = False
                next_offset = -1
                if instruction.IsForceSkip() == False:
                    status, next_offset = self._ConvertCode(CurrentBB, instruction, offset)
                    parsedCnt += 1
                else:
                    next_offset = offset + 1
                    status = True
                
                if status == False:
                    if limit > 1:
                        logging.warn('schedule limitation > 1, but reach terminal node')
                    break
                offset = next_offset
                instruction = self.instructions[offset]
                limit -= 1
        
        if parsedCnt == 0:
            raise RuntimeError('no instruction is translated...')
    
    def _ConvertCode(self, CurrentBB, instruction, offset):
        opcode = instruction.GetOpCode()
        status = False
        next_offset = -1

        if   opcode == 'MOVE':
            status, next_offset = self._TranslateMove(CurrentBB, offset, instruction)
        elif opcode == 'LOADK':
            status, next_offset = self._TranslateLoadK(CurrentBB, offset, instruction)
        elif opcode == 'LOADKX':
            status, next_offset = self._TranslateLoadKx(CurrentBB, offset, instruction)
        elif opcode == 'LOADBOOL':
            status, next_offset = self._TranslateLoadBool(CurrentBB, offset, instruction)
        elif opcode == 'LOADNIL':
            status, next_offset = self._TranslateLoadNil(CurrentBB, offset, instruction)
        elif opcode == 'VARARG':
            status, next_offset = self._TranslateVararg(CurrentBB, offset, instruction)
        elif opcode == 'GETUPVAL':
            status, next_offset = self._TranslateGetUpValue(CurrentBB, offset, instruction)
        elif opcode == 'GETTABUP':
            status, next_offset = self._TranslateGetTabup(CurrentBB, offset, instruction)
        elif opcode == 'GETTABLE':
            status, next_offset = self._TranslateGetTable(CurrentBB, offset, instruction)
        elif opcode == 'SETTABUP':
            status, next_offset = self._TranslateSetTabup(CurrentBB, offset, instruction)
        elif opcode == 'SETUPVAL':
            status, next_offset = self._TranslateSetUpVal(CurrentBB, offset, instruction)
        elif opcode == 'SETTABLE':
            status, next_offset = self._TranslateSetTable(CurrentBB, offset, instruction)
        elif opcode == 'NEWTABLE':
            status, next_offset = self._TranslateNewTable(CurrentBB, offset, instruction)
        elif opcode == 'SELF':
            status, next_offset = self._TranslateSelf(CurrentBB, offset, instruction)
        elif opcode == 'ADD':
            status, next_offset = self._TranslateAdd(CurrentBB, offset, instruction)
        elif opcode == 'SUB':
            status, next_offset = self._TranslateSub(CurrentBB, offset, instruction)
        elif opcode == 'MUL':
            status, next_offset = self._TranslateMul(CurrentBB, offset, instruction)
        elif opcode == 'DIV':
            status, next_offset = self._TranslateDiv(CurrentBB, offset, instruction)
        elif opcode == 'POW':
            status, next_offset = self._TranslatePow(CurrentBB, offset, instruction)
        elif opcode == 'MOD':
            status, next_offset = self._TranslateMod(CurrentBB, offset, instruction)
        elif opcode == 'IDIV':
            status, next_offset = self._TranslateIdiv(CurrentBB, offset, instruction)
        elif opcode == 'BAND':
            status, next_offset = self._TranslateBand(CurrentBB, offset, instruction)
        elif opcode == 'BOR':
            status, next_offset  = self._TranslateBor(CurrentBB, offset, instruction)
        elif opcode == 'BXOR':
            status, next_offset = self._TranslateBxor(CurrentBB, offset, instruction)
        elif opcode == 'SHL':
            status, next_offset = self._TranslateShl(CurrentBB, offset, instruction)
        elif opcode == 'SHR':
            status, next_offset = self._TranslateShr(CurrentBB, offset, instruction)
        elif opcode == 'UNM':
            status, next_offset = self._TranslateUnm(CurrentBB, offset, instruction)
        elif opcode == 'NOT':
            status, next_offset = self._TranslateNot(CurrentBB, offset, instruction)
        elif opcode == 'LEN':
            status, next_offset = self._TranslateLen(CurrentBB, offset, instruction)
        elif opcode == 'BNOT':
            status, next_offset = self._TranslateBnot(CurrentBB, offset, instruction)
        elif opcode == 'CONCAT':
            status, next_offset = self._TranslateConcat(CurrentBB, offset, instruction)
        elif opcode == 'JMP':
            status, next_offset = self._TranslateJmp(CurrentBB, offset, instruction)
        elif opcode == 'EQ':
            status, next_offset = self._TranslateEq(CurrentBB, offset, instruction)
        elif opcode == 'LT':
            status, next_offset = self._TranslateLt(CurrentBB, offset, instruction)
        elif opcode == 'LE':
            status, next_offset = self._TranslateLe(CurrentBB, offset, instruction)
        elif opcode == 'TEST':
            status, next_offset = self._TranslateTest(CurrentBB, offset, instruction)
        elif opcode == 'TESTSET':
            status, next_offset = self._TranslateTestSet(CurrentBB, offset, instruction)
        elif opcode == 'CALL':
            status, next_offset = self._TranslateCall(CurrentBB, offset, instruction)
        elif opcode == 'TAILCALL':
            status, next_offset = self._TranslateTailCall(CurrentBB, offset, instruction)
        elif opcode == 'RETURN':
            status, next_offset = self._TranslateReturn(CurrentBB, offset, instruction)
        elif opcode == 'FORLOOP':
            status, next_offset = self._TranslateForLoop(CurrentBB, offset, instruction)
        elif opcode == 'FORREP':
            status, next_offset = self._TranslateForRep(CurrentBB, offset, instruction)
        elif opcode == 'TFORCALL':
            status, next_offset = self._TranslateTForCall(CurrentBB, offset, instruction)
        elif opcode == 'TFORLOOP':
            status, next_offset = self._TranslateTForLoop(CurrentBB, offset, instruction)
        elif opcode == 'SETLIST':
            status, next_offset = self._TranslateSetList(CurrentBB, offset, instruction)
        elif opcode == 'CLOSURE':
            status, next_offset = self._TranslateClosure(CurrentBB, offset, instruction)
        elif opcode == 'SETGLOBAL':
            status, next_offset = self._TranslateSetGlobal(CurrentBB, offset, instruction)
        elif opcode == 'GETGLOBAL':
            status, next_offset = self._TranslateGetGlobal(CurrentBB, offset, instruction)
        elif opcode == 'TFORLOOPX':
            status, next_offset = self._TranslateTForLoopX(CurrentBB, offset, instruction)
        elif opcode == 'CLOSE':
            status, next_offset = self._TranslateClose(CurrentBB, offset, instruction)
        return status, next_offset
    
    @staticmethod
    def _NodeCollectParent(node, nodelist):
        if not isinstance(node, MiddleBasicBlock):
            raise TypeError('type of node must be MiddleBasicBlock')
        
        for incoming_node in node.incoming_edges:
            nodelist.append(incoming_node)
            LuaTranslate._NodeCollectParent(incoming_node, nodelist)
    
    @staticmethod
    def _NodeLess(a, b):
        '''
        a < b : only if node a is in front of node b
        (parent node or indirect parent node)
        '''
        if not isinstance(a, MiddleBasicBlock):
            raise TypeError('type of a must be MiddleBasicBlock')
        if not isinstance(b, MiddleBasicBlock):
            raise TypeError('type of b must be MiddleBasicBlock')
        
        nodelist = []
        LuaTranslate._NodeCollectParent(b, nodelist)
        if a in nodelist:
            return True
        
        return False
    
    @staticmethod
    def _NodoSort(node_list):
        return sorted(node_list, cmp=LuaTranslate._NodeLess)
    
    def _CalcPhi(self):
        num = len(self.basicBlocks)
        if num <= 1:
            return
        
        nodelist = []
        bbHash = {}
        idx = 0
        for bb in self.basicBlocks:
            bb.num = idx
            bbHash[idx] = bb
            idx += 1
        
        for bb in self.basicBlocks:
            if len(bb.incoming_edges) < 2:
                bb.IsPhiCalculated = True
            else:
                incoming_nodes = [bb.num for bb in bb.incoming_edges]
                incoming_nodes_set = set(incoming_nodes)
                if (bb.num in incoming_nodes_set) and (len(bb.incoming_edges) - 1 < 2):
                    bb.IsPhiCalculated = True
                else:
                    nodelist.append(bb)
        
        if len(nodelist) == 0:
            print('calc phi is disable now')
            return
        
        nodelist = LuaTranslate._NodoSort(nodelist)
        print(nodelist)

        '''
        1. Lengauer-Tarjan algorithm
        2. ...
        '''
        
        raise RuntimeError('Do we really need to calculate phi value for lua ?')
    
    def _CalcVariableInfo(self):
        '''
        calculate varible usages and definations
        '''
        var_usage  = {}
        var_define = {}

        def AddToDefine(var, instr):
            if str(var) in var_define:
                pos = 0
                print('+++++++++++++++++++++++++')
                print(self.function.hashId)
                print('-------------------------')
                while pos <= instr.GetIndex():
                    print(self.mlils[pos])
                    pos += 1
                print('+++++++++++++++++++++++++')
                raise RuntimeError('var : %s is already defined @ [%s]-[%d]' % (var, instr, instr.GetIndex()))
            else:
                var_define[str(var)] = instr.GetIndex()
        
        def AddToUsage(var, instr):
            if str(var) in var_usage:
                var_usage[str(var)].append(instr.GetIndex())
            else:
                var_usage[str(var)] = [instr.GetIndex()]
        
        for instr in self.mlils:
            op = instr.GetOperation()
            if op == LuaMiddleOperation.NODE_MOVE:
                dst = instr.GetDestVar()
                src = instr.GetSrcVar()
                
                AddToDefine(dst, instr)
                if not isinstance(src, LuaConstVar):
                    AddToUsage(src, instr)
            
            elif op == LuaMiddleOperation.NODE_LOADPARAM:
                dst = instr.GetDestVar()
                AddToDefine(dst, instr)
            
            elif op == LuaMiddleOperation.NODE_MOVV:
                dst = instr.GetDestVar()
                AddToDefine(dst, instr)
            
            elif op == LuaMiddleOperation.NODE_GETUPVAL:
                dst = instr.GetDestVar()
                up   = instr.GetUpval()

                AddToDefine(dst, instr)
                AddToUsage (up,  instr)
            
            elif op == LuaMiddleOperation.NODE_GETTABUPR:
                dst = instr.GetDestVar()
                src = instr.GetSrcVar()
                up  = instr.GetUpVal()
                
                AddToDefine(dst, instr)
                AddToUsage (src, instr)
                AddToUsage (up,  instr)
            
            elif op == LuaMiddleOperation.NODE_GETTABUPC:
                dst = instr.GetDestVar()
                up  = instr.GetUpVal()
                
                AddToDefine(dst, instr)
                AddToUsage (up,  instr)
            
            elif op == LuaMiddleOperation.NODE_GETTABLER:
                dst = instr.GetDestVar()
                src = instr.GetSrcVar()
                tab = instr.GetTabVal()
                
                AddToDefine(dst, instr)
                AddToUsage (src, instr)
                AddToUsage (tab, instr)
            
            elif op == LuaMiddleOperation.NODE_GETTABLEC:
                dst = instr.GetDestVar()
                tab = instr.GetTabVal()
                
                AddToDefine(dst, instr)
                AddToUsage (tab, instr)
            
            elif op == LuaMiddleOperation.NODE_SETTABUPRR:
                dst = instr.GetDestVar()
                src = instr.GetSrcVar()
                up  = instr.GetUpVal()

                AddToUsage(dst, instr)
                AddToUsage(src, instr)
                AddToUsage(up,  instr)
            
            elif op == LuaMiddleOperation.NODE_SETTABUPCC:
                up  = instr.GetUpVal()
                AddToUsage(up,  instr)
            
            elif op == LuaMiddleOperation.NODE_SETTABUPCR:
                src = instr.GetSrcVar()
                up  = instr.GetUpVal()

                AddToUsage(src, instr)
                AddToUsage(up,  instr)

            elif op == LuaMiddleOperation.NODE_SETTABUPRC:
                dst = instr.GetDestVar()
                up  = instr.GetUpVal()

                AddToUsage(dst, instr)
                AddToUsage(up,  instr)
            
            elif op == LuaMiddleOperation.NODE_SETUPVAL:
                dst = instr.GetDestVar()
                up  = instr.GetUpVal()

                AddToUsage(dst, instr)
                AddToDefine(up,  instr)
            
            elif op == LuaMiddleOperation.NODE_SETTABLECC:
                src = instr.GetSrcVar()
                dst = instr.GetDestVar()
                tab = instr.GetTabVal()

                AddToUsage(tab,  instr)

            elif op == LuaMiddleOperation.NODE_SETTABLERR:
                src = instr.GetSrcVar()
                dst = instr.GetDestVar()
                tab = instr.GetTabVal()

                AddToUsage(tab, instr)
                AddToUsage(dst, instr)
                AddToUsage(src, instr)
            
            elif op == LuaMiddleOperation.NODE_SETTABLECR:
                src = instr.GetSrcVar()
                dst = instr.GetDestVar()
                tab = instr.GetTabVal()

                AddToUsage(tab, instr)
                AddToUsage(src, instr)
            
            elif op == LuaMiddleOperation.NODE_SETTABLERC:
                src = instr.GetSrcVar()
                dst = instr.GetDestVar()
                tab = instr.GetTabVal()

                AddToUsage(tab, instr)
                AddToUsage(dst, instr)
            
            elif op == LuaMiddleOperation.NODE_NEWTABLE:
                dst = instr.GetDestVar()
                
                AddToDefine(dst, instr)
            
            elif op == LuaMiddleOperation.NODE_SELFR:
                dst = instr.GetDestVar()
                src = instr.GetSrcVar()
                
                AddToDefine(dst, instr)
                AddToUsage (src, instr)
            
            elif op == LuaMiddleOperation.NODE_SELFC:
                dst = instr.GetDestVar()
                AddToDefine(dst, instr)
            elif op in (
                LuaMiddleOperation.NODE_ADDCC,
                LuaMiddleOperation.NODE_ADDRR,
                LuaMiddleOperation.NODE_ADDCR,
                LuaMiddleOperation.NODE_ADDRC,
                LuaMiddleOperation.NODE_SUBCC,
                LuaMiddleOperation.NODE_SUBRR,
                LuaMiddleOperation.NODE_SUBCR,
                LuaMiddleOperation.NODE_SUBRC,
                LuaMiddleOperation.NODE_MULCC,
                LuaMiddleOperation.NODE_MULRR,
                LuaMiddleOperation.NODE_MULCR,
                LuaMiddleOperation.NODE_MULRC,
                LuaMiddleOperation.NODE_DIVCC,
                LuaMiddleOperation.NODE_DIVRR,
                LuaMiddleOperation.NODE_DIVCR,
                LuaMiddleOperation.NODE_DIVRC,
                LuaMiddleOperation.NODE_POWCC,
                LuaMiddleOperation.NODE_POWRR,
                LuaMiddleOperation.NODE_POWCR,
                LuaMiddleOperation.NODE_POWRC,
                LuaMiddleOperation.NODE_MODCC,
                LuaMiddleOperation.NODE_MODRR,
                LuaMiddleOperation.NODE_MODCR,
                LuaMiddleOperation.NODE_MODRC,
                LuaMiddleOperation.NODE_IDIVCC,
                LuaMiddleOperation.NODE_IDIVRR,
                LuaMiddleOperation.NODE_IDIVCR,
                LuaMiddleOperation.NODE_IDIVRC,
                LuaMiddleOperation.NODE_BANDCC,
                LuaMiddleOperation.NODE_BANDRR,
                LuaMiddleOperation.NODE_BANDCR,
                LuaMiddleOperation.NODE_BANDRC,
                LuaMiddleOperation.NODE_BORCC,
                LuaMiddleOperation.NODE_BORRR,
                LuaMiddleOperation.NODE_BORCR,
                LuaMiddleOperation.NODE_BORRC,
                LuaMiddleOperation.NODE_BXORCC,
                LuaMiddleOperation.NODE_BXORRR,
                LuaMiddleOperation.NODE_BXORCR,
                LuaMiddleOperation.NODE_BXORRC,
                LuaMiddleOperation.NODE_SHLCC,
                LuaMiddleOperation.NODE_SHLRR,
                LuaMiddleOperation.NODE_SHLCR,
                LuaMiddleOperation.NODE_SHLRC,
                LuaMiddleOperation.NODE_SHRCC,
                LuaMiddleOperation.NODE_SHRRR,
                LuaMiddleOperation.NODE_SHRCR,
                LuaMiddleOperation.NODE_SHRRC
                ):
                dst = instr.GetDestVal()
                l   = instr.GetLeftVal()
                r   = instr.GetRightVal()
                
                AddToDefine(dst, instr)
                if not isinstance(l, LuaConstVar):
                    AddToUsage(l, instr)
                if not isinstance(r, LuaConstVar):
                    AddToUsage(r, instr)

            elif op in (
                LuaMiddleOperation.NODE_UNM,
                LuaMiddleOperation.NODE_NOT,
                LuaMiddleOperation.NODE_LEN,
                LuaMiddleOperation.NODE_BNOT
                ):
                
                src = instr.GetSrcVar()
                dst = instr.GetDestVar()
                
                AddToDefine(dst, instr)
                AddToUsage (src, instr)
            
            elif op == LuaMiddleOperation.NODE_CONCAT:
                srclist = instr.GetSrcVal()
                dst     = instr.GetDestVar()
                
                AddToDefine(dst, instr)
                for src in srclist:
                    AddToUsage(src, instr)
            
            elif op == LuaMiddleOperation.NODE_CLOSURE:
                dst = instr.GetDestVar()
                
                AddToDefine(dst, instr)
            
            elif op in (
                LuaMiddleOperation.NODE_EQCC,
                LuaMiddleOperation.NODE_EQRR,
                LuaMiddleOperation.NODE_EQCR,
                LuaMiddleOperation.NODE_EQRC,
                LuaMiddleOperation.NODE_LTCC,
                LuaMiddleOperation.NODE_LTRR,
                LuaMiddleOperation.NODE_LTCR,
                LuaMiddleOperation.NODE_LTRC,
                LuaMiddleOperation.NODE_LECC,
                LuaMiddleOperation.NODE_LERR,
                LuaMiddleOperation.NODE_LECR,
                LuaMiddleOperation.NODE_LERC
                ):
                b = instr.GetBVar()
                c = instr.GetCVar()
                
                if not isinstance(b, LuaConstVar):
                    AddToUsage(b, instr)
                if not isinstance(c, LuaConstVar):
                    AddToUsage(c, instr)
            elif op == LuaMiddleOperation.NODE_TEST:
                var = instr.GetTestVar()
                AddToUsage(var, instr)
            
            elif op == LuaMiddleOperation.NODE_LE:
                l = instr.GetLeftVal()
                r = instr.GetRightVal()
                
                AddToUsage(l, instr)
                AddToUsage(r, instr)
            
            elif op == LuaMiddleOperation.NODE_NN:
                var = instr.GetVar()
                AddToUsage(var, instr)
            
            elif op == LuaMiddleOperation.NODE_RETURN:
                retlist = instr.GetReturn()
                for ret in retlist:
                    AddToUsage(ret, instr)
            
            elif op == LuaMiddleOperation.NODE_PHI:
                l = instr.GetLeftVar()
                r = instr.GetRightVar()
                d = instr.GetDestVar()

                AddToDefine(d, instr)
                AddToUsage(l, instr)
                AddToUsage(r, instr)
            
            elif op == LuaMiddleOperation.NODE_SETLIST:
                tab = instr.GetTabVar()
                src = instr.GetSrcVar()
                
                AddToUsage(tab, instr)
                AddToUsage(src, instr)
            
            elif op == LuaMiddleOperation.NODE_TFORCALL:
                retlist = instr.GetReturn()
                arg0    = instr.GetFunctionArg1Var()
                arg1    = instr.GetFunctionArg2Var()
                func    = instr.GetFunctionVar()
                
                for ret in retlist:
                    AddToDefine(ret, instr)
                
                AddToUsage(arg0, instr)
                AddToUsage(arg1, instr)
                AddToUsage(func, instr)

            #only NODE_CALLU here
            elif op in (
                LuaMiddleOperation.NODE_CALLU,
                LuaMiddleOperation.NODE_CALLI,
                LuaMiddleOperation.NODE_CALLN,
                LuaMiddleOperation.NODE_CALLT
                ):
                retlist = instr.GetReturn()
                args    = instr.GetParam()
                func    = instr.GetFunctionVar()

                for ret in retlist:
                    AddToDefine(ret, instr)
                for arg in args:
                    AddToUsage(arg, instr)
                
                AddToUsage(func, instr)
                
        return var_define, var_usage
    
    def _LoadParam(self, bb):
        idx = 0
        while idx < self.function.paramCount:
            node = LoadParamMiddleInstruction()
            node.SetBasicBlock(bb)
            dst  = MakeSSAVar(idx, self._CalcSSAVersion(idx))
            node.SetDestVar(dst)
            node.SetIndex (idx)
            node.SetAddress(-1)
            node.SetIndex(self._curIdx)
            self._curIdx += 1
            
            bb.Insert(node)
            self.mlils.append(node)
            idx += 1

    def TranslateCode(self):
        if self.instructions is None or len(self.instructions) == 0:
            logging.error('no instruction loaded')
            return False
        
        #phase1 : translate
        bb = MiddleBasicBlock(self.function, 0)
        self.basicBlocks.append(bb)
        self.rootBlock = bb
        self._InsertBasicBlockCache(0, bb)
        self._LoadParam(bb)
        self._ConvertCodeWithSech(bb, 0)
        
        #phase2 : phi
        self._CalcPhi()

        #phase3 : varinfos
        self.varDefine, self.varUsage = self._CalcVariableInfo()

        '''
        for ins in self.mlils:
            print(ins)
        '''

        #phase4 : linear optimization
        optimizer = LuaLinearOptimizer(self.function, self.constants, self.instructions, self.mlils, self.varDefine, self.varUsage)
        optimizer.Optimizate(self.version)
        self.mlils = optimizer.mlils
        
        #phase5 : function name
        backend = LuaLinearBackend(self.function, self.constants, self.instructions, self.mlils, self.varDefine, self.varUsage)
        backend.Analysis(self.version)
        
        return True
    
    def _CalcSSAVersion(self, register):
        '''
        return SSA version for current variable
        '''
        if register in self._ssaCalc:
            self._ssaCalc[register] += 1
            return self._ssaCalc[register]
        
        self._ssaCalc[register] = 0
        return 0
    
    def _GetCurrentSSAVersion(self, register):
        if register in self._ssaCalc:
            return self._ssaCalc[register]
        return 0
    
    def _CalcSSAVersionForG(self, name):
        if name in self._ssaGCalc:
            self._ssaGCalc[name] += 1
            return self._ssaGCalc[name]
        
        self._ssaGCalc[name] = 0
        return 0

    def _GetCurrentSSAVersionForG(self, name):
        if name in self._ssaGCalc:
            return self._ssaGCalc[name]
        return 0
    
    def _CalcSSAVersionForUpval(self, index):
        if index in self._ssaUpvalCalc:
            self._ssaUpvalCalc[index] += 1
            return self._ssaUpvalCalc[index]
        
        self._ssaUpvalCalc[index] = 0
        return 0
    
    def _GetCurrentSSAVersionForUpval(self, index):
        if index in self._ssaUpvalCalc:
            return self._ssaUpvalCalc[index]
        return 0
    
    def _TranslateClose(self, current_bb, current_pc, instruction):
        node = CloseMiddleInstruction()
        node.SetBasicBlock(current_bb)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        self._curIdx += 1

        current_bb.Insert(node)
        self.mlils.append(node)
        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateSetGlobal(self, current_bb, current_pc, instruction):
        node = MoveMiddleInstruction()
        node.SetBasicBlock(current_bb)
        name = self.constants[instruction.Bx]
        dst = MakeSSAGlobalVar(name, self._CalcSSAVersionForG(name))
        src = MakeSSAVar      (instruction.A, self._GetCurrentSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetSrcVar (src)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        self._curIdx += 1

        current_bb.Insert(node)
        self.mlils.append(node)
        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateGetGlobal(self, current_bb, current_pc, instruction):
        node = MoveMiddleInstruction()
        node.SetBasicBlock(current_bb)
        name = self.constants[instruction.Bx]
        src = MakeSSAGlobalVar(name, self._GetCurrentSSAVersionForG(name))
        dst = MakeSSAVar      (instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetSrcVar (src)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        self._curIdx += 1

        current_bb.Insert(node)
        self.mlils.append(node)
        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()

    def _TranslateMove(self, current_bb, current_pc, instruction):
        node = MoveMiddleInstruction()
        node.SetBasicBlock(current_bb)
        src  = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
        dst  = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetSrcVar (src)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        self._curIdx += 1
        
        current_bb.Insert(node)
        self.mlils.append(node)
        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()

    def _TranslateLoadK(self, current_bb, current_pc, instruction):

        constType = self.constants[instruction.Bx].const_type
        node      = MoveMiddleInstruction()
        src       = self.constants[instruction.Bx]
        dst       = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        
        node.SetBasicBlock(current_bb)
        node.SetSrcVar (src)
        node.SetDestVar(dst)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        self._curIdx += 1

        current_bb.Insert(node)
        self.mlils.append(node)
        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    #ignore OP_EXTRAARG
    def _TranslateLoadKx(self, current_bb, current_pc, instruction):

        constType = self.constants[instruction.Ax].const_type
        node      = None
        src       = self.constants[instruction.Ax]
        dst       = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        
        node.SetSrcVar (src)
        node.SetDestVar(dst)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        self._curIdx += 1

        current_bb.Insert(node)
        self.mlils.append(node)
        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset() + 1
    
    
    def _TranslateLoadBool(self, current_bb, current_pc, instruction):
        '''
        LOADBOOL A B C    R(A) := (Bool)B; if (C) pc++
        '''
        mm_node = MoveMiddleInstruction()
        mm_node.SetBasicBlock(current_bb)

        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        src = LuaConstVar(True, LuaConstType.CONST_BOOL)
        if instruction.B == 0:
            src = LuaConstVar(False, LuaConstType.CONST_BOOL)
        
        mm_node.SetDestVar(dst)
        mm_node.SetSrcVar (src)

        mm_node.SetAddress(current_pc)
        mm_node.SetIndex(self._curIdx)
        self._curIdx += 1

        current_bb.Insert(mm_node)
        self.mlils.append(mm_node)
        
        instruction.SetMlil(mm_node)
        
        if instruction.C:
            node = JmpCMiddleInstruction()
            node.SetBasicBlock(current_bb)
            node.SetCondition(instruction.C)
            node.SetAddress(current_pc)
            node.SetIndex(self._curIdx)
            self._curIdx += 1

            current_bb.Insert(node)
            self.mlils.append(node)

            self._InsertBasicBlockWithSech(current_bb, node, current_pc + 1, current_pc + 2)

            '''
            return False here, terminal node (branch)
            '''
            return False, None
        else:
            return True, instruction.GetPCOffset() + 1
    
    def _TranslateLoadNil(self, current_bb, current_pc, instruction):
        begin = instruction.A
        end   = instruction.A + instruction.B
        pos   = begin
        nodes = []

        while pos <= end:
            node = MoveMiddleInstruction()
            node.SetBasicBlock(current_bb)
            dst  = MakeSSAVar(pos, self._CalcSSAVersion(pos))
            src  = LuaConstVar(None, LuaConstType.CONST_NIL)
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetAddress(current_pc)
            node.SetIndex(self._curIdx)
            self._curIdx += 1

            current_bb.Insert(node)
            self.mlils.append(node)
            nodes.append(node)
            pos += 1
        
        instruction.SetMlil(nodes[0])
        
        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateVararg(self, current_bb, current_pc, instruction):
        count = None
        begin = instruction.A
        end   = None

        if instruction.B > 2:
            end   = instruction.A + instruction.B - 2
            count = instruction.B - 1
            pos   = begin
            vidx  = 0
            nodes = []
            while pos <= end:
                node = MovvMiddleInstruction()
                node.SetBasicBlock(current_bb)
                dst = MakeSSAVar(pos, self._CalcSSAVersion(pos))
                node.SetDestVar(dst)
                node.SetVarargIndex(vidx)
                node.SetAddress(current_pc)
                node.SetIndex(self._curIdx)
                
                current_bb.Insert(node)
                self.mlils.append(node)
                nodes.append(node)
                self._curIdx += 1
                pos  += 1
                vidx += 1
            instruction.SetMlil(nodes[0])

        elif instruction.B == 2:
            end   = instruction.A
            count = 1
            vidx  = 0
            
            node = MovvMiddleInstruction()
            node.SetBasicBlock(current_bb)
            dst = MakeSSAVar(begin, self._CalcSSAVersion(begin))
            node.SetDestVar(dst)
            node.SetVarargIndex(vidx)
            node.SetAddress(current_pc)
            node.SetIndex(self._curIdx)
            
            current_bb.Insert(node)
            self.mlils.append(node)
            self._curIdx += 1

            instruction.SetMlil(node)

        else:
            if instruction.B != 0:
                raise RuntimeError('decode error in _TranslateVararg')
            
            node = MoveMiddleInstruction()
            node.SetBasicBlock(current_bb)
            dst  = MakeSSAVar(begin, self._CalcSSAVersion(begin))
            src  = LuaVararg()
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetAddress(current_pc)
            node.SetIndex(self._curIdx)
            
            current_bb.Insert(node)
            self.mlils.append(node)
            self._curIdx += 1

            instruction.SetMlil(node)
        
        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateGetUpValue(self, current_bb, current_pc, instruction):
        node = GetUpvalMiddleInstruction()
        dst  = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetBasicBlock(current_bb)
        
        sym   = self.upvalues[instruction.B].GetName()
        if sym == None or len(sym) == 0:
            sym = None
        
        version = self._GetCurrentSSAVersionForUpval(instruction.B)
        upval = LuaUpVal(instruction.B, self.upvalues[instruction.B].GetInstack(), version, sym)
        node.SetUpval(upval)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateGetTabup(self, current_bb, current_pc, instruction):
        node = None
        
        if instruction.CConstMode:
            node = GettabupCMiddleInstruction()
            node.SetBasicBlock(current_bb)
        else:
            node = GettabupRMiddleInstruction()
            node.SetBasicBlock(current_bb)

        sym   = self.upvalues[instruction.B].GetName()
        if sym == None or len(sym) == 0:
            sym = None
        
        version = self._GetCurrentSSAVersionForUpval(instruction.B)
        upval = LuaUpVal(instruction.B, self.upvalues[instruction.B].GetInstack(), version, sym)
        node.SetUpVal(upval)

        if instruction.CConstMode:
            src = self.constants[instruction.C]
            node.SetSrcVar(src)
        else:
            src = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetSrcVar(src)
        
        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)
        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateGetTable(self, current_bb, current_pc, instruction):
        node = None

        if instruction.CConstMode:
            node = GettableCMiddleInstruction()
            node.SetBasicBlock(current_bb)
        else:
            node = GettableRMiddleInstruction()
            node.SetBasicBlock(current_bb)
        
        tab = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
        node.SetTabVal(tab)

        if instruction.CConstMode:
            src = self.constants[instruction.C]
            node.SetSrcVar(src)
        else:
            src = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetSrcVar(src)

        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateSetTabup(self, current_bb, current_pc, instruction):
        node = None
        
        if instruction.BConstMode and instruction.CConstMode:
            node = SettabupCCMiddleInstruction()
            dst  = self.constants[instruction.B]
            src  = self.constants[instruction.C]
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetBasicBlock(current_bb)
        elif instruction.BConstMode == False and instruction.CConstMode:
            node = SettabupRCMiddleInstruction()
            dst  = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
            src  = self.constants[instruction.C]
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetBasicBlock(current_bb)
        elif instruction.BConstMode and instruction.CConstMode == False:
            node = SettabupCRMiddleInstruction()
            dst  = self.constants[instruction.B]
            src  = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetBasicBlock(current_bb)
        else:
            node = SettabupRRMiddleInstruction()
            dst  = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
            src  = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetBasicBlock(current_bb)
        
        sym   = self.upvalues[instruction.A].GetName()
        if sym == None or len(sym) == 0:
            sym = None
        
        version = self._GetCurrentSSAVersionForUpval(instruction.A)
        upval = LuaUpVal(instruction.A, self.upvalues[instruction.A].GetInstack(), version, sym)
        node.SetUpVal(upval)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateSetUpVal(self, current_bb, current_pc, instruction):
        node = SetUpvalMiddleInstruction()

        dst  = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetBasicBlock(current_bb)

        sym   = self.upvalues[instruction.B].GetName()
        if sym == None or len(sym) == 0:
            sym = None
        
        version = self._CalcSSAVersionForUpval(instruction.B)
        upval = LuaUpVal(instruction.B, self.upvalues[instruction.B].GetInstack(), version, sym)
        node.SetUpVal(upval)

        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateSetTable(self, current_bb, current_pc, instruction):
        node = None

        if instruction.BConstMode and instruction.CConstMode:
            node = SettableCCMiddleInstruction()
            table = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
            node.SetTabVal(table)
            dst  = self.constants[instruction.B]
            src  = self.constants[instruction.C]
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetBasicBlock(current_bb)
        elif instruction.BConstMode == False and instruction.CConstMode:
            node = SettableRCMiddleInstruction()
            table = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
            node.SetTabVal(table)
            dst  = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
            src  = self.constants[instruction.C]
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetBasicBlock(current_bb)
        elif instruction.BConstMode and instruction.CConstMode == False:
            node = SettableCRMiddleInstruction()
            table = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
            node.SetTabVal(table)
            dst  = self.constants[instruction.B]
            src  = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetBasicBlock(current_bb)
        else:
            node = SettableRRMiddleInstruction()
            table = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
            node.SetTabVal(table)
            src  = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            dst  = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
            node.SetDestVar(dst)
            node.SetSrcVar (src)
            node.SetBasicBlock(current_bb)

        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()

    
    def _TranslateNewTable(self, current_bb, current_pc, instruction):
        node = NewtableMiddleInstruction()
        
        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetBasicBlock(current_bb)
        
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateSelf(self, current_bb, current_pc, instruction):
        node = None

        mm_node = MoveMiddleInstruction()
        mm_node.SetBasicBlock(current_bb)
        src = MakeSSAVar(instruction.B,     self._GetCurrentSSAVersion(instruction.B))
        dst = MakeSSAVar(instruction.A + 1, self._CalcSSAVersion(instruction.A + 1))
        mm_node.SetDestVar(dst)
        mm_node.SetSrcVar (src)
        mm_node.SetAddress(current_pc)
        mm_node.SetIndex(self._curIdx)
        current_bb.Insert(mm_node)
        self.mlils.append(mm_node)
        self._curIdx += 1

        if instruction.CConstMode:
            node = SelfCMiddleInstruction()
            node.SetBasicBlock(current_bb)
            node.SetKeyVar(self.constants[instruction.C])
        else:
            node = SelfRMiddleInstruction()
            node.SetBasicBlock(current_bb)
            cvar = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetKeyVar(cvar)
        
        src = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetSrcVar (src)

        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateBinaryOp(self, current_bb, current_pc, instruction, cc, rc, cr, rr):
        node = None

        if instruction.BConstMode and instruction.CConstMode:
            node = cc()
            l    = self.constants[instruction.B]
            r    = self.constants[instruction.C]
            node.SetLeftVal (l)
            node.SetRightVal(r)
            node.SetBasicBlock(current_bb)
        elif instruction.BConstMode == False and instruction.CConstMode:
            node = rc()
            l    = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
            r    = self.constants[instruction.C]
            node.SetLeftVal (l)
            node.SetRightVal(r)
            node.SetBasicBlock(current_bb)
        elif instruction.BConstMode and instruction.CConstMode == False:
            node = cr()
            l  = self.constants[instruction.B]
            r  = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetLeftVal (l)
            node.SetRightVal(r)
            node.SetBasicBlock(current_bb)
        else:
            node = rr()
            l  = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
            r  = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetLeftVal (l)
            node.SetRightVal(r)
            node.SetBasicBlock(current_bb)
        
        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVal(dst)

        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    

    def _TranslateAdd(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            AddCCMiddleInstruction, 
            AddRCMiddleInstruction, 
            AddCRMiddleInstruction, 
            AddRRMiddleInstruction)
    
    def _TranslateSub(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            SubCCMiddleInstruction, 
            SubRCMiddleInstruction, 
            SubCRMiddleInstruction, 
            SubRRMiddleInstruction)


    def _TranslateMul(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            MulCCMiddleInstruction, 
            MulRCMiddleInstruction, 
            MulCRMiddleInstruction, 
            MulRRMiddleInstruction)
    

    def _TranslateDiv(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            DivCCMiddleInstruction, 
            DivRCMiddleInstruction, 
            DivCRMiddleInstruction, 
            DivRRMiddleInstruction)
    
    
    def _TranslatePow(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            PowCCMiddleInstruction, 
            PowRCMiddleInstruction, 
            PowCRMiddleInstruction, 
            PowRRMiddleInstruction)

    def _TranslateMod(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            ModCCMiddleInstruction, 
            ModRCMiddleInstruction, 
            ModCRMiddleInstruction, 
            ModRRMiddleInstruction)
    

    def _TranslateIdiv(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            IdivCCMiddleInstruction, 
            IdivRCMiddleInstruction, 
            IdivCRMiddleInstruction, 
            IdivRRMiddleInstruction)

    def _TranslateBand(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            BandCCMiddleInstruction, 
            BandRCMiddleInstruction, 
            BandCRMiddleInstruction, 
            BandRRMiddleInstruction)


    def _TranslateBor(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            BorCCMiddleInstruction, 
            BorRCMiddleInstruction, 
            BorCRMiddleInstruction, 
            BorRRMiddleInstruction)
    

    def _TranslateBxor(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            SubCCMiddleInstruction, 
            BxorRCMiddleInstruction, 
            BxorCRMiddleInstruction, 
            BxorRRMiddleInstruction)
    

    def _TranslateShl(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            ShlCCMiddleInstruction, 
            ShlRCMiddleInstruction, 
            ShlCRMiddleInstruction, 
            ShlRRMiddleInstruction)

    def _TranslateShr(self, current_bb, current_pc, instruction):
        return self._TranslateBinaryOp(
            current_bb, 
            current_pc, 
            instruction, 
            ShrCCMiddleInstruction, 
            ShrRCMiddleInstruction, 
            ShrCRMiddleInstruction, 
            ShrRRMiddleInstruction)
    

    def _TranslateUnaryOp(self, current_bb, current_pc, instruction, rr):
        node = rr()

        src = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetSrcVar (src)
        node.SetBasicBlock(current_bb)

        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateUnm(self, current_bb, current_pc, instruction):
        return self._TranslateUnaryOp(current_bb, current_pc, instruction, UnmMiddleInstruction)
    
    def _TranslateNot(self, current_bb, current_pc, instruction):
        return self._TranslateUnaryOp(current_bb, current_pc, instruction, NotMiddleInstruction)
    
    def _TranslateLen(self, current_bb, current_pc, instruction):
        return self._TranslateUnaryOp(current_bb, current_pc, instruction, LenMiddleInstruction)
    
    def _TranslateBnot(self, current_bb, current_pc, instruction):
        return self._TranslateUnaryOp(current_bb, current_pc, instruction, BnotMiddleInstruction)
    
    def _TranslateConcat(self, current_bb, current_pc, instruction):
        node = ConcatMiddleInstruction()
        src  = []

        pos = instruction.B
        while pos <= instruction.C:
            var = MakeSSAVar(pos, self._GetCurrentSSAVersion(pos))
            src.append(var)
            pos += 1

        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        node.SetSrcVal (src)
        node.SetBasicBlock(current_bb)
        
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    
    def _TranslateJmp(self, current_bb, current_pc, instruction):
        node = JmpMiddleInstruction()
        
        next_offset = current_pc + instruction.sBx + 1
        node.SetJmpOffset(next_offset)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        node.SetBasicBlock(current_bb)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)
        
        self._InsertBasicBlockJmp(current_bb, next_offset)
        return False, None

    
    def _TranslateCMP(self, current_bb, current_pc, instruction, cc, rc, cr, rr):
        node = None

        if instruction.BConstMode and instruction.CConstMode:
            node = cc()
            b = self.constants[instruction.B]
            c = self.constants[instruction.C]
            node.SetBVar(b)
            node.SetCVar(c)
            node.SetBasicBlock(current_bb)
        elif instruction.BConstMode == False and instruction.CConstMode:
            node = rc()
            b = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
            c = self.constants[instruction.C]
            node.SetBVar(b)
            node.SetCVar(c)
            node.SetBasicBlock(current_bb)
        elif instruction.BConstMode and instruction.CConstMode == False:
            node = cr()
            b = self.constants[instruction.B]
            c = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetBVar(b)
            node.SetCVar(c)
            node.SetBasicBlock(current_bb)
        else:
            node = rr()
            b = MakeSSAVar(instruction.B, self._GetCurrentSSAVersion(instruction.B))
            c = MakeSSAVar(instruction.C, self._GetCurrentSSAVersion(instruction.C))
            node.SetBVar(b)
            node.SetCVar(c)
            node.SetBasicBlock(current_bb)
        
        node.SetCondition(instruction.A)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)

        left_offset  = instruction.GetLikelyPCOffset()
        right_offset = instruction.GetUnlikelyPCOffset()
        node.SetLikelyPCOffset(left_offset)
        node.SetUnlikelyPCOffset(right_offset)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        self._InsertBasicBlockNormal(current_bb, node, left_offset, right_offset)
        return False, None
    
    #InsertBasicBlockNormal
    def _TranslateEq(self, current_bb, current_pc, instruction):
        return self._TranslateCMP(
            current_bb, 
            current_pc, 
            instruction, 
            EqCCMiddleInstruction, 
            EqRCMiddleInstruction, 
            EqCRMiddleInstruction, 
            EqRRMiddleInstruction)

    def _TranslateLt(self, current_bb, current_pc, instruction):
        return self._TranslateCMP(
            current_bb, 
            current_pc, 
            instruction, 
            LtCCMiddleInstruction, 
            LtRCMiddleInstruction, 
            LtCRMiddleInstruction, 
            LtRRMiddleInstruction)

    def _TranslateLe(self, current_bb, current_pc, instruction):
        return self._TranslateCMP(
            current_bb, 
            current_pc, 
            instruction, 
            LeCCMiddleInstruction, 
            LeRCMiddleInstruction, 
            LeCRMiddleInstruction, 
            LeRRMiddleInstruction)

    def _TranslateTest(self, current_bb, current_pc, instruction):
        node = TestMiddleInstruction()
        node.SetCondition(instruction.C)
        test = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
        node.SetTestVar(test)

        left_offset  = instruction.GetLikelyPCOffset()
        right_offset = instruction.GetUnlikelyPCOffset()
        node.SetLikelyPCOffset(instruction.GetLikelyPCOffset())
        node.SetUnlikelyPCOffset(instruction.GetUnlikelyPCOffset())
        node.SetBasicBlock(current_bb)

        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        self._InsertBasicBlockNormal(current_bb, node, left_offset, right_offset)
        return False, None
    
    def _TranslateTestSet(self, current_bb, current_pc, instruction):
        '''
        if (R(B) <=> C) then R(A) := R(B) else pc++
        
                |________|
                /        \\
            |_MOV_|     |_____|
               |
            |_____|
        '''

        src = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
        dst = MakeSSAVar(instruction.B, self._CalcSSAVersion(instruction.B))
        mm_node = MoveMiddleInstruction()
        mm_node.SetDestVar(dst)
        mm_node.SetSrcVar (src)
        mm_node.SetBasicBlock(current_bb)

        node = TestMiddleInstruction()
        node.SetCondition(instruction.C)
        
        left_offset  = instruction.GetLikelyPCOffset()
        right_offset = instruction.GetUnlikelyPCOffset()
        node.SetLikelyPCOffset(left_offset)
        node.SetUnlikelyPCOffset(right_offset)
        node.SetBasicBlock(current_bb)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        self._InsertBasicBlockSetNode(current_bb, current_pc, node, mm_node, left_offset, right_offset)
        return False, None
        
    def _TranslateCall(self, current_bb, current_pc, instruction):
        node = CallUMiddleInstruction()
        func_var = instruction.A

        if instruction.B > 2:
            begin = instruction.A + 1
            end   = instruction.A + instruction.B - 1
            count = instruction.B - 1
            
            param = []
            pos = begin
            while pos <= end:
                var = MakeSSAVar(pos, self._GetCurrentSSAVersion(pos))
                param.append(var)
                pos += 1
            
            node.SetParam(param)
            
        #only one
        elif instruction.B == 2:
            begin = instruction.A + 1
            end   = instruction.A + 1
            count = 1
            
            param = []
            var = MakeSSAVar(begin, self._GetCurrentSSAVersion(begin))
            param.append(var)
            
            node.SetParam(param)
        #none
        elif instruction.B == 1:
            pass
        #from a+1 to top
        elif instruction.B == 0:
            begin = instruction.A + 1
            node.SetParamVararg()
            node.SetParamVarargBegin(begin)

        '''
        ... = proc() <- dummy
        function z1() y(x()) end

        1 [1] GETTABUP  0 0 -1  ; _ENV "y"
        2 [1] GETTABUP  1 0 -2  ; _ENV "x"
        3 [1] CALL      1 1 0   ; C=0 so return values indicated by L->top
        4 [1] CALL      0 0 1   ; B=0 so L->top set by previous instruction
        5 [1] RETURN    0 1

        '''

        func = MakeSSAVar(func_var, self._GetCurrentSSAVersion(func_var))
        node.SetFunctionVar(func)
        
        if instruction.C > 2:
            retBegin = instruction.A
            retEnd   = instruction.A + instruction.C - 2
            retCount = instruction.C - 1

            returns = []
            pos = retBegin
            while pos <= retEnd:
                var = MakeSSAVar(pos, self._CalcSSAVersion(pos))
                returns.append(var)
                pos += 1
            
            node.SetReturn(returns)

        elif instruction.C == 2:
            retBegin = instruction.A
            retEnd   = instruction.A
            retCount = 1

            returns = []
            var = MakeSSAVar(retBegin, self._CalcSSAVersion(retBegin))
            returns.append(var)
            node.SetReturn(returns)

        elif instruction.C == 1:
            retCount = 0
        elif instruction.C == 0:
            retCount = None
            retBegin = instruction.A

            node.SetRetVararg()
            var = MakeSSAVar(retBegin, self._CalcSSAVersion(retBegin))
            node.SetRetVarargVar(var)

        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        node.SetBasicBlock(current_bb)

        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()

    def _TranslateTailCall(self, current_bb, current_pc, instruction):
        return self._TranslateCall(current_bb, current_pc, instruction)
    
    def _CalcLastArgs(self, last_instr):
        '''
        for RETURN or SETLIST
        the last instruction must be CALL or VARARG
        '''
        if last_instr.GetOpCode() not in ('VARARG', 'CALL'):
            raise RuntimeError('the last instruction must be VARARG or CALL')

        va_begin = None
        if last_instr.GetOpCode() == 'CALL':
            if last_instr.C != 0:
                raise RuntimeError('value field : C != 0')
            va_begin = last_instr.A
        elif last_instr.GetOpCode() == 'VARARG':
            if last_instr.B != 0:
                raise RuntimeError('value field : B != 0')
            va_begin = last_instr.A
        
        return va_begin
        
    
    def _TranslateReturn(self, current_bb, current_pc, instruction):
        node = ReturnMiddleInstruction()
        
        if instruction.B > 2:
            begin = instruction.A
            end   = instruction.A + instruction.B - 2
            count = instruction.B - 1

            returns = []
            pos = begin
            while pos <= end:
                var = MakeSSAVar(pos, self._GetCurrentSSAVersion(pos))
                returns.append(var)
                pos += 1
            
            node.SetReturn(returns)
        elif instruction.B == 2:
            begin = instruction.A
            end   = instruction.B
            count = 1

            returns = []
            var = MakeSSAVar(begin, self._GetCurrentSSAVersion(begin))
            returns.append(var)
            node.SetReturn(returns)
        elif instruction.B == 1:
            count = 0
        else:
            #vararg
            count = None
            begin = instruction.A
            
            #the last instruction must be vararg or call
            last_pc = current_pc - 1
            if last_pc < 0:
                raise RuntimeError('last pc value is negative')
            
            last_instr = self.instructions[last_pc]
            va_begin = self._CalcLastArgs(last_instr)
            if va_begin < begin:
                raise RuntimeError('va_begin < begin (in return)')
            
            if va_begin == begin:
                node.SetReturn([LuaVararg()])
            else:
                returns = []
                pos = begin
                while pos < va_begin:
                    var = MakeSSAVar(pos, self._GetCurrentSSAVersion(pos))
                    returns.append(var)
                    pos += 1
                returns.append(LuaVararg())
                node.SetReturn(returns)
        
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        node.SetBasicBlock(current_bb)

        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        #terminal node
        return False, None
    
    def _TranslateForLoop(self, current_bb, current_pc, instruction):
        '''
        7 [-]: FORLOOP   R0 -4        ; R0 += R2; if R0 <= R1 then R3 := R0; PC += -4 , goto 4 end
        
        ADDRR
        '''
        mm_node = AddRRMiddleInstruction()
        left  = MakeSSAVar(instruction.A,     self._GetCurrentSSAVersion(instruction.A))
        right = MakeSSAVar(instruction.A + 2, self._GetCurrentSSAVersion(instruction.A + 2))
        dst   = MakeSSAVar(instruction.A,     self._CalcSSAVersion(instruction.A))
        mm_node.SetLeftVal (left)
        mm_node.SetRightVal(right)
        mm_node.SetDestVal (dst)
        mm_node.SetAddress(current_pc)
        mm_node.SetIndex(self._curIdx)
        mm_node.SetBasicBlock(current_bb)

        current_bb.Insert(mm_node)
        self.mlils.append(mm_node)
        self._curIdx += 1

        node = LeMiddleInstruction()
        left  = MakeSSAVar(instruction.A,     self._GetCurrentSSAVersion(instruction.A))
        right = MakeSSAVar(instruction.A + 1, self._GetCurrentSSAVersion(instruction.A + 1))
        node.SetLeftVal (left)
        node.SetRightVal(right)
        node.SetBasicBlock(current_bb)
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        dangling_node = MoveMiddleInstruction()
        src = MakeSSAVar(instruction.A,     self._GetCurrentSSAVersion(instruction.A))
        dst = MakeSSAVar(instruction.A + 3, self._CalcSSAVersion(instruction.A + 3))
        dangling_node.SetDestVar(dst)
        dangling_node.SetSrcVar (src)

        instruction.SetMlil(node)

        self._InsertBasicBlockForNode(current_bb, current_pc, node, dangling_node, instruction.sBx + current_pc + 1, current_pc + 1)
        return False, None
    
    def _TranslateForRep(self, current_bb, current_pc, instruction):
        '''
        3 [-]: FORPREP   R0 3         ; R0 -= R2; pc += 3 (goto 7)
        '''
        mm_node = SubRRMiddleInstruction()

        left  = MakeSSAVar(instruction.A,     self._GetCurrentSSAVersion(instruction.A))
        right = MakeSSAVar(instruction.A + 2, self._GetCurrentSSAVersion(instruction.A + 2))
        mm_node.SetLeftVal (left)
        mm_node.SetRightVal(right)
        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        mm_node.SetDestVal(dst)
        mm_node.SetAddress(current_pc)
        mm_node.SetIndex(self._curIdx)
        mm_node.SetBasicBlock(current_bb)

        current_bb.Insert(mm_node)
        self.mlils.append(mm_node)
        self._curIdx += 1

        node = JmpMiddleInstruction()
        
        next_offset = current_pc + instruction.sBx + 1
        node.SetJmpOffset(next_offset)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        node.SetBasicBlock(current_bb)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)
        
        self._InsertBasicBlockJmp(current_bb, next_offset)
        return False, None
    
    def _TranslateTForLoopX(self, current_bb, current_pc, instruction):
        '''
        A C	R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2));
        if R(A+3) ~= nil then R(A+2)=R(A+3) else pc++
        '''
        node = TforcallMiddleInstruction()
        func = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
        node.SetFunctionVar(func)
        arg1 = MakeSSAVar(instruction.A + 1, self._GetCurrentSSAVersion(instruction.A + 1))
        arg2 = MakeSSAVar(instruction.A + 2, self._GetCurrentSSAVersion(instruction.A + 2))
        node.SetFunctionArg1Var(arg1)
        node.SetFunctionArg2Var(arg2)
        node.SetBasicBlock(current_bb)
    
        count = instruction.C
        begin = instruction.A + 3
        end   = instruction.A + instruction.C + 2

        pos     = begin
        returns = []
        while pos <= end:
            var = MakeSSAVar(pos, self._CalcSSAVersion(pos))
            returns.append(var)
            pos += 1
        
        node.SetReturn(returns)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        # ====================================
        node = NnMiddleInstruction()
        var = MakeSSAVar(instruction.A + 3, self._GetCurrentSSAVersion(instruction.A + 3))
        node.SetVar(var)
        node.SetLikelyPCOffset(instruction.GetLikelyPCOffset())
        node.SetUnlikelyPCOffset(instruction.GetUnlikelyPCOffset())
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        node.SetBasicBlock(current_bb)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        dangling_node = AddRRMiddleInstruction()
        left = MakeSSAVar(instruction.A + 2, self._GetCurrentSSAVersion(instruction.A + 2))
        right= MakeSSAVar(instruction.A + 3, self._GetCurrentSSAVersion(instruction.A + 3))
        dst  = MakeSSAVar(instruction.A + 2, self._CalcSSAVersion(instruction.A + 2))
        dangling_node.SetLeftVal (left)
        dangling_node.SetRightVal(right)
        dangling_node.SetDestVal (dst)

        instruction.SetMlil(node)

        self._InsertBasicBlockForNode(current_bb, current_pc, node, dangling_node, instruction.GetLikelyPCOffset(), instruction.GetUnlikelyPCOffset())
        return False, None
    
    # TFORCALL
    def _TranslateTForCall(self, current_bb, current_pc, instruction):
        '''
        TFORCALL    A C        R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2))
        '''
        node = TforcallMiddleInstruction()
        func = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
        node.SetFunctionVar(func)
        arg1 = MakeSSAVar(instruction.A + 1, self._GetCurrentSSAVersion(instruction.A + 1))
        arg2 = MakeSSAVar(instruction.A + 2, self._GetCurrentSSAVersion(instruction.A + 2))
        node.SetFunctionArg1Var(arg1)
        node.SetFunctionArg2Var(arg2)
        node.SetBasicBlock(current_bb)

        count = instruction.C
        begin = instruction.A + 3
        end   = instruction.A + instruction.C + 2

        pos     = begin
        returns = []
        while pos <= end:
            var = MakeSSAVar(pos, self._CalcSSAVersion(pos))
            returns.append(var)
            pos += 1
        
        node.SetReturn(returns)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)

        return True, instruction.GetNextInstruction().GetPCOffset()
    
    def _TranslateTForLoop(self, current_bb, current_pc, instruction):
        '''
        TFORLOOP    A sBx      if R(A+1) ~= nil then { R(A)=R(A+1); pc += sBx }
        '''
        node = NnMiddleInstruction()
        var = MakeSSAVar(instruction.A + 1, self._GetCurrentSSAVersion(instruction.A + 1))
        node.SetVar(var)
        node.SetLikelyPCOffset(current_pc + instruction.sBx + 1)
        node.SetUnlikelyPCOffset(current_pc + 1)
        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        node.SetBasicBlock(current_bb)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        dangling_node = AddRRMiddleInstruction()
        left = MakeSSAVar(instruction.A,     self._GetCurrentSSAVersion(instruction.A))
        right= MakeSSAVar(instruction.A + 1, self._GetCurrentSSAVersion(instruction.A + 1))
        dst  = MakeSSAVar(instruction.A,     self._CalcSSAVersion(instruction.A))
        dangling_node.SetLeftVal (left)
        dangling_node.SetRightVal(right)
        dangling_node.SetDestVal (dst)

        instruction.SetMlil(node)
        
        self._InsertBasicBlockForNode(current_bb, current_pc, node, dangling_node, instruction.sBx + current_pc + 1, current_pc + 1)
        return False, None
    
    def _TranslateSetList(self, current_bb, current_pc, instruction):
        '''
        SETLIST A B C   R(A)[(C-1)*FPF+i] := R(A+i), 1 <= i <= B
        '''
        
        LFIELDS_PER_FLUSH = 50
        idxBegin = (instruction.C - 1) * LFIELDS_PER_FLUSH

        # R%d[%d] to R%d[top] := R%d to top
        if instruction.B == 0:
            count = None
            begin = instruction.A + 1
            
            #the last instruction must be vararg or call
            last_pc = current_pc - 1
            if last_pc < 0:
                raise RuntimeError('last pc value is negative')
            
            last_instr = self.instructions[last_pc]
            va_begin   = self._CalcLastArgs(last_instr)
            
            if va_begin < begin:
                raise RuntimeError('va_begin < begin (in return)')
            
            left_list = []
            if va_begin == begin:
                left_list.append(LuaVararg())
            else:
                pos = begin
                while pos < va_begin:
                    var = MakeSSAVar(pos, self._GetCurrentSSAVersion(pos))
                    left_list.append(var)
                    pos += 1
                left_list.append(LuaVararg())
            
            nodes = []
            for left in left_list:
                node    = SetlistMiddleInstruction()
                tab = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
                node.SetTabVar(tab)
                node.SetSrcVar(left)
            
                node.SetAddress(current_pc)
                node.SetIndex(self._curIdx)
                node.SetBasicBlock(current_bb)
                
                current_bb.Insert(node)
                self.mlils.append(node)
                nodes.append(node)
                self._curIdx += 1
            
            instruction.SetMlil(nodes[0])
        
        # R%d[%d] := R%d
        elif instruction.B == 1:
            node = SetlistMiddleInstruction()
            tab  = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
            node.SetTabVar(tab)
            node.SetTabIndex(idxBegin)

            src  = MakeSSAVar(instruction.A + 1, self._GetCurrentSSAVersion(instruction.A + 1))
            node.SetSrcVar(src)
            node.SetAddress(current_pc)
            node.SetIndex(self._curIdx)
            node.SetBasicBlock(current_bb)
            
            current_bb.Insert(node)
            self.mlils.append(node)
            self._curIdx += 1

            instruction.SetMlil(node)
        
        # R%d[%d] to R%d[%d] := R%d to R%d
        elif instruction.B > 1:
            i = 0
            nodes = []
            while i < instruction.B:
                node = SetlistMiddleInstruction()
                tab  = MakeSSAVar(instruction.A, self._GetCurrentSSAVersion(instruction.A))
                node.SetTabVar(tab)
                node.SetTabIndex(idxBegin + i)
                node.SetBasicBlock(current_bb)

                src  = MakeSSAVar(instruction.A + 1 + i, self._GetCurrentSSAVersion(instruction.A + 1 + i))
                node.SetSrcVar(src)
                node.SetAddress(current_pc)
                node.SetIndex(self._curIdx)
                nodes.append(node)
                
                current_bb.Insert(node)
                self.mlils.append(node)
                self._curIdx += 1
                i += 1
            
            instruction.SetMlil(nodes[0])
        
        if instruction.GetSkipNext():
            return True, instruction.GetNextInstruction().GetPCOffset() + 1
        
        return True, instruction.GetNextInstruction().GetPCOffset()

    def _TranslateClosure(self, current_bb, current_pc, instruction):
        node = ClosureMiddleInstruction()
        dst = MakeSSAVar(instruction.A, self._CalcSSAVersion(instruction.A))
        node.SetDestVar(dst)
        idx = instruction.Bx
        node.SetFunction(idx)
        node.SetBasicBlock(current_bb)

        node.SetAddress(current_pc)
        node.SetIndex(self._curIdx)
        
        current_bb.Insert(node)
        self.mlils.append(node)
        self._curIdx += 1

        instruction.SetMlil(node)
        return True, instruction.GetNextInstruction().GetPCOffset()



        