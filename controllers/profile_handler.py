from json_utils import edit_json_key, read_json_active_profile
from models.profiles import Profiles, Profile

def save_profile(profiles_json_path: str, profile: Profile) -> bool | None:
    """   
    Saves a profile in the json file.
    
    If a profile in profiles_json_path contains the same name as the given profile, 
    it overwrites it.

    Args: 
        profiles_json_path (str): the profile file's path.
        profile (Profile): the profile to save.
    Returns: 
        bool | None: True if json_data is validated against a pydantic model,
        None if an error occurs.
    """

    return edit_json_key(profiles_json_path, Profiles, ["profiles"][profile.name], profile)

def remove_profile(profiles_json_path: str, profile_name: str) -> bool | None:
    return edit_json_key(profiles_json_path, Profiles, ["profiles"][profile_name], "")

def switch_profile(profiles_json_path: str, profile_name: str) -> Profile | None:
    """   
    Changes the active profile name on the given path and returns active profile
    as a Profile istance.

    Args: 
        profiles_json_path (str): the profile file's path
        profile_name: the profile's name which the user is switching to
    Returns: 
        Profile | None: An istance of Profile class validated against a pydantic model,
        None if an error occurs. 
    """
    if not edit_json_key(profiles_json_path, Profiles, ["active_profile_name"], profile_name):
        return None
    
    return read_json_active_profile(profiles_json_path)