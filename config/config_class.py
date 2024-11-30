# File contaning profiles and commands classes (imported in utils.py)
# These classes and their methods are designed to read and store data from JSON files.
# For better understanding, see profiles.json and commands.json files

from typing import TypeAlias

# Type alias
KeyRemapsValues: TypeAlias = list[dict[str, str]]
ModHotkeyValues: TypeAlias = list[str]
KeyLayersValues: TypeAlias = list[dict[str, ModHotkeyValues | str | KeyRemapsValues]]
ProfilesValues: TypeAlias = dict[str, KeyLayersValues]
CommandsJson: TypeAlias = dict[str, dict[str, str]]

class KeyRemapsItem:
    def __init__(self, key_src: str, key_dst: str) -> None:
        self.key_src = key_src
        self.key_dst = key_dst
    
    @staticmethod
    def from_json_dict(key_remaps: KeyRemapsValues) -> list["KeyRemapsItem"]:
        return [
            KeyRemapsItem(
                key_remap.get("key_src", ""), 
                key_remap.get("key_dst", "")
            )
            for key_remap in key_remaps
        ]

    def __repr__(self) -> str:
        return f"\n\t(key_src: {self.key_src}, key_dst: {self.key_dst})"   
    
class KeyLayersItem:
    def __init__(self, mod_hotkey: ModHotkeyValues, mod_mode: str, key_remaps: list["KeyRemapsItem"]):
        # Handle mod_hotkey and is_active in handlers.py
        self.mod_hotkey = {mod_key: False for mod_key in mod_hotkey}
        self.mod_mode = mod_mode
        self.key_remaps = key_remaps
        self.is_active = False

    @staticmethod
    def from_json_dict(key_layers: KeyLayersValues) -> list["KeyLayersItem"]:
        return [
            KeyLayersItem(
                mod_hotkey = key_layer.get("mod_hotkey", []),
                mod_mode = key_layer.get("mod_mode", ""),
                key_remaps = KeyRemapsItem.from_json_dict(key_layer.get("key_remaps", []))
            )
            for key_layer in key_layers
        ]
       
        
    def __repr__(self) -> str:
        return f"\nmod_hotkey: {self.mod_hotkey}\nmod_mode: {self.mod_mode}\nKey remaps: {self.key_remaps}"    

class Profile:
    def __init__(self, name: str, key_layers: list["KeyLayersItem"]) -> None:
        self.name = name
        self.key_layers = key_layers

    def __repr__(self) -> str:
        return f"\nProfile name: {self.name}\nKey Layers: {self.key_layers}"

    @staticmethod
    def from_json_dict(active_profile_name: str, active_profile: ProfilesValues) -> "Profile":
        return Profile(
            active_profile_name, 
            KeyLayersItem.from_json_dict(active_profile.get("key_layers", []))
        )

class CommandsItem:
    def __init__(self, hotkey: str) -> None:
        self.hotkey = hotkey

    def __repr__(self) -> str:
        return f"\nhotkey: {self.hotkey}\n"
    
class DictCommandsItem:
    @staticmethod
    def from_json_dict(commands: CommandsJson) -> dict[str, "CommandsItem"]:
        return {
            command_name: CommandsItem(
                command_values.get("hotkey", "")
            )
            for command_name, command_values in commands.items()
        }