import json

with open('profiles.json', 'r+') as file:
    data = json.load(file)

class KeyRemap:
    def __init__(self, key_src, key_dst):
        self.key_src = key_src
        self.key_dst = key_dst
    
    def __repr__(self):
        return f"\n\t(key_src: {self.key_src}, key_dst: {self.key_dst})"        

class Profile:
    def __init__(self, mod_hotkey, key_remaps):
        self.mod_hotkey = mod_hotkey
        self.key_remaps = key_remaps

    def __repr__(self):
        return f"mod_key: {self.mod_hotkey }\nkey_remaps: {self.key_remaps}"
        

profiles = []

# (key, value) in data
for profile_group_json, profiles_json in data['profiles'].items():
    for profile_json in profiles_json:

        # dict.get() returns None if key does not exist
        current_mod_hotkey = profile_json.get('mod_hotkey')

        if current_mod_hotkey:
            key_remaps = []
            for key_remap in profile_json['key_remaps']:
                src = key_remap.get('src')
                dst = key_remap.get('dst')
                if src and dst:
                    key_remaps.append(KeyRemap(src, dst))
            
            if key_remaps:
                profiles.append(Profile(current_mod_hotkey, key_remaps))

        else:
            print(f"\tNo 'mod_hotkey' found in {profile_group}.")

for profile in profiles:
    print(profile)

        