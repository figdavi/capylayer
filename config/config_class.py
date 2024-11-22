class KeyRemapsItem:
    def __init__(self, key_src, key_dst):
        self.key_src = key_src
        self.key_dst = key_dst
    
    def __repr__(self):
        return f"\n\t(Key source: {self.key_src}, Key destination: {self.key_dst})"   
    
class MappingsItem:
    def __init__(self, mod_hotkey, mod_type, key_remaps):
        self.mod_hotkey = mod_hotkey
        self.mod_type = mod_type
        self.key_remaps = key_remaps
        self.is_active = False 
        
    def __repr__(self):
        return f"Modifier hotkey: {self.mod_hotkey}\nModifier type: {self.mod_type}\nKey remaps: {self.key_remaps}"    

class Profile:
    def __init__(self, name, mappings):
        self.name = name
        self.mappings = mappings

    def __repr__(self):
        return f"Profile name: {self.name}\nMappings: {self.mappings}"

class CommandsItem:
    def __init__(self, hotkey):
        self.hotkey = hotkey