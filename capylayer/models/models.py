from typing import TypeAlias, Self, Literal
from pydantic import BaseModel, ConfigDict, model_validator, Field, conlist
import keyboard as kb

# Type aliases
ModHotkeyValues: TypeAlias = list[str]
KeyLayersValues: TypeAlias = list[dict[str, ModHotkeyValues | str | dict[str, str]]]
ProfilesValues: TypeAlias = dict[str, KeyLayersValues]
CommandsJson: TypeAlias = dict[str, dict[str, str]]

# Constants
SWITCH_MODE_NAME = "switch"
LOCK_MODE_NAME = "lock"
INDENT_STR = "   "

class ConfigModel(BaseModel):
    model_config = ConfigDict(extra = "forbid", strict = True, revalidate_instances="always")

class KeyLayer(ConfigModel):
    mod_hotkey: conlist(str, min_length = 1) # type: ignore
    mod_hotkey_dict: dict[int, bool] = Field(default = {}, repr = False, exclude = True)
    mod_mode: Literal[SWITCH_MODE_NAME, LOCK_MODE_NAME] # type: ignore
    key_remaps: dict[str, str]
    is_active: bool = Field(default = False, repr = False, exclude = True)
        
    @model_validator(mode = "after")
    def build_mod_hotkey_dict(self) -> Self:
        """
        Builds a dictionary for easier tracking of key presses of keys 
        contained in the modifier hotkey.
        """

        # keyboard.key_to_scan_codes() returns a tuple, where first item is the key scan code
        self.mod_hotkey_dict = {kb.key_to_scan_codes(key)[0]: False for key in self.mod_hotkey}
        return self
    
    def __setattr__(self, name, value):
        """
        Calls build_mod_hotkey_dict() if the attribute being set is mod_hotkey.
        """
        super().__setattr__(name, value)
        if name == "mod_hotkey":
            self.build_mod_hotkey_dict()

    def __str__(self, indent_quant: int = 0):
        indent = indent_quant * INDENT_STR
        sub_indent = (indent_quant + 1) * INDENT_STR

        key_layer_str = f"{indent}├──mod_hotkey: {self.mod_hotkey}"
        key_layer_str += f"\n{indent}├──mod_mode: {self.mod_mode}"
        key_layer_str += f"\n{indent}└──key_remaps:"
        key_layer_str += ''.join(f"\n{sub_indent}{key_src}: {key_dst}" for key_src, key_dst in self.key_remaps.items())
    
        return key_layer_str


class Profile(ConfigModel):
    name: str
    key_layers: list[KeyLayer]

    def __str__(self, indent_quant: int = 0):
        indent = indent_quant * INDENT_STR

        profile_str = f"{indent}├──name: {self.name}"
        profile_str += f"\n{indent}└──key_layers:"
        profile_str += ''.join(f"\n{key_layer.__str__(indent_quant + 1)}" for key_layer in self.key_layers)

        return profile_str

class Profiles(ConfigModel):
    active_profile_name: str
    profiles: dict[str, Profile]

    def __str__(self, indent_quant: int = 0):
        indent = indent_quant * INDENT_STR

        profiles_str = f"{indent}├──active_profile_name: {self.active_profile_name}"
        profiles_str += f"\n{indent}└──profiles:" + ''.join(f"\n{profile.__str__(indent_quant + 1)}" for profile in self.profiles.values())

        return profiles_str

class CommandsItem(ConfigModel):
    hotkey: conlist(str, min_length = 1)  # type: ignore
    hotkey_str: str = Field(default = "", repr = False, exclude = True)

    @model_validator(mode = "after")
    def build_command_hotkey_str(self) -> Self:
        """
        Transforms a list[str] to a str joined by "+" 
         (keyboard library's format for hotkeys) 
        """
        self.hotkey_str = kb.get_hotkey_name(self.hotkey)
        return self

    def __setattr__(self, name, value):
        """
        Calls build_mod_hotkey_dict() if the attribute being set is mod_hotkey.
        """
        super().__setattr__(name, value)
        if name == "hotkey":
            self.build_command_hotkey_str()

    def __str__(self, indent_quant: int = 0):
        indent = indent_quant * INDENT_STR

        commands_str = f"{indent}└──hotkey: {self.hotkey}"

        return commands_str

class Commands(ConfigModel):
    quit: CommandsItem

    def __str__(self, indent_quant: int = 0):
        indent = indent_quant * INDENT_STR

        commands_str = f"{indent}└──quit:\n{self.quit.__str__(indent_quant + 1)}"

        return commands_str
