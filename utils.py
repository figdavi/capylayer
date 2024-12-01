# File containing read logic functions for profiles and commands
# most functions call methods from config/config_class.py classes

import json
from typing import TypeAlias
from pydantic import ValidationError
from config.config_class import Profiles, Profile, Commands

# Type alias
KeyRemapsValues: TypeAlias = list[dict[str, str]]
ModHotkeyValues: TypeAlias = list[str]
KeyLayersValues: TypeAlias = list[dict[str, ModHotkeyValues | str | KeyRemapsValues]]
ProfilesValues: TypeAlias = dict[str, KeyLayersValues]
ProfilesJson: TypeAlias = dict[str, str | ProfilesValues]

# Constants
DEFAULT_QUIT_HOTKEY = "ctrl+shift+caps lock"


def read_json_to_string(file_json_path: str) -> str | None:
    try:
        with open(file_json_path, 'r') as file_json:
            return json.dumps(json.load(file_json))
    except FileNotFoundError:
        print(f"Error: File not found in {file_json_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {file_json_path}. {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def read_config_profile(profiles_json_path: str) -> Profile | None:
    profiles_json_string = read_json_to_string(profiles_json_path)
    
    try:
        profiles = Profiles.model_validate_json(profiles_json_string)

        active_profile_name = profiles.active_profile_name
        if not active_profile_name:
            print(f"Error: No active profile found in {profiles_json_path}. Defaulting to first profile")
            active_profile_name = next(iter(profiles.profiles))
        if not any(active_profile_name == profile_names for profile_names in profiles.profiles.keys()):
            print(f"Error: No active profile called \"{active_profile_name}\" found in {profiles_json_path}. Defaulting to first profile")
            active_profile_name = next(iter(profiles.profiles))

        active_profile = profiles.profiles[active_profile_name]
        return active_profile
    
    except ValidationError as err:
        print(f"Profile validation error:{err.json(indent = 4)}")
        raise SystemExit

def read_config_commands(commands_json_path: str) -> Commands | None:
    # dict[str, CommandsItem] to index commands

    commands_json_string = read_json_to_string(commands_json_path)
    try:
        commands = Commands.model_validate_json(commands_json_string)

        if not commands.quit.hotkey:
            print(f"Error: No hotkey found for quit command in {commands_json_path}. Defaulting to {DEFAULT_QUIT_HOTKEY}")
            commands.quit.hotkey = DEFAULT_QUIT_HOTKEY

        return commands
    
    except ValidationError as err:
        print(f"Commands validation error:{err.json(indent = 4)}")
        raise SystemExit
