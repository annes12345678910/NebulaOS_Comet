from unicorn import * # pyright: ignore[reportWildcardImportFromLibrary]
from unicorn.arm64_const import * # pyright: ignore[reportWildcardImportFromLibrary]

def hook_intr(mu:Uc, intno, user_data):
    print(f"[INTERRUPT] {intno}")
    print("SVC hit → stopping emulator")
    print(mu)
    mu.emu_stop()

def hook_code(mu, address, size, user_data):
    print(f"PC=0x{address:x}, size={size}")

mu = Uc(UC_ARCH_ARM64, UC_MODE_ARM)

ADDRESS = 0x100000
mu.mem_map(ADDRESS, 2 * 1024 * 1024)

CODE = bytes.fromhex(
    "D2800020"  # mov x0, #1
    "D2800041"  # mov x1, #2  (fixed)
    "D4000001"  # svc #0
)

mu.mem_write(ADDRESS, CODE)

mu.reg_write(UC_ARM64_REG_PC, ADDRESS)

mu.hook_add(UC_HOOK_CODE, hook_code)
mu.hook_add(UC_HOOK_INTR, hook_intr)

mu.emu_start(ADDRESS, ADDRESS + len(CODE))
