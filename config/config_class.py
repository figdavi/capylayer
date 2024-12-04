from typing import TypeAlias
from enum import Enum
from pydantic import BaseModel, ConfigDict, constr, model_validator, Field

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

class KeyLayersItem(ConfigModel):
    mod_hotkey: list[constr(min_length = 1)] = Field(..., min_items=1) # type: ignore
    mod_mode: ModModeEnum
    key_remaps: list[KeyRemapsItem] = Field(..., min_items=1)
    is_active: bool = False
        
    @model_validator(mode = "after")
    def build_mod_hotkey(self):
        # Builds a mod_hotkey dictionary for easier tracking of key presses
        self.mod_hotkey = {key: False for key in self.mod_hotkey}
        return self

class Profile(ConfigModel):
    name: str = ""
    key_layers: list[KeyLayersItem]

    
class Profiles(ConfigModel):
    active_profile_name: str = ""
    profiles: dict[str, Profile]

class CommandItem(ConfigModel):
    hotkey: list[str]

    @model_validator(mode = "after")
    def build_command_hotkey(self):
        self.hotkey = HOTKEY_JOIN_CHARACTER.join(self.hotkey)
        return self


class Commands(ConfigModel):
    quit: CommandItem