import json
from typing import TypeAlias, Any
from pydantic import ValidationError
from config.config_class import Profiles, Profile, Commands

# Type aliases
KeyRemapsValues: TypeAlias = list[dict[str, str]]
ModHotkeyValues: TypeAlias = list[str]
KeyLayersValues: TypeAlias = list[dict[str, ModHotkeyValues | str | KeyRemapsValues]]
ProfilesValues: TypeAlias = dict[str, KeyLayersValues]
ProfilesJson: TypeAlias = dict[str, str | ProfilesValues]

# Constants
DEFAULT_QUIT_HOTKEY = "ctrl+shift+caps lock"


def read_json_file(json_file_path: str) -> str | None:
    try:
        with open(json_file_path, 'r') as file_json:
            return json.load(file_json)
        
    except FileNotFoundError:
        print(f"Error: File not found in {json_file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_file_path}. {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def write_json_file(json_file_path: str, json_data: dict) -> None:
    try:
        with open(json_file_path, 'w') as file_json:
            json.dump(json_data, file_json, indent = 4)

    except FileNotFoundError:
        print(f"Error: File not found in {json_file_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def update_json_file(json_file_path: str, model_class: type, json_data: dict) -> None:
    try:
        model_class.model_validate_json(json.dumps(json_data))
        write_json_file(json_file_path, json_data)
        return True
            
    except ValidationError as err:
        print(f"Validation error:{err.json(indent = 4)}")
        return None
    
def edit_json_property(json_file_path: str, model_class: type, property_name: str, value: Any) -> None:
    try:
        json_data = read_json_file(json_file_path)
        if not json_data:
            return None
        
        json_data[property_name] = value

        if not update_json_file(json_file_path, model_class, json_data):
            return None
    
    except FileNotFoundError:
        print(f"Error: File not found in {json_file_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def read_config_profile(profiles_json_path: str) -> Profile | None:
    profiles_json = read_json_file(profiles_json_path)
    if not profiles_json:
        return None
    
    try:
        profiles = Profiles.model_validate_json(json.dumps(profiles_json))

        active_profile_name = profiles.active_profile_name
        if not active_profile_name:
            print(f"Error: No active profile found in {profiles_json_path}. Defaulting to first profile")
            active_profile_name = next(iter(profiles.profiles))
            if not edit_json_property(profiles_json_path, Profiles, "active_profile_name", active_profile_name):
                return None
        if not any(active_profile_name == profile_names for profile_names in profiles.profiles.keys()):
            print(f"Error: No active profile called \"{active_profile_name}\" found in {profiles_json_path}. Defaulting to first profile")
            active_profile_name = next(iter(profiles.profiles))
            if not edit_json_property(profiles_json_path, Profiles, "active_profile_name", active_profile_name):
                return None
        
        active_profile = profiles.profiles[active_profile_name]
        return active_profile
    
    except ValidationError as err:
        print(f"Validation error:{err.json(indent = 4)}")
        return None

def read_config_commands(commands_json_path: str) -> Commands | None:
    commands_json_string = read_json_file(commands_json_path)

    try:
        commands = Commands.model_validate_json(json.dumps(commands_json_string))
        if not commands.quit.hotkey:
            print(f"Error: No hotkey found for quit command in {commands_json_path}. Defaulting to {DEFAULT_QUIT_HOTKEY}")
            commands.quit.hotkey = DEFAULT_QUIT_HOTKEY

        return commands
    
    except ValidationError as err:
        print(f"Validation error:{err.json(indent = 4)}")
        return None
