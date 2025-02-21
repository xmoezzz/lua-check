from __future__ import print_function
from LnEnum import Endianness, LuaVersion
from struct import unpack
from io import BytesIO
from LuaTranslation import LuaTranslate
from FunctionLoader import LuaByteCodeFunction #53
from FunctionLoader51 import LuaByteCodeFunction51
from FunctionLoader52 import LuaByteCodeFunction52
from LuaMiddleLang import *
from termcolor import colored, cprint
from LuaModeler import LuaModeler
from LuaUpvalFixer import LuaUpvalFixer
from LuaTaint import is_taint_source, is_taint_target

lua_time = '\x19\x93\x0D\x0A\x1A\x0A'

class LuaByteCodeLoader(object):
    def __init__(self, buf, output, elua, sourceLines):
        if buf is None or not isinstance(buf, bytes):
            raise TypeError('type of buf must be bytes --> %s' % type(buf))
        self.buf    = buf
        self.endian = Endianness.LittleEndian
        self.version= None
        self.sizeOfInt    = 4
        self.sizeOfSizeT  = 4
        self.sizeOfInstr  = 4
        self.sizeOfNum    = 8
        self.function_top = None #top level function...
        self.subFuncCount = 0
        self.output = output
        self.sourceLines = sourceLines
        self.eluaMode    = elua
    
    def SetSubFunctionCount(self, cnt):
        self.subFuncCount = cnt
    
    def GetSubFunctionCount(self):
        return self.subFuncCount
    
    def _CheckFormatVersion(self, format_version):
        if format_version != b'\x00':
            raise ValueError('format version must be 0')
    
    def _ParseLua53Common(self, stream):
        if self.eluaMode:
            raise NotImplementedError('Lua5.3 : elua mode is not supported')
        format_version = stream.read(1)
        self._CheckFormatVersion(format_version)

        luatimeinfo = stream.read(6)
        if luatimeinfo != lua_time:
            raise ValueError('not match : lua time magic (since lua 5.2)')
        
        sizeOfInt   = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfSizeT = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfInstr = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfLuaint= unpack('<B', stream.read(1)[0:1])[0]
        sizeOfMum   = unpack('<B', stream.read(1)[0:1])[0]

        endian_buf   = stream.read(8)
        endian_int = unpack('<Q', endian_buf[0:8])[0]
        if endian_int == 0x5678:
            self.endian = Endianness.LittleEndian
        else:
            self.endian = Endianness.BigEndian
        
        stream.read(8)

        #ignore it now...
        elems_buf = stream.read(1)

        isBE = False
        if self.endian == Endianness.BigEndian:
            isBE = True
        
        bytes_readed = stream.tell()
        func = LuaByteCodeFunction(None, self, stream, bytes_readed, sizeOfInstr, sizeOfInt, sizeOfLuaint, sizeOfSizeT, sizeOfMum, 0, isBE) #main function
        func.SetFunctionHashid('root')
        func.SetFunctionName('<root>')
        cur_pos = func.Parse()
        self.function_top = func
        
        #support muilt src file
        return bytes_readed
    
    def _ParseLua52Common(self, stream):
        if self.eluaMode:
            raise NotImplementedError('Lua5.2 : elua mode is not supported')
        format_version = stream.read(1)
        self._CheckFormatVersion(format_version)
        endian = stream.read(1)

        if endian == b'\x00':
            self.endian = Endianness.BigEndian
        elif endian == b'\x01':
            self.endian = Endianness.LittleEndian
        else:
            raise ValueError('Unsupported endian : %s' % (endian))

        sizeOfInt   = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfSizeT = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfInstr = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfNum   = unpack('<B', stream.read(1)[0:1])[0]
        floatType   = unpack('<B', stream.read(1)[0:1])[0]
        
        luatimeinfo = stream.read(6)
        if luatimeinfo != lua_time:
            raise ValueError('not match : lua time magic (since lua 5.2)')
        
        isBE = False
        if self.endian == Endianness.BigEndian:
            isBE = True
        
        bytes_readed = stream.tell()
        func = LuaByteCodeFunction52(None, self, stream, bytes_readed, sizeOfInstr, sizeOfInt, sizeOfInt, sizeOfSizeT, sizeOfNum, 0, isBE) #main
        func.SetFunctionHashid('root')
        func.SetFunctionName('<root>')
        cur_pos = func.Parse()
        self.function_top = func
        
        #support muilt src file
        return bytes_readed
    
    def _ParseLua51Common(self, stream):
        format_version = stream.read(1)
        self._CheckFormatVersion(format_version)
        endian = stream.read(1)
        if endian == b'\x00':
            self.endian = Endianness.BigEndian
        elif endian == b'\x01':
            self.endian = Endianness.LittleEndian
        else:
            raise ValueError('Unsupported endian : %s' % (endian))
        
        sizeOfInt   = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfSizeT = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfInstr = unpack('<B', stream.read(1)[0:1])[0]
        sizeOfNum   = unpack('<B', stream.read(1)[0:1])[0]
        floatType   = unpack('<B', stream.read(1)[0:1])[0]

        isBE = False
        if self.endian == Endianness.BigEndian:
            isBE = True
        
        bytes_readed = stream.tell()
        func = LuaByteCodeFunction51(None, self.eluaMode, self, stream, bytes_readed, sizeOfInstr, sizeOfInt, sizeOfInt, sizeOfSizeT, sizeOfNum, 0, isBE) #main function
        func.SetFunctionHashid('root')
        func.SetFunctionName('<root>')
        cur_pos = func.Parse()
        self.function_top = func
        
        #support muilt src file
        return bytes_readed
    
    def Parse(self):
        if self.buf is None or len(self.buf) == 0:
            raise ValueError('buf is none or empty')
        stream = BytesIO(self.buf)
        magic = stream.read(4)
        if magic != b'\x1B\x4C\x75\x61':
            raise ValueError('not a lua bytecode file')
        
        version = stream.read(1)
        if version == b'\x53':
            self.version = LuaVersion.LuaVersion53
            return self._ParseLua53Common(stream)
        elif version == b'\x52':
            self.version = LuaVersion.LuaVersion52
            return self._ParseLua52Common(stream)
        elif version == b'\x51':
            self.version = LuaVersion.LuaVersion51
            return self._ParseLua51Common(stream)
        else:
            raise TypeError('Unsupported version : %s' % (version))
    
    def _DebugPrintFunctionCalls(self, engine):
        normal_list = set()
        this_list   = set()
        imported_list = set()

        for instr in engine.mlils:
            if instr.GetOperation() == LuaMiddleOperation.NODE_CALLI:
                imported_list.add(instr.GetName())
            elif instr.GetOperation() == LuaMiddleOperation.NODE_CALLN:
                normal_list.add(instr.GetName())
            elif instr.GetOperation() == LuaMiddleOperation.NODE_CALLT:
                this_list.add(instr.GetName())
        
        print('normal function calls:')
        for name in normal_list:
            cprint(name, 'green', attrs=['bold'], file=sys.stderr)
        print('imported function calls:')
        for name in imported_list:
            cprint(name, 'blue', attrs=['bold'], file=sys.stderr)
        print('class method calls:')
        for name in this_list:
            cprint(name, 'yellow', attrs=['bold'], file=sys.stderr)
    
    def _DebugPrintMlil(self, engine):
        print('[', engine.function, '] => [%s] =>[%s]' % (engine.function.hashId, engine.function.GetFunctionName()))
        print('++++++++++++++++++++++++++++++++')
        self._DebugPrintFunctionCalls(engine)
        print('++++++++++++++++++++++++++++++++')
        for bb in engine.basicBlocks:
            bb.Print()
    
    def _TranslateWithFunction(self, func):
        engine = LuaTranslate(func.instructions, func.constants, func.upvalues, func, self.version)
        engine.TranslateCode()
        func.Engine = engine
        
        for subfunc in func.subfunctions:
            self._TranslateWithFunction(subfunc)
    
    def _DebugPrintFunc(self, func):
        self._DebugPrintMlil(func.Engine)
        for subfunc in func.subfunctions:
            self._DebugPrintFunc(subfunc)
    
    def _Lua51UpvalFixer(self, func):
        fixer = LuaUpvalFixer(func.instructions, func.upvalues, func)
        fixer.Fixer()

        for subfunc in func.subfunctions:
            self._Lua51UpvalFixer(subfunc)
    
    def _Translate51(self):
        if self.function_top == None:
            raise RuntimeError('top level function is not loaded')
        
        self._Lua51UpvalFixer(self.function_top)
        self._TranslateWithFunction(self.function_top)
        self._DebugPrintFunc(self.function_top)
    
    def Translate(self):
        if self.version == LuaVersion.LuaVersion51:
            self._Translate51()
        else:
            if self.function_top == None:
                raise RuntimeError('top level function is not loaded')
            self._TranslateWithFunction(self.function_top)
            self._DebugPrintFunc(self.function_top)
    
    def _CollectFunctions(self, func, funclist):
        funclist.append(func)
        for subfunc in func.subfunctions:
            self._CollectFunctions(subfunc, funclist)

    def _ProcessAnalysisWithFunction(self, func):
        printx = lambda x: cprint(x, 'white', 'on_cyan')
        printr = lambda x: cprint(x, 'white', 'on_yellow')
        printx('check function [%s]=>[%s]' % (func.hashId, func.GetFunctionName()))
        
        imported_map = {}
        normal_map   = {}
        this_map     = {}
        total_map    = {}

        def AddToMap(fmap, name, instr):
            if name in fmap:
                fmap[name].append(instr)
            else:
                fmap[name] = [instr]
        
        for instr in func.Engine.mlils:
            if instr.GetOperation() == LuaMiddleOperation.NODE_CALLI:
                AddToMap(imported_map, instr.GetName(), instr)  
            elif instr.GetOperation() == LuaMiddleOperation.NODE_CALLN:
                AddToMap(normal_map, instr.GetName(), instr)  
            elif instr.GetOperation() == LuaMiddleOperation.NODE_CALLT:
                AddToMap(this_map, instr.GetName(), instr)
        
        total_map.update(imported_map)
        total_map.update(normal_map)
        total_map.update(this_map)
        
        source_function = []
        target_function = []
        for k, v in total_map.items():
            if is_taint_source(k) != None:
                source_function.extend(v)
            elif is_taint_target(k) != None:
                target_function.extend(v)
        
        if len(target_function) == 0 or len(source_function) == 0:
            printx('no target call')
            return []
        
        printx('checking...')
        result = []
        for target_instr in target_function:
            modeler = LuaModeler(
                func, 
                target_instr, 
                func.instructions, 
                func.Engine.mlils, 
                func.constants, 
                func.Engine.varDefine,
                func.Engine.varUsage)
            
            if modeler.IsTainted():
                taint_list = modeler.GetTaintPath()
                for taint_item in taint_list:
                    taint_item.Print()
                    result.append(taint_item)
                printr('=======================')
                start_address, start_info, end_address, end_info = self.PrepareSourceLineInfo(taint_list, func.instructions, func.lineinfos, self.sourceLines)
                if start_address == None or start_info == None:
                    printr('start : no source code available')
                else:
                    printr('start : [%d] %s' % (start_address, start_info))
                if end_address == None or end_info == None:
                    printr('end : no source code available')
                else:
                    printr('end : [%d] %s' % (end_address, end_info))
                printr('=======================')
        return result
    
    def PrepareSourceLineInfo(self, chk_list, instructions, lineInfos, sourceLine):
        if len(chk_list) > 0:
            start = chk_list[0]
            end   = chk_list[-1]
            start_address = start.instr.GetAddress()
            end_address   = end.instr.GetAddress()

            start_info = None
            end_info   = None
            start_source_line = None
            end_source_line   = None
            if start_address != None and start_address < len(lineInfos):
                start_source_line = lineInfos[start_address]
                start_source_line -= 1
                if start_source_line < len(sourceLine):
                    start_info = sourceLine[start_source_line]
            
            if end_address != None and end_address < len(lineInfos):
                end_source_line = lineInfos[end_address]
                end_source_line -= 1
                if end_source_line < len(sourceLine):
                    end_info = sourceLine[end_source_line]
            
            return start_source_line, start_info, end_source_line, end_info
        
        return None, None, None, None

        
    def ProcessAnalysis(self):
        if self.function_top == None:
            raise RuntimeError('top level function is not loaded')
        
        funclist = []
        self._CollectFunctions(self.function_top, funclist)

        fd = None
        for func in funclist:
            chk_result = self._ProcessAnalysisWithFunction(func)
            if len(chk_result) and self.output not in ('stdout', 'stderr'):
                if fd == None:
                    fd = open(self.output, 'w')
                    if fd == None:
                        raise IOError('cannot open %s for write' % self.output)
                
                fd.write('---------------------------\n')
                fd.write('%s\n' % func.GetFunctionName())
                fd.write('%s\n' % func.hashId)
                fd.write('+++++++++++++++++++++++++++\n')
                for item in chk_result:
                    fd.write(str(item))
                    fd.write('\n')
                fd.write('=======================\n')
                start_address, start_info, end_address, end_info = self.PrepareSourceLineInfo(chk_result, func.instructions, func.lineinfos, self.sourceLines)
                if start_address == None or start_info == None:
                    fd.write('start : no source code available\n')
                else:
                    fd.write('start : [%d] %s\n' % (start_address, start_info))
                if end_address == None or end_info == None:
                    fd.write('end : no source code available\n')
                else:
                    fd.write('end : [%d] %s\n' % (end_address, end_info))
                fd.write('=======================\n')
                fd.write('---------------------------\n\n')
                
        if fd: fd.close()
        
        
        
