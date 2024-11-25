# File containing key handling and key remapping functions (imported in main.py)
# Classes KeyRemapsItem, MappingsItem and Profile are from config/config_class.py
import keyboard
from config.config_class import Profile, MappingsItem, KeyRemapsItem


def set_key_layer_state(key_remaps: list["KeyRemapsItem"], activate: bool) -> None:
    # Map/unmap key layer depending on activate value

    for key_remap in key_remaps:
        if not key_remap.key_src or not key_remap.key_dst:
            print(f"Error: Missing source key or destination key in remap: {key_remap}")
            # Since we do not want to map a key pair without a source or destination
            continue

        if activate:
            keyboard.remap_key(key_remap.key_src, key_remap.key_dst)
        else:
            keyboard.unremap_key(key_remap.key_src)

def handle_modifier_lock(event: keyboard.KeyboardEvent, mapping: "MappingsItem") -> None:   
    # Calls set_key_layer_state() based on lock mode logic

    if event.event_type == keyboard.KEY_DOWN:
        mapping.is_active = not mapping.is_active
        set_key_layer_state(mapping.key_remaps, mapping.is_active)

def handle_modifier_switch(event: keyboard.KeyboardEvent, mapping: "MappingsItem") -> None:   
    # Calls set_key_layer_state() based on switch mode logic

    if event.event_type == keyboard.KEY_DOWN and not mapping.is_active:
            mapping.is_active = True
            set_key_layer_state(mapping.key_remaps, mapping.is_active)
    elif event.event_type == keyboard.KEY_UP and mapping.is_active:
            mapping.is_active = False
            set_key_layer_state(mapping.key_remaps, mapping.is_active)

def handle_modifier_key(event: keyboard.KeyboardEvent, profile: "Profile") -> None:   
    # Calls corresponding handle function based on modifier hotkey mode

    for mapping in profile.mappings:
        if event.name == mapping.mod_hotkey:
            if mapping.mod_hotkey_mode == "switch":
                handle_modifier_switch(event, mapping)
            elif mapping.mod_hotkey_mode == "lock":
                handle_modifier_lock(event, mapping)
            else:
                print(f"Error: hotkey {mapping.mod_hotkey} has unknown modifier hotkey mode: {mapping.mod_hotkey_mode}")
                return None