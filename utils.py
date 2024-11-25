# File containing read logic functions for profiles and commands
# most functions call methods from config/config_class.py classes

import json
from typing import Union
from config.config_class import Profile, DictCommands, CommandsItem

type KeyRemapsData = list[dict[str, str]]
type MappingsData = dict[str, list[dict[str, Union[str, KeyRemapsData]]]]
type ProfileData = dict[str, MappingsData]
type ProfilesData = dict[str, Union[str, ProfileData]]


def load_read_json(file_json_path: str) -> Union[None, ProfilesData]:
    try:
        with open(file_json_path, 'r') as file_json:
            return json.load(file_json)
    except FileNotFoundError:
        print(f"Error: File not found in {file_json_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {file_json_path}. {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def read_config_profile(profiles_json_path: str) -> Union[None, Profile]:
    profiles_json = load_read_json(profiles_json_path)
    if profiles_json is None:
        return None
    
    profiles = profiles_json.get("profiles", {})
    if not profiles_json:
        print(f"Error: No profiles found in {profiles_json_path}")
        return None

    active_profile_name = profiles_json.get("active_profile_name", "")
    if not active_profile_name:
        print(f"Error: No active profile found in {profiles_json_path}. Defaulting to first profile")
        active_profile_name = next(iter(profiles))
    

    active_profile = profiles.get(active_profile_name, {})
    if not active_profile:
        print(f"Error: No active profile called \"{active_profile_name}\"found in {profiles_json_path}. Defaulting to first profile")
        active_profile_name = next(iter(profiles))
        active_profile = profiles.get(active_profile_name, {})


    return Profile.from_json_dict(active_profile_name, active_profile)

def read_config_commands(commands_json_path: str) -> Union[None, dict[str, CommandsItem]]:
    # dict[str, CommandsItem] makes possible to access commands by 
    #  random access with the command's name

    commands_json = load_read_json(commands_json_path)
    if commands_json is None:
        return None
     
    return DictCommands.from_json_dict(commands_json)
