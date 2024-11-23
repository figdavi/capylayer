import json
from config.config_class import Profile, KeyRemapsItem, MappingsItem, CommandsItem

def load_read_json(profiles_path):
    with open(profiles_path, 'r') as profiles_file:
        return json.load(profiles_file)

def read_config_profile(profiles_path):
    profiles_json = load_read_json(profiles_path)

    active_profile_name = profiles_json["active_profile"]
    active_profile = profiles_json["profiles"][active_profile_name]

    return Profile.from_json(active_profile)

def read_config_commands(commands_path):
    commands_json = load_read_json(commands_path)
    
    return CommandsItem.from_json(commands_json)
