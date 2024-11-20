import keyboard
from win32api import GetKeyState
from win32con import VK_CAPITAL

# Variables containing '_was_'/'_last_' store the key value
#  assigned *last time* its state was checked, so it is the contrary
#  of current's state.


symbol_layer_active = None
caps_lock_pressed = None
quit_command = 'ctrl+shift+caps lock'
caps_lock_key_name = 'caps lock'


def activate_symbol_layer():
    keyboard.remap_key('w', 'up')
    keyboard.remap_key('a', 'left')
    keyboard.remap_key('s', 'down')
    keyboard.remap_key('d', 'right')

def deactivate_symbol_layer():
    keyboard.unremap_key('w')
    keyboard.unremap_key('a')
    keyboard.unremap_key('s')
    keyboard.unremap_key('d')

def handle_caps_lock(event):
    global symbol_layer_active
    global caps_lock_pressed

    if event.event_type == keyboard.KEY_DOWN and not caps_lock_pressed:
        caps_lock_pressed = True

        if not symbol_layer_active:
            activate_symbol_layer()
            symbol_layer_active = True
        else:
            deactivate_symbol_layer() 
            symbol_layer_active = False

    elif event.event_type == keyboard.KEY_UP:
        caps_lock_pressed = False 

def onload():
    global symbol_layer_active
    global caps_lock_pressed

    symbol_layer_active = bool(GetKeyState(VK_CAPITAL))
    caps_lock_pressed = False

    if symbol_layer_active:
        activate_symbol_layer()


onload()

keyboard.hook_key(caps_lock_key_name, handle_caps_lock)
keyboard.wait(quit_command)