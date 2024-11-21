import keyboard
import json

# Todo: garantee profile key names exist, add a cli interface and add option of lock or switch behaviour for every mod_hotkey

# A profile is made up of profile items
# A profile item is made up of mod_hotkey, array of key remap and a boolean is_hotkey_active
# A key remap contains a source key and a destination key

config_file_name = "config.json"
profile_name = "preset_1"
profile_items = []
quit_command = "ctrl+shift+caps lock" # Default

class KeyRemap:
    def __init__(self, key_src, key_dst):
        self.key_src = key_src
        self.key_dst = key_dst
    
    def __repr__(self):
        return f"\n\t(key_src: {self.key_src}, key_dst: {self.key_dst})"        

class ProfileItem:
    def __init__(self, mod_hotkey, key_remaps):
        self.mod_hotkey = mod_hotkey
        self.key_remaps = key_remaps
        self.is_hotkey_active = False

    def __repr__(self):
        return f"mod_key: {self.mod_hotkey }\nkey_remaps: {self.key_remaps}"

def read_config(file_name, profile_name):
    with open(file_name, 'r') as config_file:
        config_json = json.load(config_file)

    for config_key, config_value in config_json.items():
        if config_key == "profiles":
            # reads one profile and its items
            read_config_profile(config_value, profile_name)
        elif config_key == "commands":
            pass

def read_config_profile(config_profiles, profile_name):
        profile = config_profiles[profile_name]
        for profile_item in profile:

            # dict.get() returns None if key does not exist
            current_mod_hotkey = profile_item.get('mod_hotkey')

            if current_mod_hotkey:
                key_remaps = []
                for key_remap in profile_item['key_remaps']:
                    src = key_remap.get('src')
                    dst = key_remap.get('dst')
                    if src and dst:
                        key_remaps.append(KeyRemap(src, dst))
                
                if key_remaps:
                    profile_items.append(ProfileItem(current_mod_hotkey, key_remaps))

            else:
                print(f"\tNo 'mod_hotkey' found in {profile_name}.")


def activate_symbol_layer(key_remaps):
    for key_remap in key_remaps:
        keyboard.remap_key(key_remap.key_src, key_remap.key_dst)

def deactivate_symbol_layer(key_remaps):
    for key_remap in key_remaps:
        keyboard.unremap_key(key_remap.key_src)

def handle_modifier_key(event):
    global profile_items

    for profile_item in profile_items:
        if event.name == profile_item.mod_hotkey:
            if event.event_type == keyboard.KEY_DOWN:
                if not profile_item.is_hotkey_active:
                    profile_item.is_hotkey_active = True
                    activate_symbol_layer(profile_item.key_remaps)
            elif event.event_type == keyboard.KEY_UP:
                if profile_item.is_hotkey_active:
                    profile_item.is_hotkey_active = False
                    deactivate_symbol_layer(profile_item.key_remaps)




# read one profile
read_config(config_file_name, profile_name)

for profile_item in profile_items:
    print(profile_item)


keyboard.hook(handle_modifier_key)

keyboard.wait(quit_command)