from __future__ import print_function
import os
import sys
import subprocess
import shutil
import uuid


def check(filename):
    hashname = uuid.uuid4().hex
    output = './result/' + hashname + '.txt'
    try:
        print("processing -> %s" % filename)
        p = subprocess.Popen(['python', 'LuaChecker.py', '-i', filename, '-o', output])
        code = p.wait()
        print('code = %x' % code)
        if code != 0:
            return False
    except:
        return False
    
    if os.path.isfile(output):
        ref_output = './result/' + hashname + '.ref.txt'
        with open(ref_output, 'w') as fd:
            fd.write(filename)
    return True

def scan(root):
    for (dirpath, dirnames, filenames) in os.walk(root):
        for file in filenames:
            yield os.path.join(dirpath, file)

def copy_crash_sample(filename):
    try:
        dest = os.path.join('./crashes', os.path.basename(filename))
        shutil.copyfile(filename, dest)
    except:
        pass

if __name__ == '__main__':
    cnt = 0
    if len(sys.argv) < 2:
        sys.exit(-1)
    root = sys.argv[1]

    for filename in scan(root):
        if filename.endswith('.lua'):
            status = check(filename)
            print('%d checked' % cnt)
            if status == False:
                copy_crash_sample(filename)
            cnt += 1
        else:
            try:
                lua_magic = '#!/usr/bin/lua'
                with open(filename, 'r') as fd:
                    buf = fd.read(14)
                    if buf == lua_magic:
                        status = check(filename)
                        print('%d checked' % cnt)
                        if status == False:
                            copy_crash_sample(filename)
                        cnt += 1
            except:
                pass
        with open('/tmp/LuaScanner.unix', 'w') as fd:
            fd.write("%d\n" % cnt)



