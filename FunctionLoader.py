from __future__ import print_function
import logging
import LuaString
from LuaInstruction import *
from LuaByteCode import *
from LuaVar import *
from LuaDisasm import LuaDisasm
from LuaUpvalue import LuaUpvalue
from LuaVar import LuaFunctionType

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class LuaByteCodeFunction(object):
    def __init__(self, function_owner, scriptOwner, stream, binary_pos, instructionSize, sizeOfInt, sizeOfLuaint, sizeOfSizeT, sizeOfNum, level, isBE = False, topLevel = False):
        if stream is None:
            raise ValueError('stream is none')
        self.stream    = stream
        self.topLevel = topLevel
        self.functionName  = '__unknown__'
        self.srcBegin  = 0
        self.srcEnd    = 0
        self.binaryPos = 0
        self.isBE     = isBE
        self.paramCount = 0
        self.regCount   = 0
        self.codeSize = 0
        self.constantSize   = 0
        self.sizeOfSizeT    = sizeOfSizeT
        self.sizeOfInt      = sizeOfInt
        self.instructionSize = instructionSize
        self.sizeOfNum      = sizeOfNum
        self.sizeOfLuaint   = sizeOfLuaint
        self.varFlag    = 0 # 2
        self.varCount   = 0
        self.instructions = [] #binary order
        self.upvalues     = []
        self.constants    = []
        self.subfunctions = []
        self.parent       = function_owner
        self.LFIELDS_PER_FLUSH = 50
        self._is_linked   = False
        self.hashId      = ''
        self.type        = LuaFunctionType.LUA_NORMAL
        self.Engine      = None
        self.lineinfos   = []

        #function level
        '''
        main (0)
        --function_A (1)
           --function_B (2)
        '''
        self.functionLevel = level
        self.owner         = scriptOwner
        self.binaryPos     = binary_pos
        self.stream.seek(self.binaryPos)
    
    def _SetFunctionLevel(self, level):
        self._function_level = level
    
    def GetFunctionRegisterCount(self):
        return self.regCount
    
    def GetFunctionType(self):
        return self.type
    
    def SetFunctionType(self, t):
        self.type = t
    
    def GetFunctionLevel(self):
        return self.functionLevel
    
    def SetFunctionHashid(self, hashid):
        self.hashId = hashid
    
    def GetFunctionHashid(self):
        return self.hashId
    
    def GetFunctionParent(self):
        return self.parent
    
    def GetCurStream(self):
        return self.stream

    def GetSrcBegin(self):
        return self.srcBegin
    
    def GetSrcEnd(self):
        return self.srcEnd
    
    def GetBinaryPos(self):
        return self.binaryPos
    
    def GetFunctionName(self):
        return self.functionName
    
    def SetFunctionName(self, name):
        self.functionName = name
    
    def GetCodeSize(self):
        return self.codeSize

    def IsTopLevelFunction(self):
        return self.topLevel
    
    def GetFunctionInstructionRoot(self):
        return self.instructions[0]
    
    def GetSubFunctions(self):
        '''
        return type : list
        '''
        return self.subfunctions
    
    def GetSubFunctionCount(self):
        return len(self.subfunctions)
    
    def PrintLinkedByteCode(self):
        for i in range(len(self.instructions)):
            if self.instructions[i].IsNormalInstruction():
                next_node = 'None'
                if self.instructions[i].GetNextInstruction() != None:
                    next_node = self.instructions[i].GetNextInstruction().GetOpCode()
                #print('%s -> (%s)' % (self.instructions[i].GetOpCode(), next_node))
            elif self.instructions[i].IsJmpInstruction():
                next_node = self.instructions[i].GetJmpInstruction().GetOpCode()
                #print('%s -> (%s)' % (self.instructions[i].GetOpCode(), next_node))
            else:
                likely_node   = 'None'
                unlikely_node = 'None'
                if self.instructions[i].GetLikelyInstruction() != None:
                    likely_node = self.instructions[i].GetLikelyInstruction().GetOpCode()
                if self.instructions[i].GetUnlikelyInstruction() != None:
                    unlikely_node = self.instructions[i].GetUnlikelyInstruction().GetOpCode()
                #print('%s -> (%s, %s)' % (self.instructions[i].GetOpCode(), likely_node, unlikely_node))
    
    def _Link(self):
        if self.instructions == None or len(self.instructions) == 0:
            raise RuntimeError('_Link : no instruction loaded...')
        if self._is_linked:
            logging.warn('already linked...')
            return
        
        #SetPCOffset
        for i in range(len(self.instructions)):
            self.instructions[i].SetPCOffset(i)
            #print('[%d] %s' % (self.instructions[i].GetPCOffset(), self.instructions[i].GetOpCode()))

        max_node = len(self.instructions)
        for i in range(max_node):
            if self.instructions[i].IsNormalInstruction():
                if i + 1 >= max_node:
                    self.instructions[i].SetNextInstruction(None)
                else:
                    self.instructions[i].SetNextInstruction(self.instructions[i + 1])
            elif self.instructions[i].IsJmpInstruction():
                self.instructions[i].SetJmpInstruction(
                    self.instructions[self.instructions[i].GetJmpOffset()])
            else:
                self.instructions[i].SetLikelyInstruction(
                    self.instructions[self.instructions[i].GetLikelyPCOffset()]
                )
                self.instructions[i].SetUnlikelyInstruction(
                    self.instructions[self.instructions[i].GetUnlikelyPCOffset()]
                )
        
        logging.info('link...ok')
    
    def _DisassembleCode(self, current_pos):
        pc_offset = 0
        disasm = LuaDisasm(self.stream, self.instructionSize, self.codeSize, self.constants, self.isBE)
        pos    = disasm.DisassembleCode(current_pos)
        self.stream.seek(pos)
        self.instructions = disasm.instructions
    
    def _DecodeFunctionPrototyte(self):
        bytes_readed = 0
        count_buf = self.stream.read(4)
        if self.isBE == False:
            count = unpack('<L', count_buf[0:4])[0]
        else:
            count = unpack('>L', count_buf[0:4])[0]
        self.owner.SetSubFunctionCount(count)
        logging.info('\tsub function count : 0x%x' % count)
        bytes_readed = 4
        if count == 0:
            return bytes_readed
        
        chunk_pos = self.stream.tell()
        saved_pos = self.stream.tell()
        pos = 0
        for i in range(count):
            logging.info('Processing sub-function @ 0x%x' % self.stream.tell())
            func = LuaByteCodeFunction(
                self, 
                self.owner, 
                self.stream, 
                chunk_pos, 
                self.instructionSize, 
                self.sizeOfInt,
                self.sizeOfLuaint,
                self.sizeOfSizeT, 
                self.sizeOfNum,
                self.GetFunctionLevel() + 1, 
                self.isBE)
            
            func.SetFunctionHashid(self.GetFunctionHashid() + '_' + str(i))
            pos = func.Parse()
            self.subfunctions.append(func)
            chunk_pos = chunk_pos + pos
            bytes_readed = bytes_readed + pos
        
        #4 : count_buf
        self.stream.seek(saved_pos + bytes_readed - 4)
        #IPython.embed()
        return bytes_readed
    
    def _DecodeDebugSrcLine(self):
        line_cnt = self.stream.read(4)
        return 4
    
    def _DecodeDebugLocalName(self):
        #size in binary, not count...
        var_size_buf = self.stream.read(4)
        var_block_size = 0
        current_pos = 0

        if self.isBE == False:
            var_block_size = unpack('<L', var_size_buf[0:4])[0]
        else:
            var_block_size = unpack('>L', var_size_buf[0:4])[0]
        
        if var_block_size == 0:
            return 4
        
        #for now, I'dont care about this info...
        var_block = self.stream.read(var_block_size)
        return 4 + var_block_size
    
    def _DecodeUpValues(self):
        logging.info('\tUpValues Block : 0x%x' % self.stream.tell())
        bytes_readed = 0
        upvalue_buf_cnt = self.stream.read(4)
        upvalue_cnt = 0
        
        if self.isBE == False:
            upvalue_cnt = unpack('<L', upvalue_buf_cnt[0:4])[0]
        else:
            upvalue_cnt = unpack('>L', upvalue_buf_cnt[0:4])[0]
        
        logging.info('\tUpValue count : 0x%x' % upvalue_cnt)
        
        bytes_readed = 4
        if upvalue_cnt == 0:
            return bytes_readed

        if self.upvalues == None or len(self.upvalues) == 0:
            for i in range(upvalue_cnt):
                upobj = LuaUpvalue()
                self.upvalues.append(upobj)
        
        for i in range(upvalue_cnt):
            unpack_flag_buf = self.stream.read(1)
            unpack_flag = unpack('<B', unpack_flag_buf[0:1])[0]
            string_size = unpack_flag
            bytes_readed = bytes_readed + 1

            if unpack_flag == 0xFF:
                unpack_str = '<L'
                unpack_size = 4
                if self.isBE == False:
                    if self.sizeOfSizeT == 4:
                        unpack_str = '<L'
                    else:
                        unpack_size = 8
                        unpack_str = '<Q'
                else:
                    if self.sizeOfSizeT == 4:
                        unpack_str = '>L'
                    else:
                        unpack_size = 8
                        unpack_str = '>Q'
                
                bytes_readed = bytes_readed + unpack_size
                string_size_buf = self.stream.read(unpack_size)
                string_size = unpack(unpack_str, string_size_buf[0:unpack_size])[0]
            
            if string_size != 0:
                bytes_readed = bytes_readed + (string_size - 1)
                current_upvalue = self.stream.read(string_size - 1)
                logging.info('\tUpValue : %s' % current_upvalue)
                self.upvalues[i].SetName(current_upvalue)
            else:
                self.upvalues[i].SetName('')
        return bytes_readed
    
    def _DecodeContant(self):
        '''
        Todo : openwrt support
        src : static void LoadConstants (LoadState *S, Proto *f)
        '''
        bytes_readed = 0
        constand_size_buf = self.stream.read(4)
        if self.isBE == False:
            self.constantSize = unpack('<L', constand_size_buf[0:4])[0]
        else:
            self.constantSize = unpack('>L', constand_size_buf[0:4])[0]
        
        bytes_readed = 4
        if self.constantSize == 0:
            return bytes_readed
        
        for i in range(self.constantSize):
            var = LuaConstVar(None, LuaConstType.CONST_NIL)
            self.constants.append(var)
        
        for i in range(self.constantSize):
            types_buf = self.stream.read(1)
            types = unpack('<B', types_buf[0:1])[0]
            bytes_readed = bytes_readed + 1

            if types == LUA_TNIL:
                logging.info('\t NIL (0x%x)' % self.stream.tell())
            elif types == LUA_TBOOLEAN:
                logging.info('\t BOOL (0x%x)' % self.stream.tell())
                self.constants[i].type = LuaConstType.CONST_BOOL
                bytes_readed = bytes_readed + 1 #val
                bool_val_buf = self.stream.read(1)
                bool_val = unpack('<B', bool_val_buf[0:1])[0]
                if bool_val != 0:
                    self.constants[i].var = True
                else:
                    self.constants[i].var = False
            elif types == LUA_TNUMBER:
                logging.info('\t NUMBER (0x%x)' % self.stream.tell())
                self.constants[i].type = LuaConstType.CONST_NUM
                double_val_buf = self.stream.read(self.sizeOfNum)
                double_val = 0.0
                bytes_readed = bytes_readed + self.sizeOfNum
                if self.isBE == False:
                    if self.sizeOfNum == 4:
                        double_val = unpack('<f', double_val_buf[0:self.sizeOfNum])[0]
                    else:
                        double_val = unpack('<d', double_val_buf[0:self.sizeOfNum])[0]
                else:
                    if self.sizeOfNum == 4:
                        double_val = unpack('>f', double_val_buf[0:self.sizeOfNum])[0]
                    else:
                        double_val = unpack('>d', double_val_buf[0:self.sizeOfNum])[0]
                self.constants[i].var = double_val
            elif types == LUA_TNUMINT:
                logging.info('\t INT (0x%x)' % self.stream.tell())
                self.constants[i].type = LuaConstType.CONST_INT
                int_val_buf = self.stream.read(self.sizeOfLuaint)
                int_val = 0
                bytes_readed = bytes_readed + self.sizeOfLuaint
                if self.isBE == False:
                    if self.sizeOfLuaint == 4:
                        int_val = unpack('<l', int_val_buf[0:self.sizeOfLuaint])[0]
                    else:
                        int_val = unpack('<q', int_val_buf[0:self.sizeOfLuaint])[0]
                else:
                    if self.sizeOfLuaint == 4:
                        int_val = unpack('>l', int_val_buf[0:self.sizeOfLuaint])[0]
                    else:
                        int_val = unpack('>q', int_val_buf[0:self.sizeOfLuaint])[0]
                self.constants[i].var = int_val
            elif types in (LUA_TSHRSTR, LUA_TLNGSTR):
                logging.info('\t STR (0x%x)' % self.stream.tell())
                self.constants[i].type = LuaConstType.CONST_STR
                string_size_buf = self.stream.read(1)
                string_size = unpack('<B', string_size_buf[0:1])[0]
                bytes_readed = bytes_readed + 1
                if string_size == 0xFF:
                    #to large 
                    if self.sizeOfSizeT == 4:
                        string_size_buf = self.stream.read(4)
                        bytes_readed = bytes_readed + 4
                    else:
                        string_size_buf = self.stream.read(8)
                        bytes_readed = bytes_readed + 8
                    
                    string_size = 0
                    if self.isBE == False:
                        if self.sizeOfSizeT == 4:
                            string_size = unpack('<L', string_size_buf[0:4])[0]
                        else:
                            string_size = unpack('<Q', string_size_buf[0:8])[0]
                    else:
                        if self.sizeOfSizeT == 8:
                            string_size = unpack('>L', string_size_buf[0:4])[0]
                        else:
                            string_size = unpack('>Q', string_size_buf[0:8])[0]
                    
                if string_size == 0:
                    self.constants[i].var = ''
                else:
                    string_buf = self.stream.read(string_size - 1)
                    bytes_readed = bytes_readed + (string_size - 1)
                    string_buf = string_buf.decode()
                    string_buf = LuaString.escape(string_buf)
                    self.constants[i].var = string_buf
                    logging.info('\t str = %s' % string_buf)
            elif types == LUA_NUMTAGS: #lua 5.3 or openwrt
                logging.info('\t NUMTAG (0x%x)' % self.stream.tell())
                self.constants[i].type = LuaConstType.CONST_INT
                int_val_buf = self.stream.read(self.sizeOfInt)
                int_val = 0
                bytes_readed = bytes_readed + self.sizeOfInt
                if self.isBE == False:
                    int_val = unpack('<L', int_val_buf[0:self.sizeOfInt])[0]
                else:
                    int_val = unpack('>L', int_val_buf[0:self.sizeOfInt])[0]
                self.constants[i].var = ('%d' % int_val)
            else:
                raise RuntimeError('unknown type = %d' % types)
        return bytes_readed

    def _DecodeUpValuesNew(self):
        upvalue_cnt_str = self.stream.read(4)
        upvalue_cnt  = 0
        bytes_readed = 0

        if self.isBE == False:
            upvalue_cnt = unpack('<L', upvalue_cnt_str[0:4])[0]
        else:
            upvalue_cnt = unpack('>L', upvalue_cnt_str[0:4])[0]
        bytes_readed = bytes_readed + 4

        if upvalue_cnt == 0:
            return bytes_readed
        
        for i in range(upvalue_cnt):
            upobj = LuaUpvalue()
            val_str = self.stream.read(1)
            
            instack = unpack('<B', val_str[0:1])[0]
            if instack != 0:
                upobj.SetInstack(True)
            else:
                upobj.SetInstack(False)
            
            val_str = self.stream.read(1)
            upobj.SetUpIndex(unpack('<B', val_str[0:1])[0])
            bytes_readed = bytes_readed + 2
            
            self.upvalues.append(upobj)
        
        return bytes_readed

    def _DecodeDebugNew(self):
        lineinfo_str = self.stream.read(4)
        lineinfo     = 0
        bytes_readed = 0

        if self.isBE == False:
            lineinfo = unpack('<L', lineinfo_str[0:4])[0]
        else:
            lineinfo = unpack('>L', lineinfo_str[0:4])[0]
        bytes_readed = bytes_readed + 4

        if lineinfo != 0:
            for i in range(lineinfo):
                unpackString = '<L'
                if self.isBE:
                    unpackString = '>L'
                lineString = self.stream.read(4)
                line = unpack(unpackString, lineString[0:4])[0]
                self.lineinfos.append(line)
            
            #self.stream.read(4 * lineinfo)
            bytes_readed = bytes_readed + (4 * lineinfo)
        

        localvar_str = self.stream.read(4)
        localvar     = 0
        if self.isBE == False:
            localvar = unpack('<L', localvar_str[0:4])[0]
        else:
            localvar = unpack('>L', localvar_str[0:4])[0]
        bytes_readed = bytes_readed + 4

        if localvar != 0:
            for i in range(localvar):
                string_size_buf = self.stream.read(1)
                string_size = unpack('<B', string_size_buf[0:1])[0]
                bytes_readed = bytes_readed + 1
                if string_size == 0xFF:
                    #too large 
                    if self.sizeOfSizeT == 4:
                        string_size_buf = self.stream.read(4)
                        bytes_readed = bytes_readed + 4
                    else:
                        string_size_buf = self.stream.read(8)
                        bytes_readed = bytes_readed + 8
                    
                    string_size = 0
                    if self.isBE == False:
                        if self.sizeOfSizeT == 4:
                            string_size = unpack('<L', string_size_buf[0:4])[0]
                        else:
                            string_size = unpack('<Q', string_size_buf[0:8])[0]
                    else:
                        if self.sizeOfSizeT== 8:
                            string_size = unpack('>L', string_size_buf[0:4])[0]
                        else:
                            string_size = unpack('>Q', string_size_buf[0:8])[0]

                if string_size != 0:
                    string_buf = self.stream.read(string_size - 1)
                    string_buf = LuaString.escape(string_buf)
                    bytes_readed = bytes_readed + (string_size - 1)
                    logging.info('var -> %s' % string_buf)

                #start pc
                self.stream.read(4)
                #end pc
                self.stream.read(4)
                bytes_readed = bytes_readed + 8
        
        pos = 0
        pos = pos + self._DecodeUpValues()

        return pos + bytes_readed
    
    
    def _ParseLua53ByteCode(self):
        '''
        all segments in this function
        '''
        bytes_readed = 0
        current_pos = self.binaryPos
        string_size_buf = self.stream.read(1)
        string_size = unpack('<B', string_size_buf[0:1])[0]
        bytes_readed = bytes_readed + 1
        current_pos  = current_pos + 1
        is_big_string = False
        if string_size == 0xFF:
            #to large 
            if self.sizeOfSizeT == 4:
                string_size_buf = self.stream.read(4)
                bytes_readed = bytes_readed + 4
                current_pos  = current_pos + 4
            else:
                string_size_buf = self.stream.read(8)
                bytes_readed = bytes_readed + 8
                current_pos  = current_pos + 8
            is_big_string = True

        if is_big_string:              
            if self.isBE == False:
                if self.sizeOfSizeT == 4:
                    string_size = unpack('<L', string_size_buf[0:4])[0]
                else:
                    string_size = unpack('<Q', string_size_buf[0:8])[0]
            else:
                if self.sizeOfSizeT == 8:
                    string_size = unpack('>L', string_size_buf[0:4])[0]
                else:
                    string_size = unpack('>Q', string_size_buf[0:8])[0]
                    
        if string_size != 0:
            self.srcName = self.stream.read(string_size - 1)
            bytes_readed  = bytes_readed + (string_size - 1)
            current_pos   = current_pos  + (string_size - 1)

        start_line_buf = self.stream.read(4)
        self._srcbegin = unpack('<L', start_line_buf[0:4])[0]
        current_pos = current_pos + 4
        bytes_readed = bytes_readed + 4

        end_line_buf = self.stream.read(4)
        self.srcEnd = unpack('<L', end_line_buf[0:4])[0]
        current_pos = current_pos + 4
        bytes_readed = bytes_readed = 4

        # top level function?
        if self.srcEnd == 0 and self.srcBegin == 0:
            self.topLevel = True
        
        param_cnt_buf = self.stream.read(1)
        self.paramCount = unpack('<B', param_cnt_buf[0:1])[0]
        current_pos = current_pos + 1
        bytes_readed = bytes_readed + 1

        vars_flags_buf = self.stream.read(1)
        vars_flags = unpack('<B', vars_flags_buf[0:1])[0]
        current_pos = current_pos + 1
        bytes_readed = bytes_readed + 1

        if vars_flags & 1:
            self.varFlag |= 1
            logging.info('\tvar flag : VARARG_HASARG')
        elif vars_flags & 2:
            self.varFlag |= 2
            logging.info('\tvar flag : VARARG_ISVARARG')
        elif vars_flags & 4:
            self.varFlag |= 4
            logging.info('\tvar flag : VARARG_NEEDSARG')
        elif vars_flags == 0:
            self.varFlag = 0
            logging.info('\tvar flag : VARARG_NONE')
        else:
            if vars_flags > 7:
                raise RuntimeError('Unsupported vars flag = %d' % vars_flags)
        
        regs_cnt_buf = self.stream.read(1)
        self.regCount = unpack('<B', regs_cnt_buf[0:1])[0]
        current_pos = current_pos + 1
        bytes_readed = bytes_readed + 1

        code_size_buf = self.stream.read(4)
        current_pos = current_pos + 4
        bytes_readed = bytes_readed + 4

        if self.isBE == False:
            self.codeSize = unpack('<L', code_size_buf[0:4])[0]
        else:
            self.codeSize = unpack('>L', code_size_buf[0:4])[0]
        
        #decode constant first...
        self.stream.seek(current_pos + self.codeSize * self.instructionSize)
        pos = 0
        pos = pos + self._DecodeContant()
        pos = pos + self._DecodeUpValuesNew()
        pos = pos + self._DecodeFunctionPrototyte()
        pos = pos + self._DecodeDebugNew()
        
        saved_pos = self.stream.tell()
        #back to bytecode
        self.stream.seek(current_pos)
        self._DisassembleCode(current_pos)


        logging.info('function end @ 0x%x (size : 0x%x)' % (saved_pos, (saved_pos - self.binaryPos)))
        
        self._Link()
        self.PrintLinkedByteCode()
        #next chunk or end of file
        return saved_pos - self.binaryPos
    
    def Parse(self):
        return self._ParseLua53ByteCode()
    
    def GetFunctionArgsCount(self):
        return self.paramCount
