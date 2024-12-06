# Layermp
A simple Python tool that uses the [keyboard](https://github.com/boppreh/keyboard/) library to create **key layers**.

## Features
- **Customizable profiles**: Easily create, delete, modify and transition between profiles.
- **Configurable modifier hotkeys:** Define modifier hotkeys to activate key layers based on modes
- **Layer-based key remapping:** Map keys dynamically to different actions using key layers.

## Profile
- Name
- A set of **Key Layers**

### Key Layer
- A modifier hotkey
- The modifier mode:
    - Switch: Temporarily activate a layer by holding the activate hotkey, similar to `Shift`.
    - Lock: Toggle a layer on/off by pressing the activate hotkey, similar to `CapsLock`.
- A set of **Key Remaps**

#### Key Remap
- A source key (the key being remapped).
- A destination key (the key it becomes when the key layer is active).

### Example:

- Let a profile named "Meaningless" contain 1 key layer:
- Key Layer:
    - Modifier hotkey: `CapsLock`
    - Modifier mode: **Switch**
    - Key remaps: 
        - `a` -> `Delete` <br/>
        - `s` -> `F1`
        - `d` -> `up` (up arrow)

While `CapsLock` is **held**, the key layer is active (Switch mode):
```
                     _____  _____  _____ 
                    /\ Del \\  F1 \\  ↑  \ 
                    \ \_____\\_____\\_____\
                     \/_____//_____//_____/
                      /      /      / 
                  ___/_  ___/_  ___/_   
    __________   /\  a  \\  s  \\  d  \     
   \  CapsLock \ \ \_____\\_____\\_____\    
    \___________\ \/_____//_____//_____/  
```

## Usage

### Requirements 
- Python 3.12+ needed ([Download Page](https://www.python.org/downloads/))
- Keyboard library needed ([GitHub Repository](https://github.com/boppreh/keyboard/?tab=readme-ov-file#usage))
- Pydantic library needed ([Install Page](https://docs.pydantic.dev/latest/install/))


**Note:** Currently, Layermp can only be used if you manually modify the json files in the config folder.

### Steps
1. Clone or download the repository:
```bash
git clone https://github.com/figdavi/Layermp.git
cd layermp
```

2. Run the program:
```bash
python main.py
```

## Future Improvements
- Add a CLI with [Typer](https://github.com/fastapi/typer) + [Rich](https://github.com/Textualize/rich)
- Design a way to check if key names exist as keys (keyboard library doesn't have a support to this by default)
- Error logging
- Implement better printing format for profile and commands classes
- Review exceptions and returning values
- Review docstrings (simplify)
- Create a pt-br README

## Related Articles
For an in-depth understanding of key layers, refer to:
- [Extend layers by Dreymar](https://dreymar.colemak.org/layers-extend.html)
- [Designing a Symbol Layer by Pascal Getreuer](https://getreuer.info/posts/keyboards/symbol-layer/index.html)