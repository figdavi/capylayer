import keyboard

def get_key_name(event):
    print(event.name)

keyboard.hook(get_key_name)

keyboard.wait()