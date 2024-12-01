# File containing profile and commands from config folder
# it calls handle_modifier_key in handlers.py everytime a key is pressed

import keyboard
from handlers import handle_mod_hotkey
from utils import read_config_profile, read_config_commands

CONFIG_PATH = "./config/"
PROFILE_PATH = CONFIG_PATH + "profiles.json"
COMMANDS_PATH = CONFIG_PATH + "commands.json"

profile = read_config_profile(PROFILE_PATH)
commands = read_config_commands(COMMANDS_PATH)

print(f"Loaded profile: {profile}\n")
print(f"Loaded commands: {commands}")

keyboard.hook(lambda event:handle_mod_hotkey(event, profile.key_layers))

print(f"\nPress \"{commands.quit.hotkey}\" to quit")
keyboard.wait(commands.quit.hotkey) 