import json
from typing import TypeAlias, Any, Type
from pydantic import ValidationError, BaseModel
from models.profiles import Profiles, Profile, ProfilesValues
from models.commands import Commands

# Type aliases
ProfilesJson: TypeAlias = dict[str, str | ProfilesValues]

# Constants
DEFAULT_QUIT_HOTKEY = ["ctrl", "shift", "caps lock"]

def read_json_file(json_file_path: str) -> dict | None:
    """   
    Reads a json file and returns a json object.

    Args: 
        json_file_path (str): the file's path.
    Returns: 
        dict | None: a python dictionary containing the json file's data if 
        read successfully, None if an error occurs.
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
    
def write_json_file(json_file_path: str, json_data: dict) -> bool | None:
    """   
    Writes a dict to a file in json format.

    Args: 
        json_file_path (str): the file's path.
        json_data (dict): the data (dict) being written to the file.
    Returns: 
        bool | None: True if the data is successfully writen to the file,
        None if an error occurs.
    """ 
    try:
        with open(json_file_path, 'w') as file_json:
            json.dump(json_data, file_json, indent = 4)
            return True

    except FileNotFoundError:
        print(f"Error: File not found in {json_file_path}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None

def create_json_file(json_file_path: str, model: Type[BaseModel], json_data: dict) -> bool | None:
    """   
    Validates the given data and writes to the file with if validated.

    Args: 
        json_file_path (str): the file's path.
        model (Type[BaseModel]): a pydantic model.
        json_data (dict): the data (dict) being written to the file.
    Returns: 
        bool | None: True if the given data is validated against the pydantic model,
        None if an error occurs.
    """ 
    try:
        model.model_validate_json(json.dumps(json_data))
        return write_json_file(json_file_path, json_data)
            
    except ValidationError as err:
        print(f"Error:{err.json(indent = 4)}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None


def update_json_file(json_file_path: str, model: Type[BaseModel], json_data: dict) -> bool | None:
    """   
    Validates the given file's content and the given data and writes to the file.

    Args: 
        json_file_path (str): the file's path.
        model (Type[BaseModel]): a pydantic model.
        json_data (dict): the data (dict) being written to the file.
    Returns: 
        bool | None: True if the given data is validated against the pydantic model,
        None if an error occurs.
    """ 
    try:
        model.model_validate_json(json.dumps(read_json_file(json_file_path)))
        model.model_validate_json(json.dumps(json_data))
        return write_json_file(json_file_path, json_data)
            
    except ValidationError as err:
        print(f"Error:{err.json(indent = 4)}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None

def edit_json_key(json_file_path: str, model: Type[BaseModel], nested_keys: list[str], value: Any) -> bool | None:
    """   
    Modifies a nested key's value in a json file and validates.

    Args: 
        json_file_path (str): the file's path.
        model (Type[BaseModel]): the pydantic model of data contained in the given file.
        nested_keys (list[str]): a list of keys to be accessed in a nested behaviour on the dict generated from the read json file.
        value (Any): value to be assigned to the attribute.
    Returns: 
        bool | None: True if the modified data is validated against the pydantic model,
        False if the file is empty, None if an error occurs.
    """
    json_data = read_json_file(json_file_path)
    if not json_data:
        return None

    target_dict = json_data

    try:
        for key in nested_keys[:-1]:
            if not key in target_dict or not isinstance(target_dict[key], dict):
                raise KeyError(f"Key {key} does not exist in JSON {json_file_path}")
            
            target_dict = target_dict[key]

        target_dict[nested_keys[-1]] = value
        return update_json_file(json_file_path, model, json_data)
    
    except KeyError as err:
        print(f"Error: {err}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None

def read_json_profiles(profiles_json_path: str) -> Profiles | None:
    """   
    Builds a profiles model, validates it and returns it.

    Args: 
        profiles_json_path (str): the profile file's path.
    Returns: 
        Profile | None: An istance of Profile class if the read data is 
        succesfully validated, None if an error occurs.
    """
    profiles_json = read_json_file(profiles_json_path)
    if not profiles_json:
        return None

    try:
        profiles = Profiles.model_validate_json(json.dumps(profiles_json))

        if not profiles.profiles:
            raise ValueError(f"No profile found in {profiles_json_path}")
        
        return profiles
    
    except ValidationError as err:
        print(f"Error:{err.json(indent = 4)}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None

def read_json_active_profile(profiles_json_path: str) -> Profile | None:
    """   
    Identifies the active profile in the file, builds a profile model, validates it and returns it.

    Args: 
        profiles_json_path (str): the profile file's path.
    Returns:
        Profile | None: An istance of Profile class if the read data is 
        succesfully validated, None if an error occurs.
    """
    profiles_json = read_json_file(profiles_json_path)
    if not profiles_json:
        return None

    try:
        profiles = Profiles.model_validate_json(json.dumps(profiles_json))

        if not profiles.profiles:
            raise ValueError(f"No profile found in {profiles_json_path}")

        active_profile_name = profiles.active_profile_name
        if not any(active_profile_name == profile_names for profile_names in profiles.profiles.keys()):
            print(f"Error: No active profile called \"{active_profile_name}\" found in {profiles_json_path}. Defaulting to first profile")
            active_profile_name = next(iter(profiles.profiles))
            if not edit_json_key(profiles_json_path, Profiles, ["active_profile_name"], active_profile_name):
                return None
        
        active_profile = profiles.profiles[active_profile_name]
        return active_profile
    
    except ValidationError as err:
        print(f"Error:{err.json(indent = 4)}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None

def read_json_commands(commands_json_path: str) -> Commands | None:
    """   
    Builds a Commands model, validates it and returns it.

    Args: 
        commands_json_path (str): the commands file's path.
    Returns: 
        Commands | None: An istance of Commands class if the read data is 
        succesfully validated, None if an error occurs.
    """
    commands_json_str = read_json_file(commands_json_path)
    if not commands_json_str:
        return None
    try:
        commands = Commands.model_validate_json(json.dumps(commands_json_str))
        return commands
    
    except ValidationError as err:
        print(f"Error:{err.json(indent = 4)}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None
