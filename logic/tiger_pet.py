"""
Tiger pet class with state machine and attributes
Updated with Coins system and Random Messages
"""
from enum import Enum
import math
import random

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
        
        # Progression & Economy
        self.level = 1
        self.exp = 0.0
        self.exp_to_next_level = 100.0
        self.coins = 100  # New: Currency system
        
        # State
        self.state = PetState.HAPPY
        self.age = 0
        
        # Decay rates (Balanced based on Guide)
        self.hunger_decay_rate = 0.12
        self.energy_decay_rate = 0.08
        self.mood_decay_rate = 0.06
        self.cleanliness_decay_rate = 0.04
        
    def update(self, delta_time=1.0):
        """Update pet state (called every game tick)"""
        self.age += delta_time
        
        # Decay stats
        self.hunger = max(0, self.hunger - self.hunger_decay_rate * delta_time)
        self.energy = max(0, self.energy - self.energy_decay_rate * delta_time)
        self.mood = max(0, self.mood - self.mood_decay_rate * delta_time)
        self.cleanliness = max(0, self.cleanliness - self.cleanliness_decay_rate * delta_time)
        
        # Mood modifiers
        mood_modifier = 0
        if self.hunger < 30: mood_modifier -= 0.2
        if self.energy < 30: mood_modifier -= 0.15
        if self.cleanliness < 30: mood_modifier -= 0.1
            
        self.mood = max(0, self.mood + mood_modifier * delta_time)
        self._update_state()
        
        # Passive exp gain
        if self._is_healthy():
            self.add_exp(0.1 * delta_time)
            
    def _update_state(self):
        if self.hunger < 20: self.state = PetState.HUNGRY
        elif self.energy < 20: self.state = PetState.TIRED
        elif self.cleanliness < 20: self.state = PetState.DIRTY
        elif self.mood < 30: self.state = PetState.SAD
        elif self.mood > 70 and self.hunger > 50 and self.energy > 50:
            self.state = PetState.HAPPY
        else:
            self.state = PetState.NEUTRAL
            
    def _is_healthy(self):
        return (self.hunger > 40 and self.energy > 40 and 
                self.mood > 40 and self.cleanliness > 30)
                
    def feed(self):
        if self.hunger >= 90:
            return False, "Tiger says: No thanks, I'm full! 🍖"
            
        self.hunger = min(100, self.hunger + 40)
        self.add_exp(5)
        
        # Random messages
        messages = [
            "Delicious! Tiger is happy! 🍖",
            "Nom nom nom! So tasty! 😋",
            "Tiger devoured the meat! 🐯",
            "Best meal ever! ⭐"
        ]
        return True, random.choice(messages)
        
    def clean(self):
        if self.cleanliness >= 90:
            return False, "Tiger is already sparkling clean! ✨"
            
        self.cleanliness = min(100, self.cleanliness + 50)
        self.mood = min(100, self.mood + 10)
        self.add_exp(3)
        
        messages = [
            "Sparkly clean! Tiger feels fresh! ✨",
            "Scrub scrub! All dirt gone! 🛁",
            "Tiger loves bubbles! 🧼"
        ]
        return True, random.choice(messages)
        
    def sleep(self):
        if self.energy >= 90:
            return False, "Tiger is not tired at all! ⚡"
            
        self.energy = min(100, self.energy + 60)
        self.mood = min(100, self.mood + 15)
        self.add_exp(4)
        
        messages = [
            "Zzz... Tiger had a good nap! 😴",
            "Tiger is dreaming of chasing butterflies... 🦋",
            "Fully recharged! 🔋"
        ]
        return True, random.choice(messages)
        
    def play(self):
        if self.energy < 20:
            return False, "Tiger is too tired to play! 😫"
            
        self.mood = min(100, self.mood + 30)
        self.energy = max(0, self.energy - 15)
        self.hunger = max(0, self.hunger - 10)
        self.add_exp(8)
        
        messages = [
            "So much fun! Tiger is happy! 🎾",
            "Rawr! Tiger caught the toy! 🧸",
            "Zoomies! Tiger is running around! 🏃"
        ]
        return True, random.choice(messages)
        
    def add_exp(self, amount):
        self.exp += amount
        # Earn coins based on XP
        coin_gain = amount * 0.5
        if coin_gain >= 1 or (self.age % 10 < 0.1): # Only add integer amounts or accumulate
             self.coins += coin_gain
        
        while self.exp >= self.exp_to_next_level:
            self.level_up()
            
    def level_up(self):
        self.exp -= self.exp_to_next_level
        self.level += 1
        self.coins += 50 # Bonus coins on level up
        self.exp_to_next_level = math.floor(100 * (1.2 ** (self.level - 1)))
        
        self.hunger = min(100, self.hunger + 20)
        self.energy = min(100, self.energy + 20)
        self.mood = min(100, self.mood + 20)
        self.cleanliness = min(100, self.cleanliness + 20)
        
        decay_reduction = 0.98
        self.hunger_decay_rate *= decay_reduction
        self.energy_decay_rate *= decay_reduction
        self.mood_decay_rate *= decay_reduction
        self.cleanliness_decay_rate *= decay_reduction
        
    def to_dict(self):
        data = super().to_dict() if hasattr(super(), 'to_dict') else {}
        # Manually constructing dict to ensure all fields including new ones
        return {
            'hunger': self.hunger,
            'energy': self.energy,
            'mood': self.mood,
            'cleanliness': self.cleanliness,
            'level': self.level,
            'exp': self.exp,
            'exp_to_next_level': self.exp_to_next_level,
            'age': self.age,
            'coins': int(self.coins),  # Save coins
            'hunger_decay_rate': self.hunger_decay_rate,
            'energy_decay_rate': self.energy_decay_rate,
            'mood_decay_rate': self.mood_decay_rate,
            'cleanliness_decay_rate': self.cleanliness_decay_rate
        }
        
    def from_dict(self, data):
        self.hunger = data.get('hunger', 100.0)
        self.energy = data.get('energy', 100.0)
        self.mood = data.get('mood', 100.0)
        self.cleanliness = data.get('cleanliness', 100.0)
        self.level = data.get('level', 1)
        self.exp = data.get('exp', 0.0)
        self.exp_to_next_level = data.get('exp_to_next_level', 100.0)
        self.age = data.get('age', 0)
        self.coins = data.get('coins', 100)  # Load coins
        self.hunger_decay_rate = data.get('hunger_decay_rate', 0.15)
        self.energy_decay_rate = data.get('energy_decay_rate', 0.1)
        self.mood_decay_rate = data.get('mood_decay_rate', 0.08)
        self.cleanliness_decay_rate = data.get('cleanliness_decay_rate', 0.05)
        self._update_state()