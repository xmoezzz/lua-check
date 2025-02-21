from __future__ import print_function

def escape(string):
    escaped = ''
    for ch in string:
        if ch == '\n':
            escaped += '\\n'
        elif ch == '\r':
            escaped += '\\r'
        else:
            escaped += ch
    return escaped
