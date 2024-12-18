# capylayer
A simple Python tool to create **key layers** activated by modifier hotkeys.

Capylayer allows you to remap specified keys to build layers for your keyboard. Layers are activated by modifier hotkeys and are contained in profiles. You can build layouts like QWERTY, Colemak, Dvorak, a symbol layer, or any other useful remapping.

## Modifier mode
A modifier hotkey can be set to one of two modes:
- **Switch**: Temporarily activate a layer by *holding* the modifier hotkey, similar to Shift.
- **Lock**: Toggle a layer on/off by *pressing* the modifier hotkey, similar to CapsLock.

## Example

**Profile:** "capy"
- **Key Layer:**
    - **Modifier hotkey**: `CapsLock`  
    - **Modifier mode**: Switch  
    - **Key remaps**:
        - `a` → `delete`
        - `s` → `f1`
        - `d` → `up`

While `CapsLock` is **held**, the key layer is active:
```
                     _____  _____  _____ 
                    /\ del \\  f1 \\  ↑  \ 
                    \ \_____\\_____\\_____\
                     \/_____//_____//_____/
                      /      /      / 
                  ___/_  ___/_  ___/_   
    __________   /\  a  \\  s  \\  d  \     
   \  CapsLock \ \ \_____\\_____\\_____\    
    \___________\ \/_____//_____//_____/  
```

## Installation

- Python 3.12+ needed ([Download Page](https://www.python.org/downloads/))

1. Install via pip:
```bash
pip install git+https://github.com/figdavi/capylayer.git
```

## Usage
1. Add profiles in capylayer/models/config/profiles.json

2. Then run:
```bash
capylayer
```

## Future Improvements
- Add a TUI with [Textual](https://github.com/Textualize/textual)
- Design a way to check if key names exist as keys
- Error logging
- Implement support for key to symbol remapping
- Create a pt-br README