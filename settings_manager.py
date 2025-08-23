import json
import os

class SettingsManager:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "screen_width": 1440,
            "screen_height": 1080,
            "fullscreen": False,
            "volume": 0.7,
            "sound_enabled": True
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    for key in self.default_settings:
                        if key not in loaded_settings:
                            loaded_settings[key] = self.default_settings[key]
                    return loaded_settings
        except Exception as e:
            print(f"설정 파일 로드 오류: {e}")
        
        return self.default_settings.copy()
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"설정 파일 저장 오류: {e}")
    
    def get_setting(self, key):
        return self.settings.get(key, self.default_settings.get(key))
    
    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()
    
    def get_screen_size(self):
        return (self.get_setting("screen_width"), self.get_setting("screen_height"))
    
    def get_volume(self):
        return self.get_setting("volume")
    
    def is_sound_enabled(self):
        return self.get_setting("sound_enabled")
    
    def is_fullscreen(self):
        return self.get_setting("fullscreen")