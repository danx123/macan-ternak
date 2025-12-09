# 🛠️ Development Guide - Macan Ternak

Complete guide for developers who want to extend and modify the game.

## 🎯 Quick Modification Examples

### 1. Change Tiger Colors

**File**: `engine3d/viewport.py`

```python
# Find this line (around line 95):
self.tiger_color = [1.0, 0.6, 0.2]  # Orange tiger

# Change to:
self.tiger_color = [0.9, 0.9, 0.9]  # White tiger
self.tiger_color = [0.2, 0.2, 0.2]  # Black panther
self.tiger_color = [0.8, 0.7, 0.4]  # Lion color
```

### 2. Adjust Game Difficulty

**File**: `logic/tiger_pet.py`

```python
# In TigerPet.__init__(), modify decay rates:

# EASY MODE (slower decay)
self.hunger_decay_rate = 0.08   # was 0.15
self.energy_decay_rate = 0.05   # was 0.10
self.mood_decay_rate = 0.04     # was 0.08
self.cleanliness_decay_rate = 0.03  # was 0.05

# HARD MODE (faster decay)
self.hunger_decay_rate = 0.25
self.energy_decay_rate = 0.20
self.mood_decay_rate = 0.15
self.cleanliness_decay_rate = 0.10
```

### 3. Change Button Colors

**File**: `ui/control_panel.py`

```python
# Feed button (around line 37)
self.feed_btn.setStyleSheet("""
    QPushButton {
        background-color: #FF5722;  # Change this!
        color: white;
        ...
    }
""")

# Material Design colors:
# Red: #F44336, Pink: #E91E63, Purple: #9C27B0
# Blue: #2196F3, Teal: #009688, Green: #4CAF50
# Orange: #FF9800, Brown: #795548, Grey: #9E9E9E
```

### 4. Add Custom Notification Messages

**File**: `logic/tiger_pet.py`

```python
def feed(self):
    if self.hunger >= 90:
        return False, "Tiger says: No thanks, I'm full! 🍖"
    
    self.hunger = min(100, self.hunger + 40)
    self.add_exp(5)
    
    # Add random messages
    import random
    messages = [
        "Delicious! Tiger is happy! 🍖",
        "Nom nom nom! So tasty! 😋",
        "Tiger devoured the meat! 🐯",
        "Best meal ever! ⭐"
    ]
    return True, random.choice(messages)
```

### 5. Change Game Speed

**File**: `app/game_window.py`

```python
# In _setup_game_loop() method:
self.game_timer.start(1000)  # 1000ms = 1 second

# Change to:
self.game_timer.start(500)   # 0.5 seconds (faster)
self.game_timer.start(2000)  # 2 seconds (slower)
```

## 🏗️ Major Feature Additions

### Feature 1: Add a Shop System

#### Step 1: Create Shop Data Model

**File**: `logic/shop.py`

```python
class ShopItem:
    def __init__(self, name, description, price, effect_type, effect_value):
        self.name = name
        self.description = description
        self.price = price  # Cost in coins
        self.effect_type = effect_type  # 'hunger', 'energy', etc.
        self.effect_value = effect_value

class Shop:
    def __init__(self):
        self.items = [
            ShopItem("Premium Food", "Delicious meat", 50, "hunger", 60),
            ShopItem("Energy Drink", "Instant boost", 40, "energy", 80),
            ShopItem("Toy Ball", "Improves mood", 30, "mood", 50),
            ShopItem("Bath Set", "Extra clean", 35, "cleanliness", 70)
        ]
    
    def buy_item(self, item, pet, coins):
        if coins < item.price:
            return False, "Not enough coins!", coins
        
        # Apply effect
        current = getattr(pet, item.effect_type)
        setattr(pet, item.effect_type, min(100, current + item.effect_value))
        
        coins -= item.price
        return True, f"Bought {item.name}!", coins
```

#### Step 2: Add Coins to Pet

**File**: `logic/tiger_pet.py`

```python
class TigerPet:
    def __init__(self):
        # ... existing code ...
        self.coins = 100  # Starting coins
    
    def add_exp(self, amount):
        self.exp += amount
        self.coins += int(amount * 0.5)  # Earn coins from XP
        # ... rest of method ...
```

#### Step 3: Create Shop UI

**File**: `ui/shop_panel.py`

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget
from PySide6.QtCore import Signal

class ShopPanel(QWidget):
    item_purchased = Signal(object)  # Emits ShopItem
    
    def __init__(self, shop):
        super().__init__()
        self.shop = shop
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.coins_label = QLabel("Coins: 100")
        layout.addWidget(self.coins_label)
        
        self.item_list = QListWidget()
        for item in self.shop.items:
            self.item_list.addItem(f"{item.name} - {item.price} coins")
        layout.addWidget(self.item_list)
        
        buy_btn = QPushButton("Buy Selected Item")
        buy_btn.clicked.connect(self._on_buy)
        layout.addWidget(buy_btn)
    
    def _on_buy(self):
        if self.item_list.currentRow() >= 0:
            item = self.shop.items[self.item_list.currentRow()]
            self.item_purchased.emit(item)
    
    def update_coins(self, coins):
        self.coins_label.setText(f"Coins: {coins}")
```

#### Step 4: Integrate into Main Window

**File**: `app/game_window.py`

```python
from logic.shop import Shop
from ui.shop_panel import ShopPanel

class GameWindow(QMainWindow):
    def __init__(self):
        # ... existing code ...
        self.shop = Shop()
        
    def _setup_ui(self):
        # ... existing code ...
        
        # Add shop panel
        self.shop_panel = ShopPanel(self.shop)
        self.shop_panel.setFixedWidth(200)
        main_layout.addWidget(self.shop_panel)
        
        # Connect signal
        self.shop_panel.item_purchased.connect(self._on_item_purchased)
    
    def _on_item_purchased(self, item):
        pet = self.game_manager.pet
        success, msg, new_coins = self.shop.buy_item(item, pet, pet.coins)
        if success:
            pet.coins = new_coins
            self.shop_panel.update_coins(new_coins)
        self.stats_panel.show_notification(msg, success)
```

### Feature 2: Add Mini-Games

#### Example: Catch the Fish Game

**File**: `logic/minigames/catch_fish.py`

```python
import random

class CatchFishGame:
    def __init__(self):
        self.duration = 10  # seconds
        self.fish_caught = 0
        self.is_active = False
    
    def start(self):
        self.is_active = True
        self.fish_caught = 0
        self.time_left = self.duration
    
    def update(self, dt):
        if not self.is_active:
            return
        
        self.time_left -= dt
        if self.time_left <= 0:
            self.end()
    
    def catch(self):
        """Called when player clicks"""
        if self.is_active:
            # Random success based on timing
            if random.random() > 0.3:
                self.fish_caught += 1
                return True
        return False
    
    def end(self):
        self.is_active = False
        # Rewards based on fish caught
        exp_reward = self.fish_caught * 10
        coin_reward = self.fish_caught * 5
        return exp_reward, coin_reward
```

**File**: `ui/minigame_panel.py`

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QTimer, Signal

class CatchFishPanel(QWidget):
    game_ended = Signal(int, int)  # exp, coins
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self._setup_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.status_label = QLabel("Click to catch fish!")
        layout.addWidget(self.status_label)
        
        self.catch_btn = QPushButton("🐟 CATCH!")
        self.catch_btn.clicked.connect(self._on_catch)
        layout.addWidget(self.catch_btn)
    
    def start_game(self):
        self.game.start()
        self.timer.start(100)  # Update 10 times per second
    
    def _on_catch(self):
        if self.game.catch():
            self.status_label.setText(f"Caught {self.game.fish_caught} fish!")
    
    def _update(self):
        if not self.game.is_active:
            self.timer.stop()
            exp, coins = self.game.end()
            self.game_ended.emit(exp, coins)
```

### Feature 3: Multiple Pet Types

#### Step 1: Create Base Pet Class

**File**: `logic/base_pet.py`

```python
from abc import ABC, abstractmethod

class BasePet(ABC):
    def __init__(self):
        self.hunger = 100.0
        self.energy = 100.0
        self.mood = 100.0
        self.cleanliness = 100.0
        self.level = 1
        self.exp = 0.0
    
    @abstractmethod
    def get_species_name(self):
        pass
    
    @abstractmethod
    def get_special_ability(self):
        pass
    
    def update(self, dt):
        # Common update logic
        self.hunger -= self.hunger_decay_rate * dt
        self.energy -= self.energy_decay_rate * dt
        # ... etc
```

#### Step 2: Create Specific Pet Types

**File**: `logic/tiger_pet.py`

```python
from .base_pet import BasePet

class TigerPet(BasePet):
    def __init__(self):
        super().__init__()
        self.hunger_decay_rate = 0.15
        self.energy_decay_rate = 0.10
    
    def get_species_name(self):
        return "Tiger"
    
    def get_special_ability(self):
        return "Mighty Roar: +50% XP for 1 minute"
```

**File**: `logic/lion_pet.py`

```python
from .base_pet import BasePet

class LionPet(BasePet):
    def __init__(self):
        super().__init__()
        self.hunger_decay_rate = 0.20  # Eats more
        self.energy_decay_rate = 0.08  # More energetic
    
    def get_species_name(self):
        return "Lion"
    
    def get_special_ability(self):
        return "King's Pride: Slower mood decay"
```

#### Step 3: Pet Selection UI

**File**: `ui/pet_selection.py`

```python
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class PetSelectionDialog(QDialog):
    pet_selected = Signal(str)  # Emits pet type name
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choose Your Pet")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        tiger_btn = QPushButton("🐯 Tiger\nBalanced stats")
        tiger_btn.clicked.connect(lambda: self._select("tiger"))
        layout.addWidget(tiger_btn)
        
        lion_btn = QPushButton("🦁 Lion\nHigh energy, eats more")
        lion_btn.clicked.connect(lambda: self._select("lion"))
        layout.addWidget(lion_btn)
    
    def _select(self, pet_type):
        self.pet_selected.emit(pet_type)
        self.accept()
```

## 🎨 Advanced 3D Rendering

### Load Real 3D Models

**Install PyWavefront**:
```bash
pip install PyWavefront
```

**File**: `engine3d/model_loader.py`

```python
import pywavefront
from OpenGL.GL import *

class ModelLoader:
    def __init__(self, filepath):
        self.scene = pywavefront.Wavefront(filepath, collect_faces=True)
    
    def render(self):
        for mesh in self.scene.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    if mesh.materials[0].vertex_format == 'T2F_N3F_V3F':
                        glTexCoord2f(*self.scene.vertices[vertex_i][0:2])
                        glNormal3f(*self.scene.vertices[vertex_i][2:5])
                        glVertex3f(*self.scene.vertices[vertex_i][5:8])
                    else:
                        glVertex3f(*self.scene.vertices[vertex_i])
            glEnd()
```

**Usage in Viewport**:

```python
class Viewport3D(QOpenGLWidget):
    def __init__(self, game_manager):
        super().__init__()
        self.tiger_model = None
    
    def initializeGL(self):
        # ... existing code ...
        try:
            self.tiger_model = ModelLoader('assets/models/tiger.obj')
        except:
            print("No 3D model found, using placeholder")
    
    def _draw_tiger(self):
        if self.tiger_model:
            self.tiger_model.render()
        else:
            # Use existing placeholder code
            self._draw_placeholder_tiger()
```

## 🔊 Adding Sound Effects

**Install**:
```bash
pip install pygame
```

**File**: `services/sound_manager.py`

```python
import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self._load_sounds()
    
    def _load_sounds(self):
        sound_dir = 'assets/sounds'
        if not os.path.exists(sound_dir):
            return
        
        sound_files = {
            'feed': 'feed.wav',
            'clean': 'clean.wav',
            'sleep': 'sleep.wav',
            'play': 'play.wav',
            'levelup': 'levelup.wav'
        }
        
        for name, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
    
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.sfx_volume)
            self.sounds[sound_name].play()
    
    def play_music(self, music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)  # Loop
```

## 📊 Analytics & Statistics

**File**: `logic/analytics.py`

```python
from datetime import datetime
import json
from pathlib import Path

class GameAnalytics:
    def __init__(self):
        self.stats_file = Path.home() / '.macan_ternak' / 'analytics.json'
        self.stats = self._load_stats()
    
    def _load_stats(self):
        if self.stats_file.exists():
            with open(self.stats_file) as f:
                return json.load(f)
        return {
            'total_playtime': 0,
            'sessions': [],
            'actions_performed': {'feed': 0, 'clean': 0, 'sleep': 0, 'play': 0},
            'max_level_reached': 1,
            'total_exp_earned': 0
        }
    
    def start_session(self):
        self.session_start = datetime.now()
    
    def end_session(self):
        duration = (datetime.now() - self.session_start).total_seconds()
        self.stats['total_playtime'] += duration
        self.stats['sessions'].append({
            'date': datetime.now().isoformat(),
            'duration': duration
        })
        self._save_stats()
    
    def log_action(self, action_name):
        if action_name in self.stats['actions_performed']:
            self.stats['actions_performed'][action_name] += 1
    
    def update_max_level(self, level):
        self.stats['max_level_reached'] = max(
            self.stats['max_level_reached'], 
            level
        )
    
    def _save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
```

## 🧪 Unit Testing

**File**: `tests/test_tiger_pet.py`

```python
import unittest
from logic.tiger_pet import TigerPet

class TestTigerPet(unittest.TestCase):
    def setUp(self):
        self.pet = TigerPet()
    
    def test_initial_stats(self):
        self.assertEqual(self.pet.hunger, 100)
        self.assertEqual(self.pet.energy, 100)
        self.assertEqual(self.pet.level, 1)
    
    def test_hunger_decay(self):
        initial_hunger = self.pet.hunger
        self.pet.update(1.0)
        self.assertLess(self.pet.hunger, initial_hunger)
    
    def test_feeding(self):
        self.pet.hunger = 50
        success, _ = self.pet.feed()
        self.assertTrue(success)
        self.assertEqual(self.pet.hunger, 90)
    
    def test_feeding_when_full(self):
        self.pet.hunger = 95
        success, _ = self.pet.feed()
        self.assertFalse(success)
    
    def test_leveling_up(self):
        self.pet.exp = 0
        self.pet.add_exp(100)
        self.assertEqual(self.pet.level, 2)
        self.assertLess(self.pet.exp, 100)

if __name__ == '__main__':
    unittest.main()
```

**Run tests**:
```bash
python -m unittest discover tests
```

## 🚀 Performance Optimization

### 1. Profile Your Code

```python
import cProfile
import pstats

def profile_game():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run game for 60 seconds
    # ... game code ...
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

### 2. Optimize 3D Rendering

```python
# Use display lists (compile geometry once)
class Viewport3D:
    def initializeGL(self):
        # ... existing code ...
        self.tiger_display_list = glGenLists(1)
        glNewList(self.tiger_display_list, GL_COMPILE)
        self._draw_tiger_geometry()
        glEndList()
    
    def _draw_tiger(self):
        glCallList(self.tiger_display_list)
```

### 3. Batch UI Updates

```python
# Instead of updating every stat individually
def _update_ui(self):
    # Batch read all pet stats
    pet = self.game_manager.pet
    stats = (pet.hunger, pet.energy, pet.mood, pet.cleanliness, 
             pet.level, pet.exp, pet.exp_to_next_level)
    
    # Single update call
    self.stats_panel.update_all(*stats)
```

## 📦 Building Executables

### Using PyInstaller

```bash
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile --windowed --name "MacanTernak" main.py

# With icon (Windows)
pyinstaller --onefile --windowed --icon=assets/icon.ico --name "MacanTernak" main.py
```

### Creating Installer (Windows)

Use Inno Setup with this script:

```
[Setup]
AppName=Macan Ternak
AppVersion=1.0
DefaultDirName={pf}\MacanTernak
DefaultGroupName=Macan Ternak

[Files]
Source: "dist\MacanTernak.exe"; DestDir: "{app}"
Source: "assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs

[Icons]
Name: "{group}\Macan Ternak"; Filename: "{app}\MacanTernak.exe"
```

## 🐛 Debugging Tips

### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='macan_debug.log'
)

logger = logging.getLogger(__name__)

# In your code:
logger.debug(f"Pet stats: hunger={pet.hunger}, mood={pet.mood}")
logger.info("Game started")
logger.warning("Low hunger detected")
logger.error("Failed to save game")
```

### Qt Debug Output

```python
# In main.py
import sys
from PySide6.QtCore import qInstallMessageHandler, QtMsgType

def qt_message_handler(mode, context, message):
    if mode == QtMsgType.QtInfoMsg:
        print(f"INFO: {message}")
    elif mode == QtMsgType.QtWarningMsg:
        print(f"WARNING: {message}")
    elif mode == QtMsgType.QtCriticalMsg:
        print(f"CRITICAL: {message}")
    elif mode == QtMsgType.QtFatalMsg:
        print(f"FATAL: {message}")

qInstallMessageHandler(qt_message_handler)
```

---

## 🎓 Next Steps

1. **Start Small**: Make small modifications to understand the codebase
2. **Experiment**: Try breaking things to learn how they work
3. **Read Code**: Study each file to understand the architecture
4. **Add Features**: Start with simple additions, then tackle complex ones
5. **Share**: Contribute your improvements back to the community!

Happy developing! 🐯
