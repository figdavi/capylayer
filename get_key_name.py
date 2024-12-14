import keyboard as kb

def get_key_name(event):
    print(f"key name: {event.name}\tkey scan code: {event.scan_code}")

kb.hook(get_key_name)

kb.wait()