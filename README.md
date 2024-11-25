# Layermp
A simple Python tool that uses the [keyboard](https://github.com/boppreh/keyboard/) library to create **key layers**.

## Features
- **Configurable modifier hotkeys:** Define modifier hotkeys to activate key layers based on [modes](#modifier-hotkey-modes).
- **Layer-based key remapping:** Map keys dynamically to different actions using key layers.
- **Customizable profiles**: Easily create, delete, modify and transition between profiles.

## Modifier Hotkey Modes:
1. **Switch**:
Temporarily activate a layer by holding the modifier hotkey, similar to `Shift`.
2. **Lock**:
Toggle a layer on/off by pressing the modifier hotkey, similar to `CapsLock`.

## Profiles structure 

A **Profile** contains:
- Name
- A set of **mappings**

Each **Mapping** contains:
- A **modifier hotkey**
- The modifier's hotkey [**mode**](#modifier-hotkey-modes)
- A set of **key remaps**

Each **Key remap** consists of:
- A **source key** (the key being remapped).
- A **destination key** (the key it becomes when the key layer is active).

### Example:

```
- Let a profile named "Meaningless" contain 1 mapping:
- Mapping:
    - Modifier hotkey: `CapsLock`
    - Modifier hotkey mode: Switch
    - Key remaps: 'a' -> 'delete'
                  's' -> 'f1'
                  'd' -> '?'

While `CapsLock` is held, the key layer is active (Switch mode):
                     _____  _____  _____ 
                    /\ del \\  f1 \\  ?  \ 
                    \ \_____\\_____\\_____\
                     \/_____//_____//_____/
                      /      /      / 
                  ___/_  ___/_  ___/_   
    __________   /\  a  \\  s  \\  d  \     
   \  CapsLock \ \ \_____\\_____\\_____\    
    \ __________\ \/_____//_____//_____/  
```

## Usage

**Note:** 
- Python 3.12+ needed ([install page](https://www.python.org/downloads/))
- Keyboard library needed ([install page](https://github.com/boppreh/keyboard/?tab=readme-ov-file#usage))


Currently, Layermp can only be used if you manually modify the json files in the config folder and then run (in the main.py folder):
```
python main.py
```

## Future Improvements
- Add a CLI with [Typer](https://github.com/fastapi/typer) + [Rich](https://github.com/Textualize/rich)
- Design a way to check if key names exist as keys (keyboard library doesn't have a support to this by default)
- Implement better error handling
- Create a pt-br README

## References
For an in-depth understanding of key layers, refer to:
- [Extend layers by Dreymar](https://dreymar.colemak.org/layers-extend.html)
- [Designing a Symbol Layer by Pascal Getreuer](https://getreuer.info/posts/keyboards/symbol-layer/index.html)