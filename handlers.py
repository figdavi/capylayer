# File containing key handling and key remapping functions (imported in main.py)
import keyboard

# Map/unmap key layer depending on activate value
def set_key_layer_state(key_remaps, activate):
    for key_remap in key_remaps:
        if activate:
            keyboard.remap_key(key_remap.key_src, key_remap.key_dst)
        else:
            keyboard.unremap_key(key_remap.key_src)

# Call set_key_layer_state() if mod_hotkey pressed, based on lock mode logic
def handle_modifier_lock(event, mapping):
    if event.event_type == keyboard.KEY_DOWN:
        mapping.is_active = not mapping.is_active
        set_key_layer_state(mapping.key_remaps, mapping.is_active)

# Call set_key_layer_state() if mod_hotkey pressed, based on switch mode logic
def handle_modifier_switch(event, mapping):
    if event.event_type == keyboard.KEY_DOWN:
        if not mapping.is_active:
            mapping.is_active = True
            set_key_layer_state(mapping.key_remaps, mapping.is_active)
    elif event.event_type == keyboard.KEY_UP:
        if mapping.is_active:
            mapping.is_active = False
            set_key_layer_state(mapping.key_remaps, mapping.is_active)

# Call corresponding handle function based on modifier hotkey mode
def handle_modifier_key(event, profile):
    for mapping in profile.mappings:
        if event.name == mapping.mod_hotkey:
            if mapping.mod_hotkey_mode == "switch":
                handle_modifier_switch(event, mapping)
            elif mapping.mod_hotkey_mode == "lock":
                handle_modifier_lock(event, mapping)