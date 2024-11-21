import keyboard
import json

config_file_name = "config.json"
quit_command = "ctrl+shift+caps lock" # Default
profiles = []

class KeyRemap:
    def __init__(self, key_src, key_dst):
        self.key_src = key_src
        self.key_dst = key_dst
    
    def __repr__(self):
        return f"\n\t(key_src: {self.key_src}, key_dst: {self.key_dst})"        

class Profile:
    def __init__(self, mod_hotkey, key_remaps, is_active):
        self.mod_hotkey = mod_hotkey
        self.key_remaps = key_remaps
        self.is_active = is_active

    def __repr__(self):
        return f"mod_key: {self.mod_hotkey }\nkey_remaps: {self.key_remaps}"

def read_config(file_name, profile_name):
    with open(file_name, 'r') as config_file:
        config_json = json.load(config_file)

    for config_key, config_value in config_json.items():
        if config_key == "profiles":
            read_config_profiles(config_value, profile_name)
        elif config_key == "commands":
            pass

def read_config_profiles(config_profiles, profile_name):
        for profile_json in config_profiles[profile_name]:

            # dict.get() returns None if key does not exist
            current_mod_hotkey = profile_json.get('mod_hotkey')

            if current_mod_hotkey:
                key_remaps = []
                for key_remap in profile_json['key_remaps']:
                    src = key_remap.get('src')
                    dst = key_remap.get('dst')
                    if src and dst:
                        key_remaps.append(KeyRemap(src, dst))
                
                if key_remaps:
                    profiles.append(Profile(current_mod_hotkey, key_remaps, False))

            else:
                print(f"\tNo 'mod_hotkey' found in {profile_name}.")


def activate_symbol_layer():
    for key_src, key_dst in key_mappings.items():
        keyboard.remap_key(key_src, key_dst)

def deactivate_symbol_layer():
    for key in key_mappings.keys():
        keyboard.unremap_key(key)

def handle_modifier_key(event):
    if event.event_type == keyboard.KEY_DOWN and keyboard.is_pressed(modifier_key_name):
        activate_symbol_layer()
    elif event.event_type == keyboard.KEY_UP:
        deactivate_symbol_layer() 



read_config(config_file_name, "preset_1")

for profile in profiles:
    print(profile)

# keyboard.hook_key(key, callback, suppress=False):Hooks key up and key down events for a single key
keyboard.hook(handle_modifier_key)

keyboard.wait(quit_command)