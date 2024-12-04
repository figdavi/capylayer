
from typing import TypeAlias, Self
from enum import Enum
from pydantic import BaseModel, ConfigDict, model_validator, constr, Field, conlist

# Type aliases
KeyRemapsValues: TypeAlias = list[dict[str, str]]
ModHotkeyValues: TypeAlias = list[str]
KeyLayersValues: TypeAlias = list[dict[str, ModHotkeyValues | str | KeyRemapsValues]]
ProfilesValues: TypeAlias = dict[str, KeyLayersValues]

# Constants
SWITCH_MODE_NAME = "switch"
LOCK_MODE_NAME = "lock"


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