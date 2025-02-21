from __future__ import print_function
import re

lua_target_list = [
    {
        'name' : 'os.execute',
        'regex': '',
        'is_reg' : False,
        'desc' : 'command injection (os.execute)',
        'callback' : None,
        'runtime' : '',
    },
    {
        'name' : 'os.remove',
        'regex': '',
        'is_reg' : False,
        'desc' : 'delete file (os.remove)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : 'os.rename',
        'regex': '',
        'is_reg' : False,
        'desc' : 'rename file (os.rename)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : 'io.open',
        'regex': '',
        'is_reg' : False,
        'desc' : 'control file (io.open)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : 'nixio.exec',        
        'regex': '',
        'is_reg' : False,
        'desc' : 'command injection (nixio.exec)',
        'callback' : None,
        'runtime' : '',
    },
    {
        'name' : 'io.write',
        'regex' : '',
        'is_reg' : False,
        'desc' : 'write something to file(io.write)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : '',
        'regex' : '(.*)execute',
        'is_reg' : True,
        'desc' : 'command injection (execute)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : 'fork_exec',
        'regex': '',
        'is_reg' : False,
        'desc' : 'command injection (execute)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : 'ltn12_popen',
        'regex': '',
        'is_reg' : False,
        'desc' : 'command injection (execute)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : '',
        'regex' : '^strcat$',
        'is_reg' : True,
        'desc' : 'Function that concatenates two string arguments it receives. Returns the result of concatenation as string.',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : 'io.popen',
        'regex' : '',
        'is_reg' : False,
        'desc' : 'command injection(io.popen)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : 'sys.exec',
        'regex' : '',
        'is_reg' : False,
        'desc' : 'command injection(sys.exec)',
        'callback' : None,
        'runtime' : ''
    },
    {
        'name' : '',
        'regex' : '(.*)exec',
        'is_reg' : True,
        'desc' : 'command injection (execute)',
        'callback' : None,
        'runtime' : ''
    }
]


lua_source_list = [
    {
        'name' : 'luci.http.formvalue',
        'regex': '',
        'is_reg' : False,
        'callback' : None
    },
    {
        'name' : '',
        'regex': '^cgilua.QUERY.',
        'is_reg' : True,
        'callback' : None
    },
    {
        'name' : 'os.getenv',
        'regex' : '',
        'is_reg' : False,
        'callback' : None
    },
    #D-Link
    #teamf1lualib/db lib
    {
        'name' : 'db.getAttribute',
        'regex' : '',
        'is_reg' : False,
        'callback' : None
    },
    {
        'name' : 'cgilua.urlcode.parsequery',
        'regex' : '',
        'is_reg' : False,
        'callback' : None
    }
]


lua_tfor_list = [
    {
        'name' : 'pairs',
        'regex' : '',
        'is_reg' : False
    },
    {
        'name' : 'ipairs',
        'regex' : '',
        'is_reg' : False
    }
]

def is_taint_target(name):
    for item in lua_target_list:
        if item['is_reg'] == True:
            matched = re.match(item['regex'], name)
            if matched:
                return item
        else:
            if item['name'] == name:
                return item
    return None

def is_taint_source(name):
    for item in lua_source_list:
        if item['is_reg'] == True:
            matched = re.match(item['regex'], name)
            if matched:
                return item
        else:
            if item['name'] == name:
                return item
    return None

def is_tfor_call(name):
    for item in lua_tfor_list:
        if item['is_reg'] == True:
            matched = re.match(item['regex'], name)
            if matched:
                return item
        else:
            if item['name'] == name:
                return item
    return None

def add_tfor_call(name, regex, is_regex):
    item = {}
    item['name']   = name
    item['regex']  = regex
    item['is_reg'] = is_regex
    lua_tfor_list.append(item)

