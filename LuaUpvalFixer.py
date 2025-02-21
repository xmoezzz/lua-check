#for lua5.1 only
from __future__ import print_function

class LuaUpvalFixer(object):
    def __init__(self, instructions, upvals, function):
        self.instructions = instructions
        self.upvals       = upvals
        self.function     = function
    
    def _FixUpval(self, instr, idx, offset):
        subfunc   = self.function.subfunctions[idx]
        subUpvals = len(subfunc.upvalues)
        if subUpvals == 0:
            return
        
        if offset >= len(self.instructions):
            raise RuntimeError('upval count is none-zero, but current instruction is the last one in current function')
        
        pos = offset
        cnt = 0
        while cnt < subUpvals:
            op = self.instructions[pos].GetOpCode()
            if op == 'MOVE':
                #instack
                upidx = self.instructions[pos].B
                subfunc.upvalues[cnt].SetInstack(True)
                subfunc.upvalues[cnt].SetUpIndex(upidx)
                self.instructions[pos].SetForceSkip()
                cnt += 1
            elif op == 'GETUPVAL':
                #not instack
                upidx = self.instructions[pos].B
                subfunc.upvalues[cnt].SetInstack(False)
                subfunc.upvalues[cnt].SetUpIndex(upidx)
                self.instructions[pos].SetForceSkip()
                cnt += 1
            else:
                raise RuntimeError('reach other node while fixing upval')
            pos += 1
        
        if cnt < subUpvals:
            raise RuntimeError('unable to solve all upvals (%d -> %d)' % (cnt, subUpvals))
    
    def Fixer(self):
        offset = 0
        for instr in self.instructions:
            if instr.GetOpCode() == 'CLOSURE':
                idx = instr.Bx
                self._FixUpval(instr, idx, offset + 1)
            offset += 1