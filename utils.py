# File containing read logic functions for profiles and commands
# most functions call methods from config/config_class.py classes

import json
from config.config_class import Profile, KeyRemapsItem, MappingsItem, CommandsItem

# Returns a dictionary containing json's file content
def load_read_json(profiles_path):
    with open(profiles_path, 'r') as profiles_file:
        return json.load(profiles_file)

# Reads active profile value in profile.json and
# Returns a instance of Profile class containing profile name and mappings (see config/config_class.py)
def read_config_profile(profiles_path):
    profiles_json = load_read_json(profiles_path)

    active_profile_name = profiles_json["active_profile"]
    active_profile = profiles_json["profiles"][active_profile_name]

    return Profile.from_json(active_profile)

# Returns a **dictionary** where key = command name : value = instance of CommandsItem class
# (so its possible to access the command by random access)
# CommandsItem contains the command hotkey (see config/config_class.py)
def read_config_commands(commands_path):
    commands_json = load_read_json(commands_path)
    
    return CommandsItem.from_json(commands_json)
