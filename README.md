# Layermp
A simple Python tool using [keyboard](https://github.com/boppreh/keyboard/) library to create **key layers**.

## Features
- **Configurable modifier hotkeys:** Define modifier hotkeys to activate key layers based on [modes](#modifier-hotkey-modes).
- **Layer-based key remapping:** Map keys dynamically to different actions using key layers.
- **Customizable profiles**: Easily add, remove, edit and switch between profiles.

## Modifier Hotkey Modes:
1. **Switch**:
Temporarily activate a layer by holding the modifier hotkey, similar to `Shift`.
2. **Lock**:
Toggle a layer on/off by pressing the modifier hotkey, similar to `CapsLock`.

## Profiles       
Each profile contains:
- Multiple **mappings**
### Mappings
Each mapping contains:
- A **modifier hotkey**
- A set of **key remaps**
### Key remap
A key remap consists of:
- A **source key** (the key being remapped).
- A **destination key** (the key it becomes when the key layer is active).

#### Example:
- Let a profile have 1 mapping:
- Let the Mapping be:
    - Modifier hotkey ([shift](#modifier-hotkey-modes) mode): `Shift`
    - Key remaps: `a` -> `delete`
                  `s` -> `f1`
                  `d` -> `?`

While `Shift` is pressed, the key layer is active:
                     ______ ______ ______  
                    /\ del \\  f1 \\  ?  \ 
                    \ \_____\\_____\\_____\
                     \/_____//_____//_____/
                      /      /      / 
                  ___/___ __/__ ___/__    
   ___________   /\  a  \\  s  \\  d  \     
   \   Shift   \ \ \_____\\_____\\_____\    
    \___________\ \/_____//_____//_____/  

## References
For an in-depth understanding of key layers, refer to:
- [Extend layers by Dreymar](https://dreymar.colemak.org/layers-extend.html)
- [Desingning a Symbol Layer by Pascal Getreuer](https://getreuer.info/posts/keyboards/symbol-layer/index.html)