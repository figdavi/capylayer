from typing import TypeAlias, Self
from pydantic import BaseModel, ConfigDict, model_validator, Field, conlist

# Type aliases
CommandsJson: TypeAlias = dict[str, dict[str, str]]

# Constants
HOTKEY_JOIN_CHARACTER = '+'

class ConfigModel(BaseModel):
    model_config = ConfigDict(extra = 'forbid', strict = True)

class CommandsItem(ConfigModel):
    hotkey: conlist(str, min_length = 1) = Field(default_factory=list)  # type: ignore
    hotkey_str: str = ""

    @model_validator(mode = "after")
    def build_command_hotkey_str(self) -> Self:
        """
        Transforms a list[str] to a str joined by "+" 
         (keyboard library's format for hotkeys) 

        Args: 
            self: an istance of CommandItem
        Returns: 
            Self: an istance of CommandItem
        """
        self.hotkey_str = HOTKEY_JOIN_CHARACTER.join(self.hotkey)
        return self


class Commands(ConfigModel):
    quit: CommandsItem