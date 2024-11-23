import keyboard

def activate_symbol_layer(key_remaps):
    for key_remap in key_remaps:
        keyboard.remap_key(key_remap.key_src, key_remap.key_dst)

def deactivate_symbol_layer(key_remaps):
    for key_remap in key_remaps:
        keyboard.unremap_key(key_remap.key_src)

def handle_modifier_lock(event, mapping):
    if event.event_type == keyboard.KEY_DOWN:
        if not mapping.is_active:
            activate_symbol_layer(mapping.key_remaps)
            mapping.is_active = True
        else:
            deactivate_symbol_layer(mapping.key_remaps) 
            mapping.is_active = False


def handle_modifier_switch(event, mapping):
    if event.event_type == keyboard.KEY_DOWN:
        if not mapping.is_active:
            mapping.is_active = True
            activate_symbol_layer(mapping.key_remaps)
    elif event.event_type == keyboard.KEY_UP:
        if mapping.is_active:
            mapping.is_active = False
            deactivate_symbol_layer(mapping.key_remaps)

def handle_modifier_key(event, profile):
    for mapping in profile.mappings:
        if event.name == mapping.mod_hotkey:
            if mapping.mod_type == "switch":
                handle_modifier_switch(event, mapping)
            elif mapping.mod_type == "lock":
                handle_modifier_lock(event, mapping)