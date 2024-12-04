import keyboard
from models.profiles import KeyLayersItem, SWITCH_MODE_NAME, LOCK_MODE_NAME

def set_key_layer_state(key_layer: KeyLayersItem, activate: bool) -> None:
    """   
    Map/unmap individual keys that form a key layer

    Args: 
        key_layer (KeyLayersItem): an istance of KeyLayersItem
        activate (bool): a boolean indicating whether of not to activate the layer
    Returns: 
        None
    """
    key_layer.is_active = activate

    for key_remap in key_layer.key_remaps:
        if activate:
            keyboard.remap_key(key_remap.key_src, key_remap.key_dst)
        else:
            keyboard.unremap_key(key_remap.key_src)

def handle_modifier_lock(key_layer: KeyLayersItem) -> None:
    """   
    Activates key layer through set_key_layer_state() based on modifier hotkey lock mode

    Args: 
        key_layer (KeyLayersItem): an istance of KeyLayersItem
    Returns: 
        None
    """
    if all(key_layer.mod_hotkey_dict.values()):
        set_key_layer_state(key_layer.key_remaps, not key_layer.is_active)

        for key in key_layer.mod_hotkey_dict.keys():
            key_layer.mod_hotkey_dict[key] = False

def handle_modifier_switch(key_layer: KeyLayersItem) -> None: 
    """   
    Activates key layer through set_key_layer_state() based on modifier hotkey switch mode

    Args: 
        key_layer (KeyLayersItem): an istance of KeyLayersItem
    Returns: 
        None
    """
    if all(key_layer.mod_hotkey_dict.values()):
        if not key_layer.is_active:
            set_key_layer_state(key_layer.key_remaps, True)
    else:
        if key_layer.is_active:
            set_key_layer_state(key_layer.key_remaps, False)

def handle_mod_mode(key_layer: KeyLayersItem) -> None:
    """   
    Calls corresponding handle_modifier function based on modifier hotkey mode

    Args: 
        key_layer (KeyLayersItem): an istance of KeyLayersItem
    Returns: 
        None
    """    
    if key_layer.mod_mode == SWITCH_MODE_NAME:
        handle_modifier_switch(key_layer)   
    elif key_layer.mod_mode == LOCK_MODE_NAME:
        handle_modifier_lock(key_layer)

def handle_mod_hotkey(event: keyboard.KeyboardEvent, key_layers: list[KeyLayersItem]) -> None:
    """   
    Handle key events to track press and release of keys the compose modifier hotkey

    Args: 
        key_layer (KeyLayersItem): an istance of KeyLayersItem
    Returns: 
        None
    """ 
    for key_layer in key_layers:
        if event.name in key_layer.mod_hotkey_dict:
            key_layer.mod_hotkey_dict[event.name] = (event.event_type == keyboard.KEY_DOWN)
            handle_mod_mode(key_layer)
            