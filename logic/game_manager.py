"""
Game manager that coordinates all game systems
"""
from logic.tiger_pet import TigerPet
import time

class GameManager:
    """Central game manager coordinating all systems"""
    
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.pet = TigerPet()
        self.last_update_time = time.time()
        self.is_paused = False
        
    def update(self):
        """Main game update loop"""
        if self.is_paused:
            return
            
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Update pet
        self.pet.update(delta_time)
        
        # Auto-save every 30 seconds
        if int(current_time) % 30 == 0:
            self.save_game()
            
    def feed_pet(self):
        """Feed the pet"""
        return self.pet.feed()
        
    def clean_pet(self):
        """Clean the pet"""
        return self.pet.clean()
        
    def sleep_pet(self):
        """Let pet sleep"""
        return self.pet.sleep()
        
    def play_with_pet(self):
        """Play with pet"""
        return self.pet.play()
        
    def save_game(self):
        """Save current game state"""
        game_data = {
            'pet': self.pet.to_dict(),
            'last_save_time': time.time()
        }
        self.save_manager.save_game(game_data)
        
    def load_game(self):
        """Load saved game state"""
        game_data = self.save_manager.load_game()
        
        if game_data and 'pet' in game_data:
            self.pet.from_dict(game_data['pet'])
            
            # Calculate offline progress
            last_save = game_data.get('last_save_time', time.time())
            offline_time = time.time() - last_save
            
            # Limit offline decay to 1 hour max
            offline_time = min(offline_time, 3600)
            
            if offline_time > 60:  # More than 1 minute offline
                self.pet.update(offline_time)
                
    def pause(self):
        """Pause the game"""
        self.is_paused = True
        
    def resume(self):
        """Resume the game"""
        self.is_paused = False
        self.last_update_time = time.time()
        
    def reset_game(self):
        """Reset to new game"""
        self.pet = TigerPet()
        self.save_game()