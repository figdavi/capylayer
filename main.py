# File containing profile and commands from config folder
# it calls handle_modifier_key in handlers.py everytime a key is pressed

import keyboard
from handlers import handle_mod_hotkey
from utils import read_config_profile, read_config_commands

config_path = "./config/"
profiles_path = config_path + "profiles.json"
commands_path = config_path + "commands.json"

profile = read_config_profile(profiles_path)
if not profile:
    raise SystemExit

commands = read_config_commands(commands_path)
if not commands:
    raise SystemExit

if not commands["quit"].hotkey:
    print(f"Error: quit command not found in {commands_path}")
    raise SystemExit

print(f"Loaded profile: {profile}\n")
print(f"Loaded commands: {commands}")

keyboard.hook(lambda event:handle_mod_hotkey(event, profile.key_layers))

print(f"\nPress \"{commands["quit"].hotkey}\" to quit")
keyboard.wait(commands["quit"].hotkey) 