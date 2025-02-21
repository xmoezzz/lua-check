from __future__ import print_function
import enum

class LuaDecompileStatus(enum.IntEnum):
    ROOT_ITEM = 0,
    FUNC_ITEM = 1,
    IF_ITEM   = 2,
    ELIF_ITEM = 3,
    ELSE_ITEM = 4,
