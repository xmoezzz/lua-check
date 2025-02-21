from __future__ import print_function
import os
import sys
import subprocess
import argparse
import logging
import tempfile
from struct import unpack
from ByteCodeLoader import LuaByteCodeLoader
import logging
import tempfile

logger = logging.getLogger()


def RecompileLuaFile(input_file, version):
    '''
    return new file name
    '''
    tmpname  = None
    tmpname2 = None
    code = 0

    with tempfile.NamedTemporaryFile() as fd:
        tmpname = fd.name
    
    with tempfile.NamedTemporaryFile() as fd:
        tmpname2 = fd.name
    
    if version == '\x51':
        p = subprocess.Popen(['./bin/lua51/luadec', input_file, '>', tmpname])
        code = p.wait()
    elif version == '\x52':
        logging.error('Unsupported version : lua52')
        sys.exit(-1)
    
    if code != 0:
        logging.error('failed to decompile lua file : %s' % (input_file))
        sys.exit(-1)
    
    p = subprocess.Popen(['./bin/lua53/luac', '-o', tmpname2, tmpname])
    code = p.wait()

    if code != 0:
        logging.error('failed to compile')
        sys.exit(-1)
    
    if os.path.exists(tmpname2) == False:
        logging.error('bytecode file not exists')
        sys.exit(-1)
    
    return tmpname2

def CompileLuaFile(input_file):
    '''
    return new file name
    '''
    tmpname = None
    code = 0
    with tempfile.NamedTemporaryFile() as fd:
        tmpname = fd.name
    
    p = subprocess.Popen(['./bin/lua53/luac', '-o', tmpname, input_file])
    code = p.wait()
    
    if code != 0:
        logging.error('failed to compile')
        sys.exit(-1)
    
    if os.path.exists(tmpname) == False:
        logging.error('bytecode file not exists')
        sys.exit(-1)
    
    return tmpname

def GetVersionInt(version):
    return unpack('b', version)[0]

def ExecuteLuaCheck(filebytes, output, eluaMode = False):
    if filebytes is None or len(filebytes):
        logger.error('input is empty')
        return False
    
    if not isinstance(filebytes, bytes):
        logger.error('type of filebytes must be bytes --> %s', type(filebytes))
        return False
    
    try:
        tempfile = None
        with tempfile.NamedTemporaryFile() as fd:
            tempfile = fd.name
        
        with open(tempfile, 'wb') as fd:
            fd.write(filebytes)
        
        fd = open(tempfile, 'rb')
        if fd == None:
            logging.error('Unable to open %s' % (tempfile))
        magic = fd.read(4)
        fd.close()

        sourceLines = []
        if magic != b'\x1B\x4C\x75\x61':
            input_file = CompileLuaFile(input_file)
            with open(args.input, 'r') as s:
                sourceLines = s.read().splitlines()
        
        output = args.output
        elua   = False
        if args.elua != 'false':
            elua = True

        with open(input_file, 'rb') as fd:
            buf = fd.read()
            loader = LuaByteCodeLoader(buf, output, elua, sourceLines)
            loader.Parse()
            loader.Translate()
            loader.ProcessAnalysis()
            
    except Exception as e:
        logger.error('internal error : %s', str(e))
        return False

    return True

if __name__ == '__main__':
    print("======================================")
    print("       Web script static analysis     ")
    print("======================================")
    parse = argparse.ArgumentParser(description='web script check tool')
    parse.add_argument('--output', '-o', type=str, default='stdout', help='output(file/stdout)')
    parse.add_argument('--input',  '-i', type=str, required=True,    help='input lua script')
    parse.add_argument('--elua',   '-e', type=str, default='false',  help='enable elua flag')
    args = parse.parse_args()
    
    input_file = args.input
    if input_file == None or len(input_file) == 0:
        logging.error('Invalid input file')
        sys.exit(-1)
    
    if os.path.exists(input_file) == False:
        logging.error('Unable to open %s' % (input_file))
        sys.exit(-1)
    
    fd = open(input_file, 'rb')
    if fd == None:
        logging.error('Unable to open %s' % (input_file))
    magic = fd.read(4)
    fd.close()

    sourceLines = []
    if magic != b'\x1B\x4C\x75\x61':
        input_file = CompileLuaFile(input_file)
        with open(args.input) as s:
            sourceLines = s.read().splitlines()
    
    output = args.output
    elua   = False
    if args.elua != 'false':
        elua = True

    with open(input_file, 'rb') as fd:
        buf = fd.read()
        loader = LuaByteCodeLoader(buf, output, elua, sourceLines)
        loader.Parse()
        loader.Translate()
        loader.ProcessAnalysis()