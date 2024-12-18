from capylayer.models.utils import edit_config_key, read_config_file
from capylayer.models.models import Profiles, Profile, Commands
from pathlib import Path
import importlib.resources

# Config files
config_dir_traversable = importlib.resources.files("capylayer.models.config")
config_dir = Path(str(config_dir_traversable))
profiles_path = config_dir / "profiles.json"
commands_path = config_dir / "commands.json"

def read_active_profile(file_path: Path = profiles_path) -> Profile | None:
    """   
    Returns a Profile model of the current active profile from file.
    """
    profiles = read_config_file(file_path, Profiles)
    if not profiles:
        return None

    try:
        active_profile_name = profiles.active_profile_name
        if not any(active_profile_name == profile_names for profile_names in profiles.profiles.keys()):
            print(f"No active profile called \"{active_profile_name}\" found in {file_path}.")
            print("Defaulting to first profile.")
            active_profile_name = next(iter(profiles.profiles))
            if not edit_config_key(file_path, Profiles, ["active_profile_name"], active_profile_name):
                return None
        
        active_profile = profiles.profiles[active_profile_name]
        return active_profile
    
    except Exception as err:
        print(f"Error: {err}")
        return None

def save_profile(profile: Profile, file_path: Path = profiles_path) -> bool | None:
    """   
    Saves a profile to file.
        
    If a profile in the file contains the same name as the given profile, 
    it overwrites it.
    """
    return edit_config_key(file_path, Profiles, ["profiles", f"{profile.name}"], profile)

def switch_profile(profile_name: str, file_path: Path = profiles_path) -> Profile | None:
    """   
    Switches to profile with the given name.
    """
    if not edit_config_key(file_path, Profiles, ["active_profile_name"], profile_name):
        return None
    
    return read_active_profile()

def remove_profile(profile_name: str, file_path: Path = profiles_path) -> bool | None:
    """
    Removes a profile from file.
    """
    return edit_config_key(file_path, Profiles, ["profiles", f"{profile_name}"], "")

def read_commands(file_path: Path = commands_path) -> Commands | None:
    """   
    Returns a Commands model from file.
    """
    try:
        return read_config_file(file_path, Commands)
    
    except Exception as err:
        print(f"Error: {err}")
        return None
    
def save_commands(commands: Commands, file_path: Path = commands_path) -> bool | None:
    """   
    Saves quit hotkey
    """
    return edit_config_key(file_path, Commands, ["quit", "hotkey"], commands.quit.hotkey)