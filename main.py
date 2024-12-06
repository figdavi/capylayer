import keyboard
from controllers.key_handler import handle_mod_hotkey
from json_utils import read_json_active_profile, read_json_commands

CONFIG_PATH = "./config/"
PROFILE_PATH = CONFIG_PATH + "profiles.json"
COMMANDS_PATH = CONFIG_PATH + "commands.json"

profile = read_json_active_profile(PROFILE_PATH)
commands = read_json_commands(COMMANDS_PATH)

print(f"Loaded profile: {profile}\n")
print(f"Loaded commands: {commands}")
if profile:
    keyboard.hook(lambda event:handle_mod_hotkey(event, profile.key_layers))

if commands:
    print(f"\nPress \"{commands.quit.hotkey_str}\" to quit")
    keyboard.wait(commands.quit.hotkey_str) 