
from typing import TypeAlias, Self, Literal
from pydantic import BaseModel, ConfigDict, model_validator, constr, Field, conlist

# Type aliases
ModHotkeyValues: TypeAlias = list[str]
KeyLayersValues: TypeAlias = list[dict[str, ModHotkeyValues | str | dict[str, str]]]
ProfilesValues: TypeAlias = dict[str, KeyLayersValues]
CommandsJson: TypeAlias = dict[str, dict[str, str]]

# Constants
SWITCH_MODE_NAME: str = "switch"
LOCK_MODE_NAME: str = "lock"
HOTKEY_JOIN_CHARACTER = '+'


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra = "forbid", strict = True, revalidate_instances="always")

class KeyLayersItem(ConfigModel):
    mod_hotkey: conlist(str, min_length = 1) # type: ignore
    mod_hotkey_dict: dict[str, bool] = Field(default = {}, repr = False, exclude = True)
    mod_mode: Literal[SWITCH_MODE_NAME, LOCK_MODE_NAME] # type: ignore
    key_remaps: dict[str, str]
    is_active: bool = Field(default = False, repr = False, exclude = True)
        
    @model_validator(mode = "after")
    def build_mod_hotkey_dict(self) -> Self:
        """
        Builds a dictionary for easier tracking of key presses of keys 
        contained in the modifier hotkey.
        """
        self.mod_hotkey_dict = {key: False for key in self.mod_hotkey}
        return self
    
    def __setattr__(self, name, value):
        """
        Calls build_mod_hotkey_dict() if the attribute being set is mod_hotkey.
        """
        super().__setattr__(name, value)
        if name == "mod_hotkey":
            self.build_mod_hotkey_dict()

class Profile(ConfigModel):
    name: str
    key_layers: list[KeyLayersItem]

class Profiles(ConfigModel):
    active_profile_name: str
    profiles: dict[str, Profile]

class CommandsItem(ConfigModel):
    hotkey: conlist(str, min_length = 1)  # type: ignore
    hotkey_str: str = Field(default = "", repr = False, exclude = True)

    @model_validator(mode = "after")
    def build_command_hotkey_str(self) -> Self:
        """
        Transforms a list[str] to a str joined by "+" 
         (keyboard library's format for hotkeys) 
        """
        self.hotkey_str = HOTKEY_JOIN_CHARACTER.join(self.hotkey)
        return self


class Commands(ConfigModel):
    quit: CommandsItem