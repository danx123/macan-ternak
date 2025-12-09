"""
Tiger pet class with state machine and attributes
"""
from enum import Enum
import math

class PetState(Enum):
    """Pet emotional states"""
    HAPPY = "happy"
    NEUTRAL = "neutral"
    HUNGRY = "hungry"
    TIRED = "tired"
    DIRTY = "dirty"
    SAD = "sad"

class TigerPet:
    """Main pet class with all attributes and behaviors"""
    
    def __init__(self):
        # Core stats (0-100)
        self.hunger = 100.0
        self.energy = 100.0
        self.mood = 100.0
        self.cleanliness = 100.0
        
        # Progression
        self.level = 1
        self.exp = 0.0
        self.exp_to_next_level = 100.0
        
        # State
        self.state = PetState.HAPPY
        self.age = 0  # in seconds
        
        # Decay rates per second
        self.hunger_decay_rate = 0.15
        self.energy_decay_rate = 0.1
        self.mood_decay_rate = 0.08
        self.cleanliness_decay_rate = 0.05
        
    def update(self, delta_time=1.0):
        """Update pet state (called every game tick)"""
        self.age += delta_time
        
        # Decay stats
        self.hunger = max(0, self.hunger - self.hunger_decay_rate * delta_time)
        self.energy = max(0, self.energy - self.energy_decay_rate * delta_time)
        self.mood = max(0, self.mood - self.mood_decay_rate * delta_time)
        self.cleanliness = max(0, self.cleanliness - self.cleanliness_decay_rate * delta_time)
        
        # Mood is affected by other stats
        mood_modifier = 0
        if self.hunger < 30:
            mood_modifier -= 0.2
        if self.energy < 30:
            mood_modifier -= 0.15
        if self.cleanliness < 30:
            mood_modifier -= 0.1
            
        self.mood = max(0, self.mood + mood_modifier * delta_time)
        
        # Update state based on stats
        self._update_state()
        
        # Passive exp gain (very slow)
        if self._is_healthy():
            self.add_exp(0.1 * delta_time)
            
    def _update_state(self):
        """Determine current emotional state"""
        if self.hunger < 20:
            self.state = PetState.HUNGRY
        elif self.energy < 20:
            self.state = PetState.TIRED
        elif self.cleanliness < 20:
            self.state = PetState.DIRTY
        elif self.mood < 30:
            self.state = PetState.SAD
        elif self.mood > 70 and self.hunger > 50 and self.energy > 50:
            self.state = PetState.HAPPY
        else:
            self.state = PetState.NEUTRAL
            
    def _is_healthy(self):
        """Check if pet is in good condition"""
        return (self.hunger > 40 and self.energy > 40 and 
                self.mood > 40 and self.cleanliness > 30)
                
    def feed(self):
        """Feed the tiger"""
        if self.hunger >= 90:
            return False, "Tiger is not hungry!"
            
        self.hunger = min(100, self.hunger + 40)
        self.add_exp(5)
        return True, "Yum! Tiger enjoyed the meal! 🍖"
        
    def clean(self):
        """Clean the tiger"""
        if self.cleanliness >= 90:
            return False, "Tiger is already clean!"
            
        self.cleanliness = min(100, self.cleanliness + 50)
        self.mood = min(100, self.mood + 10)
        self.add_exp(3)
        return True, "Sparkly clean! Tiger feels fresh! ✨"
        
    def sleep(self):
        """Let tiger sleep"""
        if self.energy >= 90:
            return False, "Tiger is not tired!"
            
        self.energy = min(100, self.energy + 60)
        self.mood = min(100, self.mood + 15)
        self.add_exp(4)
        return True, "Zzz... Tiger had a good nap! 😴"
        
    def play(self):
        """Play with tiger"""
        if self.energy < 20:
            return False, "Tiger is too tired to play!"
            
        self.mood = min(100, self.mood + 30)
        self.energy = max(0, self.energy - 15)
        self.hunger = max(0, self.hunger - 10)
        self.add_exp(8)
        return True, "So much fun! Tiger is happy! 🎾"
        
    def add_exp(self, amount):
        """Add experience points and handle leveling"""
        self.exp += amount
        
        # Check for level up
        while self.exp >= self.exp_to_next_level:
            self.level_up()
            
    def level_up(self):
        """Level up the tiger"""
        self.exp -= self.exp_to_next_level
        self.level += 1
        
        # Increase exp requirement (exponential growth)
        self.exp_to_next_level = math.floor(100 * (1.2 ** (self.level - 1)))
        
        # Bonus stats on level up
        self.hunger = min(100, self.hunger + 20)
        self.energy = min(100, self.energy + 20)
        self.mood = min(100, self.mood + 20)
        self.cleanliness = min(100, self.cleanliness + 20)
        
        # Slightly reduce decay rates as tiger grows
        decay_reduction = 0.98
        self.hunger_decay_rate *= decay_reduction
        self.energy_decay_rate *= decay_reduction
        self.mood_decay_rate *= decay_reduction
        self.cleanliness_decay_rate *= decay_reduction
        
    def get_state_description(self):
        """Get human-readable state description"""
        descriptions = {
            PetState.HAPPY: "Your tiger is very happy! 😊",
            PetState.NEUTRAL: "Your tiger is doing okay.",
            PetState.HUNGRY: "Your tiger is hungry! 🍖",
            PetState.TIRED: "Your tiger needs rest! 😴",
            PetState.DIRTY: "Your tiger needs a bath! 🛁",
            PetState.SAD: "Your tiger is sad... 😢"
        }
        return descriptions.get(self.state, "Unknown state")
        
    def to_dict(self):
        """Convert pet to dictionary for saving"""
        return {
            'hunger': self.hunger,
            'energy': self.energy,
            'mood': self.mood,
            'cleanliness': self.cleanliness,
            'level': self.level,
            'exp': self.exp,
            'exp_to_next_level': self.exp_to_next_level,
            'age': self.age,
            'hunger_decay_rate': self.hunger_decay_rate,
            'energy_decay_rate': self.energy_decay_rate,
            'mood_decay_rate': self.mood_decay_rate,
            'cleanliness_decay_rate': self.cleanliness_decay_rate
        }
        
    def from_dict(self, data):
        """Load pet from dictionary"""
        self.hunger = data.get('hunger', 100.0)
        self.energy = data.get('energy', 100.0)
        self.mood = data.get('mood', 100.0)
        self.cleanliness = data.get('cleanliness', 100.0)
        self.level = data.get('level', 1)
        self.exp = data.get('exp', 0.0)
        self.exp_to_next_level = data.get('exp_to_next_level', 100.0)
        self.age = data.get('age', 0)
        self.hunger_decay_rate = data.get('hunger_decay_rate', 0.15)
        self.energy_decay_rate = data.get('energy_decay_rate', 0.1)
        self.mood_decay_rate = data.get('mood_decay_rate', 0.08)
        self.cleanliness_decay_rate = data.get('cleanliness_decay_rate', 0.05)
        self._update_state()