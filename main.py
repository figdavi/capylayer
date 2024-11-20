import keyboard


key_mappings = {
    'w': 'up',
    'a': 'left',
    's': 'down',
    'd': 'right'
}

modifier_key_name = 'caps lock'
quit_command = 'ctrl+shift+' + modifier_key_name


def activate_symbol_layer():
    for key_src, key_dst in key_mappings.items():
        keyboard.remap_key(key_src, key_dst)

def deactivate_symbol_layer():
    for key in key_mappings.keys():
        keyboard.unremap_key(key)

def handle_modifier_key(event):
    if event.event_type == keyboard.KEY_DOWN and keyboard.is_pressed(modifier_key_name):
        activate_symbol_layer()
    elif event.event_type == keyboard.KEY_UP:
        deactivate_symbol_layer() 
        

keyboard.hook_key(modifier_key_name, handle_modifier_key)
keyboard.wait(quit_command)