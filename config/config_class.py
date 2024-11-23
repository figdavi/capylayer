# File contaning profiles and commands classes (imported in utils.py)

# For better understanding, see profiles.json and commands.json files
# These classes and its methods are made to read and store them

class KeyRemapsItem:
    def __init__(self, key_src, key_dst):
        self.key_src = key_src
        self.key_dst = key_dst
    
    # Returns a list of KeyRemapsItem containing key source and key destination
    @staticmethod
    def from_json(key_remaps_json):
        return [
            KeyRemapsItem(
                key_remap.get("key_src", ""), 
                key_remap.get("key_dst", "")
            )
            for key_remap in key_remaps_json
        ]

    def __repr__(self):
        return f"\n\t(Key source: {self.key_src}, Key destination: {self.key_dst})"   
    
class MappingsItem:
    def __init__(self, mod_hotkey, mod_hotkey_mode, key_remaps):
        self.mod_hotkey = mod_hotkey
        self.mod_hotkey_mode = mod_hotkey_mode
        self.key_remaps = key_remaps
        self.is_active = False 

    # Returns a list of MappingsItem containing a modifier hotkey, modifier hotkey mode (switch or lock) and a list of KeyRemapsItem
    @staticmethod
    def from_json(mappings_json):
        return [
             MappingsItem(
                mod_hotkey = mapping.get("mod_hotkey", ""),
                mod_hotkey_mode = mapping.get("mod_hotkey_mode", ""),
                key_remaps = KeyRemapsItem.from_json(mapping["key_remaps"])
            )
            for mapping in mappings_json
        ]
       
        
    def __repr__(self):
        return f"Modifier hotkey: {self.mod_hotkey}\nModifier hotkey mode: {self.mod_hotkey_mode}\nKey remaps: {self.key_remaps}"    

class Profile:
    def __init__(self, name, mappings):
        self.name = name
        self.mappings = mappings

    def __repr__(self):
        return f"Profile name: {self.name}\nMappings: {self.mappings}"
    
    # Returns an instance of Profile class contaning the profile name and a list of MappingsItem
    @staticmethod
    def from_json(profile_json):
        return Profile(
            profile_json.get("name", ""), 
            MappingsItem.from_json(profile_json["mappings"])
        )

class CommandsItem:
    def __init__(self, hotkey):
        self.hotkey = hotkey

    # Returns a **dictionary** where key = command name : value = instance of CommandsItem class
    @staticmethod
    def from_json(commands_json):
        return {
            command.get("name"): CommandsItem(
                command.get("hotkey")
            )
            for command in commands_json["commands"].values()
        }