# File contaning profiles and commands classes (imported in utils.py)
# These classes and their methods are designed to read and store data from JSON files.
# For better understanding, see profiles.json and commands.json files

from typing import Union

# Type alias
type KeyRemapsData = list[dict[str, str]]
type MappingsValuesData = list[dict[str, Union[str, KeyRemapsData]]]
type ProfileValuesData = dict[str, dict[str, MappingsValuesData]]
type DictCommand = dict[str, dict[str, str]]


class KeyRemapsItem:
    def __init__(self, key_src: str, key_dst: str) -> None:
        self.key_src = key_src
        self.key_dst = key_dst
    
    @staticmethod
    def from_json_dict(key_remaps: KeyRemapsData) -> list["KeyRemapsItem"]:
        return [
            KeyRemapsItem(
                key_remap.get("key_src", ""), 
                key_remap.get("key_dst", "")
            )
            for key_remap in key_remaps
        ]

    def __repr__(self) -> str:
        return f"\n\t(key_src: {self.key_src}, key_dst: {self.key_dst})"   
    
class MappingsItem:
    def __init__(self, mod_hotkey: str, mod_hotkey_mode: str, key_remaps: list["KeyRemapsItem"]):
        self.mod_hotkey = mod_hotkey
        self.mod_hotkey_mode = mod_hotkey_mode
        self.key_remaps = key_remaps
        self.is_active = False 

    @staticmethod
    def from_json_dict(mappings: MappingsValuesData) -> list["MappingsItem"]:
        return [
             MappingsItem(
                mod_hotkey = mapping.get("mod_hotkey", ""),
                mod_hotkey_mode = mapping.get("mod_hotkey_mode", ""),
                key_remaps = KeyRemapsItem.from_json_dict(mapping.get("key_remaps", []))
            )
            for mapping in mappings
        ]
       
        
    def __repr__(self) -> str:
        return f"\nmod_hotkey: {self.mod_hotkey}\nmod_hotkey_mode: {self.mod_hotkey_mode}\nKey remaps: {self.key_remaps}"    

class Profile:
    def __init__(self, name: str, mappings: list["MappingsItem"]) -> None:
        self.name = name
        self.mappings = mappings

    def __repr__(self) -> str:
        return f"\nProfile name: {self.name}\nMappings: {self.mappings}"

    @staticmethod
    def from_json_dict(active_profile_name: str, active_profile: ProfileValuesData) -> "Profile":
        return Profile(
            active_profile_name, 
            MappingsItem.from_json_dict(active_profile.get("mappings", []))
        )

class CommandsItem:
    def __init__(self, hotkey: str) -> None:
        self.hotkey = hotkey

    def __repr__(self) -> str:
        return f"\nhotkey: {self.hotkey}\n"
    
class DictCommands:
    @staticmethod
    def from_json_dict(commands: DictCommand) -> dict[str, "CommandsItem"]:
        return {
            command_name: CommandsItem(
                command_values.get("hotkey", "")
            )
            for command_name, command_values in commands.items()
        }