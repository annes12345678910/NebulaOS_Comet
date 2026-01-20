import pathlib,platform
import ctypes

libex = ''
if platform.system() == "Darwin": # macos
    libex = 'nebcapi.dylib'
else:
    print("C Bindings not avaliable for this mode, reverting to Python Standard")

library_path = pathlib.Path(__file__).parent / libex

lib: ctypes.CDLL

def init():
    global lib

    lib = ctypes.CDLL(str(library_path))

    makeconnect("dict_GetValueByKeyName", [ctypes.POINTER(_cdict), ctypes.c_char_p], ctypes.c_void_p)

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

class _cdict(ctypes.Structure):
    _fields_ = [
        ('keys', ctypes.POINTER(_cdictkey)),
        ('size', ctypes.c_uint)
    ]

class Dict:
    def __init__(self) -> None:
        self.cdict = _cdict()

    # void* dict_GetValueByKeyName(Dictionary *dict, const char* keyName);
    def get_value_by_key(self, key: str):
        return lib.dict_GetValueByKeyName(ctypes.byref(self.cdict), key.encode())
    
    def __getitem__(self, key):
        self.get_value_by_key(key)
    

def test():
    init()

    mycdict = Dict()

if __name__ == "__main__":
    test()
