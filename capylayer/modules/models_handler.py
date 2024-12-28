from .io_utils import *
from .models import Profile, ProgramConfig
from typing import Literal, cast
from pathlib import Path
import platform


# Data files
modules_dir = Path(__file__).parent.resolve()
data_dir = modules_dir / "data"
program_config_path = data_dir / "program_config.json"
profiles_dir = data_dir / "profiles"

def hook_profile(profile: Profile) -> bool:
    if not profile or not profile.key_layers:
        return False
    
    system = platform.system()

    if system == "Windows":
        from ._win_handler import start_key_handler
    elif system == "Linux" or system == "Darwin":
        from ._darwin_nix_handler import start_key_handler
    else:
        raise OSError(f"Error: Platform {system} is unsupported")
    
    start_key_handler(profile)
    return True

def read_onload_profile(program_config_path: Path = program_config_path, dir_path: Path = profiles_dir) -> Profile | Literal[False]:
    """   
    Returns a Profile model of the set onload profile.
    """
    program_config = cast(ProgramConfig, read_data_file(program_config_path, ProgramConfig))
    if not program_config:
        return False
    
    profile_to_load = find_json_file(dir_path, program_config.onload_profile_name)
    if not profile_to_load:
        return False

    return cast(Profile, read_data_file(profile_to_load, Profile))

def save_profile(profile: Profile, dir_path: Path = profiles_dir) -> bool:
    """   
    Saves current profile as a json file in the given directory.
    """
    profile_to_save = find_json_file(dir_path, Profile.name)
    if not profile_to_save:
        return False

    return write_data_file(profile_to_save, Profile, profile)

def switch_profile(profile_name: str, dir_path: Path = profiles_dir) -> Profile | Literal[False]:
    """   
    Switches to profile with the given name.
    """
    profile_to_load = find_json_file(dir_path, profile_name)
    if not profile_to_load:
        return False

    return cast(Profile, read_data_file(profile_to_load, Profile))

def remove_profile(profile_name: str, dir_path: Path = profiles_dir) -> bool:
    """
    Removes a profile from file.
    """
    profile_to_remove = find_json_file(dir_path, profile_name)
    if not profile_to_remove:
        return False

    return delete_file(profile_to_remove)

def read_exit_hotkey(program_config_path: Path = program_config_path) -> list[str] | Literal[False]:
    program_config = cast(ProgramConfig, read_data_file(program_config_path, ProgramConfig))

    if not program_config:
        return False
    
    return program_config.exit_hotkey