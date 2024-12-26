import keyboard as kb
from .modules.key_handler import handle_mod_hotkey
from .modules.models_handler import read_onload_profile, read_exit_hotkey


def main() -> None:
    profile = read_onload_profile()
    exit_hotkey = read_exit_hotkey()

    if profile:
        print(f"Loaded profile:\n{profile}")

        kb.hook(lambda event:handle_mod_hotkey(event, profile.key_layers))

    if exit_hotkey:
        print(f"\nPress \"{exit_hotkey}\" to quit")
        kb.wait(kb.get_hotkey_name(exit_hotkey))

if __name__ == "__main__":
    main()