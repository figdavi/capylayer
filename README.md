# capylayer
A simple python package to create **key layers** activated by modifier hotkeys.

Layers are activated by defined hotkeys. You can build remappings for symbol layers, layouts like Dvorak, or any other customized layer.

## Platform support
### Windows
On windows, an AHK script is used to simulate key remapping. Use AHK [key name syntax](https://documentation.help/AutoHotkey-en/KeyList.htm#keyboard) for it to work.

### Other platforms
On Linux and MacOS, for now, [keyboard](https://github.com/boppreh/keyboard/) library is used to simulate the key remapping action, unfortunately it does not work as intended/fully for a range of keys. For example, modifier keys like `Alt` when remapped by other keys will not fully work (E.g. `Alt` + `F4` won't work).

## Modifier mode
A modifier hotkey can be set to one of two modes:
- **Switch**: Activate a layer by *holding*, similar to Shift.
- **Lock**: Toggle a layer on/off by *pressing*, similar to CapsLock.

## Example

**Profile:** "capy"
- **Key Layer:**
    - **Modifier hotkey**: `CapsLock`  
    - **Modifier mode**: Switch  
    - **Key remaps**:
        - `a` → `Delete`
        - `s` → `F1`
        - `d` → `Up`

While `CapsLock` is **held**, the key layer is active:
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

## Installation

- Python 3.12+ needed ([Download Page](https://www.python.org/downloads/))

- Install via pip:
```bash
pip install capylayer
```

## Usage
1. Add profiles in capylayer/modules/data/profiles (TUI is not implemented currently)

2. Then run:
```bash
capylayer
```

## Future Improvements
- Add a TUI with [Textual](https://github.com/Textualize/textual)
- Design a way to check if key names exist as keys
- Error logging
- Key -> Hotkey remapping
- Implement better key remapping for Linux and MacOS
- Compile script dynamically
- Create a pt-br README
- Implement a dead key behaviour for accents
- Add dist files to repo