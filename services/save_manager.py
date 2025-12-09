"""
Save and load game data using JSON
"""
import json
import os
from pathlib import Path

class SaveManager:
    """Handles saving and loading game data"""
    
    def __init__(self):
        # Create save directory in user's home
        self.save_dir = Path.home() / '.macan_ternak'
        self.save_file = self.save_dir / 'savegame.json'
        
        # Ensure save directory exists
        self.save_dir.mkdir(exist_ok=True)
        
    def save_game(self, game_data):
        """Save game data to JSON file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(game_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
            
    def load_game(self):
        """Load game data from JSON file"""
        if not self.save_file.exists():
            return None
            
        try:
            with open(self.save_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
            
    def delete_save(self):
        """Delete save file"""
        try:
            if self.save_file.exists():
                self.save_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
            
    def save_exists(self):
        """Check if save file exists"""
        return self.save_file.exists()