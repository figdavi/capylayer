from .models import Profile
from subprocess import Popen, CalledProcessError
from pathlib import Path
import atexit
import platform

# Executable files (ahk scripts)
cur_dir = Path(__file__).parent.resolve()
ahk_dir = cur_dir / "_ahk"
exec_64_path = ahk_dir / "capylayer_ahk64.exe"
exec_32_path = ahk_dir / "capylayer_ahk32.exe"

# OS bit adressing
IS_64BIT = platform.machine().endswith("64")

def start_key_handler(profile: Profile) -> bool:
    key_layers = profile.model_dump_json(
        exclude = {"name": True, "key_layers": {"__all__": {"mod_hotkey"}}}
    )

    if not _load_ahk_script(key_layers):
        return False
    
    return True

def _load_ahk_script(data: str) -> bool:
    try:
        global process
        print("\nInitializing AHK script process...")
        process = Popen([exec_64_path if IS_64BIT else exec_32_path, data])
        print("AHK script process initialized")
        return True
    
    except FileNotFoundError as err:
        print(f"\nAHK File Error: {err}")
        print(f"Note: expected ahk executable path: \"{exec_64_path if IS_64BIT else exec_32_path}\"") 
        return False
    except CalledProcessError as err:
        print(f"\nAHK Proccess Error: {err}")
        return False
    
def _close_process() -> None:
    if process is None:
        return None
    if process.poll() is None:
        print("\nTerminating AHK script process...")
        process.terminate()
        process.wait()
        print("AHK script process terminated.")
        return None
    else:
        print("\nNo found AHK script process to terminate.")

# Closing child process at main process exit
process = None
atexit.register(_close_process)