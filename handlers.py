# File containing key handling and key remapping functions (imported in main.py)
import keyboard
from config.config_class import KeyLayersItem, KeyRemapsItem

def set_key_layer_state(key_remaps: list[KeyRemapsItem], activate: bool) -> None:
    # Map/unmap key layer depending on activate value

    for key_remap in key_remaps:
        if not key_remap.key_src or not key_remap.key_dst:
            print(f"Error: Missing source key or destination key in remap: {key_remap}")
            continue

        if activate:
            keyboard.remap_key(key_remap.key_src, key_remap.key_dst)
        else:
            keyboard.unremap_key(key_remap.key_src)

def handle_modifier_lock(key_layer: KeyLayersItem) -> None:   
    # Calls set_key_layer_state() based on lock mode logic

    if all(key_layer.mod_hotkey.values()):
        key_layer.is_active = not key_layer.is_active
        set_key_layer_state(key_layer.key_remaps, key_layer.is_active)

        for key in key_layer.mod_hotkey.keys():
            key_layer.mod_hotkey[key] = False

def handle_modifier_switch(key_layer: KeyLayersItem) -> None:   
    # Calls set_key_layer_state() based on switch mode logic

    if all(key_layer.mod_hotkey.values()):
        if not key_layer.is_active:
            key_layer.is_active = True
            set_key_layer_state(key_layer.key_remaps, key_layer.is_active)
    else:
        if key_layer.is_active:
            key_layer.is_active = False
            set_key_layer_state(key_layer.key_remaps, key_layer.is_active)

def handle_mod_mode(key_layer: KeyLayersItem) -> None:   
    # Calls corresponding handle function based on modifier hotkey mode

    if key_layer.mod_mode == "switch":
        handle_modifier_switch(key_layer)   
    elif key_layer.mod_mode == "lock":
        handle_modifier_lock(key_layer)
    else:   
        print(f"Error: hotkey {key_layer.mod_hotkey} has unknown modifier hotkey mode: {key_layer.mod_mode}")
        return None

def handle_mod_hotkey(event: keyboard.KeyboardEvent, key_layers: list[KeyLayersItem]) -> None:
    # Handle key events to track press and release of keys of modifier hotkey

    for key_layer in key_layers:
        if event.name in key_layer.mod_hotkey:
            key_layer.mod_hotkey[event.name] = (event.event_type == keyboard.KEY_DOWN)
            handle_mod_mode(key_layer)
            