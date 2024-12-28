import keyboard as kb
from .modules.models_handler import read_onload_profile, read_exit_hotkey, hook_profile

def main() -> None:
    profile = read_onload_profile()
    
    if profile:
        print(f"Loaded profile:\n{profile}")
        hook_profile(profile)

    exit_hotkey = read_exit_hotkey()
    if exit_hotkey:
        print(f"\nPress \"{exit_hotkey}\" to quit")
        kb.wait(kb.get_hotkey_name(exit_hotkey))

if __name__ == "__main__":
    main()