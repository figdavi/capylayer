from .modules.models_handler import read_onload_profile, read_exit_hotkey
from .modules.models import Profile
import keyboard as kb
import platform

def call_key_handler(profile: Profile) -> bool:
    if not profile or not profile.key_layers:
        return False
    
    system = platform.system()

    if system == "Windows":
        from .modules._win_handler import start_key_handler
    elif system == "Linux" or system == "Darwin":
        from .modules._darwin_nix_handler import start_key_handler
    else:
        raise OSError(f"Error: Platform \"{system}\" is unsupported")
    
    start_key_handler(profile)
    return True


def main() -> None:
    profile = read_onload_profile()
    
    if profile:
        print(f"Loaded profile:\n{profile}")
        call_key_handler(profile)

    exit_hotkey = read_exit_hotkey()
    if exit_hotkey:
        print(f"\nPress \"{exit_hotkey}\" to quit")
        kb.wait(kb.get_hotkey_name(exit_hotkey))

if __name__ == "__main__":
    main()