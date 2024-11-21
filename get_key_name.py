import keyboard

quit_command = "esc"

def print_key_name(event):
    print(event.name)

keyboard.hook(print_key_name)

print(f"Press \'{quit_command}\' to exit")
keyboard.wait(quit_command)