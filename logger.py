from colorama import Fore

def error(msg, namespace: str=__name__):
    print(f"{Fore.RED}[{namespace}: ERROR] {msg}{Fore.RESET}")

def warn(msg, namespace: str=__name__):
    print(f"{Fore.YELLOW}[{namespace}: WARNING] {msg}{Fore.RESET}")

def info(msg, namespace: str=__name__):
    print(f"[{namespace}: INFO] {msg}")