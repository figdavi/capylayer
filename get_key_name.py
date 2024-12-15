import keyboard as kb

def get_key_name(event):
    print(f"key name: {event.name}\tkey scan code: {kb.key_to_scan_codes(event.name)}")

kb.hook(get_key_name)

kb.wait()