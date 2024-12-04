import json
from typing import TypeAlias, Any, Type
from pydantic import ValidationError, BaseModel
from models.profiles import Profiles, Profile, ProfilesValues
from models.commands import Commands, CommandItem

# Type aliases
ProfilesJson: TypeAlias = dict[str, str | ProfilesValues]

# Constants
DEFAULT_QUIT_HOTKEY = ["ctrl", "shift", "caps lock"]

def read_json_file(json_file_path: str) -> str | None:
    """   
    Returns a json object

    Args: 
        json_file_path (str): the file's path
    Returns: 
        dict: a python dictionary containing the json file's data
    """ 
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
    """   
    Writes a dict to a file in json format

    Args: 
        json_file_path (str): the file's path
        json_data (dict): the data (dict) being written to the file
    Returns: 
        None
    """ 
    try:
        with open(json_file_path, 'w') as file_json:
            json.dump(json_data, file_json, indent = 4)

    except FileNotFoundError:
        print(f"Error: File not found in {json_file_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def update_json_file(json_file_path: str, model_class: Type[BaseModel], json_data: dict) -> bool | None:
    """   
    Validates the given json_data (dict) against a Pydantic class model
        and writes to the file with if validated

    Args: 
        json_file_path (str): the file's path
        model_class (Type[BaseModel]): a class model
        json_data (dict): the data (dict) being written to the file
    Returns: 
        bool | None: True if json_data is validated against the class model
    """ 
    try:
        model_class.model_validate_json(json.dumps(json_data))
        write_json_file(json_file_path, json_data)
        return True
            
    except ValidationError as err:
        print(f"Validation error:{err.json(indent = 4)}")
        return None
    
def edit_json_attribute(json_file_path: str, model_class: Type[BaseModel], attribute_name: str, value: Any) -> bool | None:
    """   
    Validates the given json_data (dict) against a Pydantic class model
        and writes to the file with if validated

    Args: 
        json_file_path (str): the file's path
        model_class (Type[BaseModel]): a class model
        attribute_name (str): name of an attribute contained in the passed class model
        value (Any): value to be assigned to the attribute
    Returns: 
        bool | None: True if json_data is validated against the class model
    """
    try:
        json_data = read_json_file(json_file_path)
        if not json_data:
            return None
        
        if not isinstance(json_data, dict):
            raise ValueError("Value error: json_data is not a valid dictionary")

        json_data[attribute_name] = value

        if not update_json_file(json_file_path, model_class, json_data):
            return None
        
        return True
    
    except FileNotFoundError:
        print(f"Error: File not found in {json_file_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def read_json_profile(profiles_json_path: str) -> Profile | None:
    """   
    Reads the profiles file identifies the active profile, builds a profile 
        class model, validates it and returns it as an istance of Profile class

    Args: 
        profiles_json_path (str): the profile file's path
    Returns: 
        Profile | None: An istance of Profile class
    """
    profiles_json = read_json_file(profiles_json_path)
    if not profiles_json:
        return None
    
    try:
        profiles = Profiles.model_validate_json(json.dumps(profiles_json))

        active_profile_name = profiles.active_profile_name
        if not any(active_profile_name == profile_names for profile_names in profiles.profiles.keys()):
            print(f"Error: No active profile called \"{active_profile_name}\" found in {profiles_json_path}. Defaulting to first profile")
            active_profile_name = next(iter(profiles.profiles))
            if not edit_json_attribute(profiles_json_path, Profiles, "active_profile_name", active_profile_name):
                return None
        
        active_profile = profiles.profiles[active_profile_name]
        return active_profile
    
    except ValidationError as err:
        print(f"Validation error:{err.json(indent = 4)}")
        return None

def read_json_commands(commands_json_path: str) -> Commands | None:
    """   
    Reads the commands file, builds a Commands class model, validates it and 
        returns it as an istance of Commands class

    Args: 
        commands_json_path (str): the commands file's path
    Returns: 
        Commands | None: An istance of Commands class
    """
    commands_json_str = read_json_file(commands_json_path)
    if not commands_json_str:
        return None

    try:
        commands = Commands.model_validate_json(json.dumps(commands_json_str))

        return commands
    
    except ValidationError as err:
        print(f"Validation error:{err.json(indent = 4)}")
        return None
