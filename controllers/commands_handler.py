from pydantic import FilePath
from config_utils import CONFIG_PATH, edit_config_key, read_config_file, write_config_file
from models import Commands

# Constants
COMMANDS_PATH: FilePath = FilePath(CONFIG_PATH + "commands.json")

def read_commands() -> Commands | None:
    """   
    Returns a Commands model from file.
    """
    try:
        return read_config_file(COMMANDS_PATH, Commands)
    
    except Exception as err:
        print(f"Error: {err}")
        return None
    
def save_commands(commands: Commands) -> bool | None:
    """   
    Saves quit hotkey
    """
    return edit_config_key(COMMANDS_PATH, Commands, ["quit", "hotkey"], commands.quit.hotkey)