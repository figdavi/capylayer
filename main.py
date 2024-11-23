import keyboard
from handlers import handle_modifier_key
from utils import read_config_profile, read_config_commands

config_path = "./config/"
profiles_path = config_path + "profiles.json"
commands_path = config_path + "commands.json"

profile = read_config_profile(profiles_path)
commands = read_config_commands(commands_path)

keyboard.hook(lambda event: handle_modifier_key(event, profile))
keyboard.wait(commands["quit"].hotkey) 