import pathlib,platform
import ctypes
from typing import TYPE_CHECKING

libex = ''
if platform.system() == "Darwin": # macos
    libex = 'nebcapi.dylib'
else:
    print("C Bindings not avaliable for this parent system, reverting to Python Standard")

library_path = pathlib.Path(__file__).parent / libex

lib: ctypes.CDLL

def init():
    global lib

    lib = ctypes.CDLL(str(library_path))

    makeconnect("dict_GetValueByKeyName", [ctypes.POINTER(_cdict), ctypes.c_char_p], ctypes.c_void_p)
    makeconnect("dict_GetValueByIndex", [ctypes.POINTER(_cdict), ctypes.c_uint], ctypes.c_void_p)

def makeconnect(cfunc: str, args: list = [], res = None):
    poop: ctypes._NamedFuncPointer = getattr(lib, cfunc)
    poop.argtypes = args
    poop.restype = res

# ----------
# Dict stuff
# ----------
class _cdictkey(ctypes.Structure):
    _fields_ = [
        ('value', ctypes.c_void_p),
        ('name', ctypes.c_char_p),
        ('type', ctypes.c_uint)
    ]
    if TYPE_CHECKING:
        value: ctypes.c_void_p
        name: bytes
        type: int

class _cdict(ctypes.Structure):
    _fields_ = [
        ('keys', ctypes.POINTER(_cdictkey)),
        ('size', ctypes.c_uint)
    ]
    if TYPE_CHECKING:
        keys: ctypes._Pointer[_cdictkey]

class Dict:
    def __init__(self) -> None:
        self.cdict = _cdict()

    def get_value_by_key(self, key: str):
        return lib.dict_GetValueByKeyName(ctypes.byref(self.cdict), key.encode())
    
    def get_value_by_index(self, index: int):
        return lib.dict_GetValueByIndex(ctypes.byref(self.cdict), index)
    
    def __getitem__(self, key):
        if type(key) is str:
            return self.get_value_by_key(key)
        elif type(key) is int:
            return self.get_value_by_index(key)
        return ctypes.c_void_p(None)


def test():
    init()
    cstd = ctypes.CDLL("libc.dylib")

    cstd.malloc.argtypes = [ctypes.c_size_t]
    cstd.malloc.restype = ctypes.c_void_p

    mycdict = Dict()
    mycdict.cdict.keys = ctypes.cast(cstd.malloc(ctypes.sizeof(_cdictkey) * 3), ctypes.POINTER(_cdictkey)) # three keys

    o = ctypes.c_int(55)
    e = _cdictkey()
    e.name = b"E"
    e.value = ctypes.c_void_p(ctypes.addressof(o))
    mycdict.cdict.keys[0] = e
    mycdict.cdict.size = 3

    ptr: ctypes.c_void_p = mycdict["E"]                  # c_void_p or int address
    value = ctypes.cast(
        ptr,
        ctypes.POINTER(ctypes.c_int)
    ).contents.value

    print(value)

if __name__ == "__main__":
    test()
