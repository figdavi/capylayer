import keyboard
import json

from config.config_class import Profile, KeyRemapsItem, MappingsItem, CommandsItem

# Todo: garantee profile key names exist, add a cli, add option of lock or switch behaviour for every mod_hotkey
# cli should have options to add, remove, switch profile, view current profile, change mod_hotkey, change remappings,
# if possible add profiles without hotkeys, only remappings

# A profile is made up of profile items
# A profile item is made up of mod_hotkey, array of key remap and a boolean is_hotkey_active
# A key remap contains a source key and a destination key

config_path = "./config/"
profiles_path = config_path + "profiles.json"
commands_path = config_path + "commands.json"

def get_active_profile(profiles_json):
    active_profile_name = profiles_json["active_profile"]
    for profile in profiles_json["profiles"]:
        if profile["name"] == active_profile_name:
            return profile

def read_config_profile(profiles_path):
    with open(profiles_path, 'r') as profiles_file:
        profiles_json = json.load(profiles_file)
    
    active_profile = get_active_profile(profiles_json)
    key_remaps = []
    mappings = []
    profile_name = active_profile.get("name")

    for mapping in active_profile["mappings"]:
        mod_hotkey = mapping.get("mod_hotkey")
        mod_type = mapping.get("mod_type")

        for key_remap in mapping["key_remaps"]:
            src = key_remap.get("key_src")
            dst = key_remap.get("key_dst")

            key_remaps.append(KeyRemapsItem(src, dst))
        
        mappings.append(MappingsItem(mod_hotkey, mod_type, key_remaps))

    profile = Profile(profile_name, mappings)

    return profile
            

def read_config_commands(commands_path):
    with open(commands_path, 'r') as commands_file:
        commands_json = json.load(commands_file)

    commands = {}

    for command in commands_json["commands"]:
        name = command.get("name")
        hotkey = command.get("hotkey")
        description = command.get("description")

        commands[name] = CommandsItem(hotkey, description)
    
    return commands

def activate_symbol_layer(key_remaps):
    for key_remap in key_remaps:
        keyboard.remap_key(key_remap.key_src, key_remap.key_dst)

def deactivate_symbol_layer(key_remaps):
    for key_remap in key_remaps:
        keyboard.unremap_key(key_remap.key_src)

def handle_modifier_key(event):
    global profile

    for mapping in profile.mappings:
        if event.name == mapping.mod_hotkey:
            if event.event_type == keyboard.KEY_DOWN:
                if not mapping.is_active:
                    mapping.is_active = True
                    activate_symbol_layer(mapping.key_remaps)
            elif event.event_type == keyboard.KEY_UP:
                if mapping.is_active:
                    mapping.is_active = False
                    deactivate_symbol_layer(mapping.key_remaps)



profile = read_config_profile(profiles_path)
commands = read_config_commands(commands_path)

keyboard.hook(handle_modifier_key)
keyboard.wait(commands["quit"].hotkey) 