from __future__ import print_function
import enum

class Endianness(enum.IntEnum):
	LittleEndian = 0
	BigEndian    = 1

class LuaVersion(enum.IntEnum):
	LuaVersion51 = 0,
	LuaVersion52 = 1,
	LuaVersion53 = 2
