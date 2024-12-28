from .models import Profile, KeyLayer, ModModeEnum
import keyboard as kb

def start_key_handler(profile: Profile):
    kb.hook(lambda event:_handle_mod_hotkey(event, profile.key_layers))
    return True

def _set_key_layer_state(layer: KeyLayer, activate: bool) -> None:
    """   
    Map/unmap individual keys that form a key layer.
    """
    layer.is_active = activate

    if activate:
        for key_src, key_dst in layer.key_remaps.items():
            kb.remap_key(key_src, key_dst)
    else:
        for key_src in layer.key_remaps:
            kb.unremap_key(key_src) # type: ignore

def _handle_mod_mode(layer: KeyLayer) -> None:
    """   
    Activate/Deactivate key layer based on modifier hotkey mode.
    """    
    if layer.mod_mode == ModModeEnum.switch:
        if all(layer.mod_hotkey_dict.values()):
            if not layer.is_active:
                _set_key_layer_state(layer, True)
        else:
            if layer.is_active:
                _set_key_layer_state(layer, False)  

    elif layer.mod_mode == ModModeEnum.lock:
        if all(layer.mod_hotkey_dict.values()):
            _set_key_layer_state(layer, not layer.is_active)
            for key in layer.mod_hotkey_dict:
                layer.mod_hotkey_dict[key] = False

def _handle_mod_hotkey(event: kb.KeyboardEvent, key_layers: list[KeyLayer]) -> None:
    """   
    Handle key events to track press and release of keys that make up the modifier hotkey.
    """
    # bool on layer.mode_hotkey_dict is used differently depending on layer.mod_mode
    for layer in key_layers:
        if event.name not in layer.mod_hotkey_dict:
            continue
        
        is_down_press = (event.event_type == kb.KEY_DOWN)
        if layer.mod_hotkey_dict[event.name] == is_down_press:
            return None
        
        layer.mod_hotkey_dict[event.name] = is_down_press
        _handle_mod_mode(layer)