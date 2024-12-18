import keyboard as kb
from capylayer.controllers.key_handler import handle_mod_hotkey
from capylayer.controllers.models_handler import read_active_profile, read_commands


def main() -> None:
    profile = read_active_profile()
    commands = read_commands()

    print(f"Loaded profile:\n{profile}")
    print(f"Loaded commands:\n{commands}")

    if profile:
        kb.hook(lambda event:handle_mod_hotkey(event, profile.key_layers))

    if commands:
        print(f"\nPress \"{commands.quit.hotkey_str}\" to quit")
        kb.wait(commands.quit.hotkey_str)

if __name__ == "__main__":
    main()