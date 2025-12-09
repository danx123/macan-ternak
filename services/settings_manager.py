"""
Settings manager for game configuration
"""
import json
from pathlib import Path

class SettingsManager:
    """Manages game settings and preferences"""
    
    def __init__(self):
        self.settings_dir = Path.home() / '.macan_ternak'
        self.settings_file = self.settings_dir / 'settings.json'
        
        # Default settings
        self.defaults = {
            'sound_enabled': True,
            'music_volume': 0.7,
            'sfx_volume': 0.8,
            'auto_save': True,
            'auto_save_interval': 30,
            'graphics_quality': 'medium',
            'fullscreen': False,
            'language': 'en'
        }
        
        self.settings = self.defaults.copy()
        self.load_settings()
        
    def load_settings(self):
        """Load settings from file"""
        if not self.settings_file.exists():
            self.save_settings()
            return
            
        try:
            with open(self.settings_file, 'r') as f:
                loaded = json.load(f)
                self.settings.update(loaded)
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def save_settings(self):
        """Save settings to file"""
        try:
            self.settings_dir.mkdir(exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
        
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
        
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.defaults.copy()
        self.save_settings()