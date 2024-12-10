from config_utils import CONFIG_PATH, edit_config_key, read_config_file
from pydantic import FilePath
from models import Profiles, Profile, Commands

# Constants
PROFILES_PATH: FilePath = FilePath(CONFIG_PATH + "profiles.json")
COMMANDS_PATH: FilePath = FilePath(CONFIG_PATH + "commands.json")

def read_active_profile() -> Profile | None:
    """   
    Returns a Profile model of the current active profile from file.
    """
    profiles = read_config_file(PROFILES_PATH, Profiles)
    if not profiles:
        return None

    try:

        active_profile_name = profiles.active_profile_name
        if not any(active_profile_name == profile_names for profile_names in profiles.profiles.keys()):
            print(f"No active profile called \"{active_profile_name}\" found in {PROFILES_PATH}.")
            print("Defaulting to first profile.")
            active_profile_name = next(iter(profiles.profiles))
            if not edit_config_key(PROFILES_PATH, Profiles, ["active_profile_name"], active_profile_name):
                return None
        
        active_profile = profiles.profiles[active_profile_name]
        return active_profile
    
    except Exception as err:
        print(f"Error: {err}")
        return None

def save_profile(profile: Profile) -> bool | None:
    """   
    Saves a profile to file.
        
    If a profile in the file contains the same name as the given profile, 
    it overwrites it.
    """
    return edit_config_key(PROFILES_PATH, Profiles, ["profiles", f"{profile.name}"], profile)

def switch_profile(profile_name: str) -> Profile | None:
    """   
    Switches to profile with the given name.
    """
    if not edit_config_key(PROFILES_PATH, Profiles, ["active_profile_name"], profile_name):
        return None
    
    return read_active_profile()

def remove_profile(profile_name: str) -> bool | None:
    """
    Removes a profile from file.
    """
    return edit_config_key(PROFILES_PATH, Profiles, ["profiles", f"{profile_name}"], "")

def read_commands() -> Commands | None:
    """   
    Returns a Commands model from file.
    """
    try:
        return read_config_file(COMMANDS_PATH, Commands)
    
    except Exception as err:
        print(f"Error: {err}")
        return None
    
def save_commands(commands: Commands) -> bool | None:
    """   
    Saves quit hotkey
    """
    return edit_config_key(COMMANDS_PATH, Commands, ["quit", "hotkey"], commands.quit.hotkey)