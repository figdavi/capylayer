import keyboard as kb
from models import KeyLayer, SWITCH_MODE_NAME, LOCK_MODE_NAME

def set_key_layer_state(key_layer: KeyLayer, activate: bool) -> None:
    """   
    Map/unmap individual keys that form a key layer.
    """
    key_layer.is_active = activate
    print(activate)

    for key_src, key_dst in key_layer.key_remaps.items():
        if activate:
            kb.remap_key(key_src, key_dst)
        else:
            kb.unremap_key(key_src) # type: ignore

def handle_modifier_lock(key_layer: KeyLayer) -> None:
    """   
    Activates/deactivates key layer based on modifier hotkey lock mode
    """

    if all(key_layer.mod_hotkey_dict.values()):
        set_key_layer_state(key_layer, not key_layer.is_active)
        for key in key_layer.mod_hotkey_dict.keys():
            key_layer.mod_hotkey_dict[key] = False

def handle_modifier_switch(key_layer: KeyLayer) -> None: 
    """   
    Activates/deactivates key layer based on modifier hotkey switch mode.
    """
    if all(key_layer.mod_hotkey_dict.values()):
        if not key_layer.is_active:
            set_key_layer_state(key_layer, True)
    else:
        if key_layer.is_active:
            set_key_layer_state(key_layer, False)

def handle_mod_mode(key_layer: KeyLayer) -> None:
    """   
    Calls corresponding handler modifier function based on modifier hotkey mode.
    """    
    if key_layer.mod_mode == SWITCH_MODE_NAME:
        handle_modifier_switch(key_layer)   
    elif key_layer.mod_mode == LOCK_MODE_NAME:
        handle_modifier_lock(key_layer)

def handle_mod_hotkey(event: kb.KeyboardEvent, key_layers: list[KeyLayer]) -> None:
    """   
    Handle key events to track press and release of keys that make up the modifier hotkey.
    """

    # bool on key_layer.mode_hotkey_dict is used differently depending on key_layer.mod_mode

    for key_layer in key_layers:
        if event.scan_code in key_layer.mod_hotkey_dict:
            key_layer.mod_hotkey_dict[event.scan_code] = (event.event_type == kb.KEY_DOWN)
            handle_mod_mode(key_layer)    