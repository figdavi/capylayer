from typing import Any, Type, TypeVar, cast
from pydantic import ValidationError, FilePath
from models import Profiles, Commands

# Type Aliases
ModelType = Type[Profiles] | Type[Commands]

T = TypeVar('T', bound = Profiles | Commands)

# Constants
CONFIG_PATH = "./config/"
DEFAULT_QUIT_HOTKEY = ["ctrl", "shift", "caps lock"]

def read_config_file(file_path: FilePath, model_type: ModelType) -> T | None:
    """   
    Reads a config file and returns it as a model.
    """ 
    try:
        with open(file_path, "r") as file:
            return cast(T, model_type.model_validate_json(file.read()))
        
    except FileNotFoundError:
        print(f"Error: File not found in {file_path}")
        return None
    except (ValidationError, Exception) as err:
        print(f"Error: {err}")
        return None
    
def write_config_file(file_path: FilePath, model_type: ModelType, data: dict) -> bool | None:
    """   
    Validates data against model and writes to file.
    """ 
    try:
        with open(file_path, 'w') as file:
            data_model = model_type.model_validate(data)
            file.write(data_model.model_dump_json(indent = 4))
            return True

    except FileNotFoundError:
        print(f"Error: File not found in {file_path}")
        return None
    except (ValidationError, Exception) as err:
        print(f"Error: {err}")
        return None

def edit_config_key(file_path: FilePath, model_type: ModelType, nested_keys: list[str], value: Any) -> bool | None:
    """   
    Writes data (value) to a nested key to a config file.
    """
    model = read_config_file(file_path, model_type)
    if not model:
        return None
    
    data_dict = model.model_dump() 

    target_dict = data_dict
    try:
        for key in nested_keys[:-1]:
            if not key in target_dict or not isinstance(target_dict[key], dict):
                raise KeyError(f"Key \"{key}\" does not exist in {file_path}")
            
            target_dict = target_dict[key]

        target_dict[nested_keys[-1]] = value

        return write_config_file(file_path, model_type, data_dict)
    
    except KeyError as err:
        print(f"Error: {err}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None
    
def remove_config_key(file_path: FilePath, model_type: ModelType, nested_keys: list[str]) -> bool | None:
    """   
    Removes a nested key from config file.
    """
    model = read_config_file(file_path, model_type)
    if not model:
        return None

    data_dict = model.model_dump() 

    target_dict = data_dict

    try:
        for key in nested_keys[:-1]:
            if not key in target_dict or not isinstance(target_dict[key], dict):
                raise KeyError(f"Key \"{key}\" does not exist in {file_path} following {nested_keys}")
            
            target_dict = target_dict[key]

        
        del target_dict[nested_keys[-1]]

        return write_config_file(file_path, model_type, data_dict)
    
    except KeyError as err:
        print(f"Error: {err}")
        return None
    except (ValidationError, Exception) as err:
        print(f"Error: {err}")
        return None