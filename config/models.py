from typing import TypeAlias, Self
from enum import Enum
from pydantic import BaseModel, ConfigDict, constr, model_validator, Field, conlist

# Type aliases
KeyRemapsValues: TypeAlias = list[dict[str, str]]
ModHotkeyValues: TypeAlias = list[str]
KeyLayersValues: TypeAlias = list[dict[str, ModHotkeyValues | str | KeyRemapsValues]]
ProfilesValues: TypeAlias = dict[str, KeyLayersValues]
CommandsJson: TypeAlias = dict[str, dict[str, str]]

# Constants
SWITCH_MODE_NAME = "switch"
LOCK_MODE_NAME = "lock"
HOTKEY_JOIN_CHARACTER = '+'

class ConfigModel(BaseModel):
    model_config = ConfigDict(extra = 'forbid', strict = True)

class KeyRemapsItem(ConfigModel):
    key_src: constr(min_length = 1) # type: ignore
    key_dst: constr(min_length = 1) # type: ignore

class ModModeEnum(str, Enum):
    switch = SWITCH_MODE_NAME
    lock = LOCK_MODE_NAME

class KeyLayersItem(BaseModel):
    mod_hotkey: conlist(str, min_length = 1) = Field(default_factory=list) # type: ignore
    mod_hotkey_dict: dict[str, bool] = {}
    mod_mode: ModModeEnum
    key_remaps: conlist(KeyRemapsItem, min_length = 1) = Field(default_factory=list)  # type: ignore
    is_active: bool = False
        
    @model_validator(mode = "after")
    def build_mod_hotkey_dict(self) -> Self:
        """
        Builds a dictionary for easier tracking of key presses of keys 
            contained in the modifier hotkey

        Args: 
            Self (KeyLayersItem): an istance of KeyLayersItem
        Returns: 
            KeyLayersItem: an istance of KeyLayersItem
        """
        self.mod_hotkey_dict = {key: False for key in self.mod_hotkey}
        return self

class Profile(ConfigModel):
    name: str = ""
    key_layers: list[KeyLayersItem]

    
class Profiles(ConfigModel):
    active_profile_name: str = ""
    profiles: dict[str, Profile]

class CommandItem(ConfigModel):
    hotkey: list[str]
    hotkey_str: str = ""

    @model_validator(mode = "after")
    def build_command_hotkey_str(self) -> Self:
        """
        Transforms a list[str] to a str joined by "+" 
            (keyboard library's format for hotkeys) 

        Args: 
            Self (CommandItem): an istance of CommandItem
        Returns: 
            CommandItem: an istance of CommandItem
        """
        self.hotkey_str = HOTKEY_JOIN_CHARACTER.join(self.hotkey)
        return self


class Commands(ConfigModel):
    quit: CommandItem