import keyboard
from config.config_class import KeyLayersItem, KeyRemapsItem, SWITCH_MODE_NAME, LOCK_MODE_NAME

def set_key_layer_state(key_remaps: list[KeyRemapsItem], activate: bool) -> None:
    # Map/unmap key layer depending on activate value

    for key_remap in key_remaps:
        if activate:
            keyboard.remap_key(key_remap.key_src, key_remap.key_dst)
        else:
            keyboard.unremap_key(key_remap.key_src)

def handle_modifier_lock(key_layer: KeyLayersItem) -> None:   
    # Calls set_key_layer_state() based on lock mode logic

    # Checks a dictionary "mod_hotkey": key, unused press 
    # All presses are "used" when a key layer activates and restored on key release
    if all(key_layer.mod_hotkey.values()):
        key_layer.is_active = not key_layer.is_active
        set_key_layer_state(key_layer.key_remaps, key_layer.is_active)

        for key in key_layer.mod_hotkey.keys():
            key_layer.mod_hotkey[key] = False

def handle_modifier_switch(key_layer: KeyLayersItem) -> None:   
    # Calls set_key_layer_state() based on switch mode logic

    # Checks a dictionary "mod_hotkey": key, being pressed
    # Layer activates when all keys are being pressed
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

    if key_layer.mod_mode == SWITCH_MODE_NAME:
        handle_modifier_switch(key_layer)   
    elif key_layer.mod_mode == LOCK_MODE_NAME:
        handle_modifier_lock(key_layer)

def handle_mod_hotkey(event: keyboard.KeyboardEvent, key_layers: list[KeyLayersItem]) -> None:
    # Handle key events to track press and release of keys of modifier hotkey

    for key_layer in key_layers:
        if event.name in key_layer.mod_hotkey:
            key_layer.mod_hotkey[event.name] = (event.event_type == keyboard.KEY_DOWN)
            handle_mod_mode(key_layer)
            