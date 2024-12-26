from typing import Self, Any
from enum import Enum
from pydantic import BaseModel, ConfigDict, model_validator, Field

# Type aliases
type ModHotkeyValues = list[str]
type KeyLayersValues = list[dict[str, ModHotkeyValues | str | dict[str, str]]]
type ProfilesValues = dict[str, KeyLayersValues]
type Hotkey = list[str]

# Constants
INDENT_STR = "   "

class DataModel(BaseModel):
    model_config = ConfigDict(extra = "forbid", strict = True, revalidate_instances = "always")

class ModModeEnum(str, Enum):
    switch = "switch"
    lock = "lock"

class KeyLayer(DataModel):
    mod_hotkey: Hotkey
    mod_mode: ModModeEnum
    key_remaps: dict[str, str]

    mod_hotkey_dict: dict[str, bool] = Field(default = {}, repr = False, exclude = True)
    is_active: bool = Field(default = False, repr = False, exclude = True)
        
    @model_validator(mode = "after")
    def build_mod_hotkey_dict(self) -> Self:
        """
        Builds a dictionary for easier tracking of key presses of keys 
        contained in the modifier hotkey.
        """

        # keyboard.key_to_scan_codes() returns a tuple, where first item is the key scan code
        self.mod_hotkey_dict = {key: False for key in self.mod_hotkey}
        return self
    
    def __setattr__(self, name: str, value: Any):
        """
        Calls build_mod_hotkey_dict() if the attribute being set is mod_hotkey.
        """
        super().__setattr__(name, value)
        if name == "mod_hotkey":
            self.build_mod_hotkey_dict() # type: ignore

    def __str__(self, indent_quant: int = 0):
        indent = indent_quant * INDENT_STR
        sub_indent = (indent_quant + 1) * INDENT_STR

        key_layer_str = f"{indent}├──mod_hotkey: {self.mod_hotkey}"
        key_layer_str += f"\n{indent}├──mod_mode: {self.mod_mode}"
        key_layer_str += f"\n{indent}└──key_remaps:"
        key_layer_str += ''.join(f"\n{sub_indent}{key_src}: {key_dst}" for key_src, key_dst in self.key_remaps.items())
    
        return key_layer_str


class Profile(DataModel):
    name: str
    key_layers: list[KeyLayer]

    def __str__(self, indent_quant: int = 0):
        indent = indent_quant * INDENT_STR

        profile_str = f"{indent}├──name: {self.name}"
        profile_str += f"\n{indent}└──key_layers:"
        profile_str += ''.join(f"\n{key_layer.__str__(indent_quant + 1)}" for key_layer in self.key_layers)

        return profile_str

class ProgramConfig(DataModel):
    onload_profile_name: str
    exit_hotkey: Hotkey