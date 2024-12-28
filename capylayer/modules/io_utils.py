from typing import Any, Type, Literal
from pydantic import ValidationError
from .models import DataModel
from pathlib import Path

def read_data_file(file_path: Path, model_type: Type[DataModel]) -> DataModel | Literal[False]:
    """   
    Reads a data file and returns it as a model.
    """ 
    try:
        return model_type.model_validate_json(file_path.read_text())

    except FileNotFoundError:
        print(f"Read Data Error: File not found in {file_path}")
        return False
    except (ValidationError, Exception) as err:
        print(f"Read Data Error: {err}")
        return False
    
def write_data_file(file_path: Path, model_type: Type[DataModel], data: Any) -> bool:
    """   
    Validates data against model and writes to file.

    Models are always validated when edited, but to prevent writing
    the wrong model to file, the data is validated again.
    """ 
    try:
        data_model = model_type.model_validate(data)
        file_path.write_text(
            data_model.model_dump_json(
                indent = 4, exclude = {"key_layers": {"__all__": {"mod_hotkey_dict", "is_active"}}}
            )
        )
        return True

    except FileNotFoundError:
        print(f"Write Data Error: File not found in {file_path}")
        return False
    except (ValidationError, Exception) as err:
        print(f"Write Data Error: {err}")
        return False

def edit_data_key(file_path: Path, model_type: Type[DataModel], nested_keys: list[str], value: Any) -> bool:
    """   
    Writes data (value) to a nested key to a data file.
    """
    model = read_data_file(file_path, model_type)
    if not model:
        return False
    
    data_dict = model.model_dump() 

    walk_dict = data_dict
    try:
        for key in nested_keys[:-1]:
            if not key in walk_dict or not isinstance(walk_dict[key], dict):
                raise KeyError(f"Key \"{key}\" does not exist in {file_path}")
            
            walk_dict = walk_dict[key]

        walk_dict[nested_keys[-1]] = value

        return write_data_file(file_path, model_type, data_dict)
    
    except (Exception, ValidationError, KeyError) as err:
        print(f"Edit Data Error: {err}")
        return False
    
def delete_file(file_path: Path) -> bool:
    """   
    Deletes a file. 
    """
    try:
        file_path.unlink()
        return True
    except FileNotFoundError:
        print(f"Delete Error: File not found in {file_path}")
        return False
    
def find_json_file(dir_path: Path, file_name: str) -> Path | Literal[False]:
    """
    Returns the first json file path with the given name in the given directory.
    """
    try:
        return next(dir_path.glob(f"{file_name}.json"))
    except StopIteration:
        print(f"JSON Error: file \"{file_name}.json\" not found in {dir_path}")
        return False
