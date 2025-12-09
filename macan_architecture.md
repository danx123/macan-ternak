# 🏗️ Macan Ternak - System Architecture

This document explains the complete architecture and how all components work together.

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                   main.py                           │
│              (Application Entry)                    │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              app/game_window.py                     │
│            (Main Window Controller)                 │
│  - Initializes all systems                          │
│  - Connects UI to logic                             │
│  - Manages game loop timer                          │
└─────┬──────────────┬──────────────┬─────────────────┘
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────────┐
│UI Layer  │  │3D Engine │  │ Logic Layer  │
└──────────┘  └──────────┘  └──────────────┘
      │              │              │
      ▼              ▼              ▼
[Widgets]      [Viewport]      [Game State]
                                     │
                                     ▼
                              ┌──────────────┐
                              │   Services   │
                              │  (Save/Load) │
                              └──────────────┘
```

## 🎯 Design Principles

### 1. Separation of Concerns
- **UI** knows nothing about game logic
- **Logic** knows nothing about rendering
- **Engine** is independent of game rules
- **Services** are pure utilities

### 2. Data Flow

```
User Action → UI Signal → Game Manager → Pet Logic
                                            ↓
                                      State Update
                                            ↓
                                    Update UI/3D View
```

### 3. Update Loop

```
Timer (1 second) → GameManager.update()
                       ↓
                   Pet.update()
                       ↓
              Stats Decay & State Change
                       ↓
              UI Refresh (Stats Panel)
                       ↓
           3D Refresh (Visual Feedback)
```

## 📦 Module Breakdown

### 1. Entry Point (`main.py`)

```python
Purpose: Initialize Qt application and show main window
Dependencies: PySide6, app.GameWindow
Responsibilities:
  - Create QApplication
  - Set application style
  - Create and show GameWindow
  - Handle exit
```

### 2. App Layer (`app/`)

#### `game_window.py`

```python
Purpose: Main window orchestrator
Key Responsibilities:
  - Create and layout all UI components
  - Initialize GameManager
  - Setup game loop timer (1 second ticks)
  - Connect UI signals to game actions
  - Handle window events (close = save)
  
Key Methods:
  - _setup_ui(): Create layout
  - _game_update(): Called every second
  - _update_ui(): Refresh all displays
  - _on_feed/clean/sleep/play(): Action handlers
```

### 3. UI Layer (`ui/`)

#### `control_panel.py`

```python
Purpose: Left panel with action buttons
Signals:
  - feed_clicked
  - clean_clicked
  - sleep_clicked
  - play_clicked
  
Features:
  - Styled buttons with icons
  - Instructions display
  - No game logic - pure presentation
```

#### `stats_panel.py`

```python
Purpose: Right panel showing pet status
Key Features:
  - Progress bars for all stats
  - Dynamic color coding (red/orange/normal)
  - Experience bar with level display
  - Animated notifications
  
Key Methods:
  - update_stats(): Refresh all displays
  - show_notification(): Show fade-out message
  - _update_bar_color(): Color based on value
```

### 4. Engine3D Layer (`engine3d/`)

#### `viewport.py`

```python
Purpose: 3D OpenGL rendering viewport
Key Features:
  - OpenGL 2.1 rendering
  - Orbital camera system
  - Mouse interaction (drag/zoom)
  - Placeholder 3D tiger model
  - Animation system (breathing, rotation)
  
Rendering Pipeline:
  1. Setup camera (gluLookAt)
  2. Draw ground plane
  3. Draw tiger with components:
     - Body (main cube)
     - Head with eyes
     - Four legs
     - Tail with animation
  4. Apply lighting
  
Key Methods:
  - initializeGL(): Setup OpenGL
  - paintGL(): Render frame
  - _draw_tiger(): Draw pet model
  - _animate(): Update animation state
  - update_scene(): React to pet state
```

### 5. Logic Layer (`logic/`)

#### `tiger_pet.py`

```python
Purpose: Pet state machine and attributes
Core Attributes:
  - hunger, energy, mood, cleanliness (0-100)
  - level, exp, exp_to_next_level
  - state (PetState enum)
  - decay_rates
  
State Machine:
  HAPPY → All stats good
  NEUTRAL → Moderate stats
  HUNGRY → Hunger < 20
  TIRED → Energy < 20
  DIRTY → Cleanliness < 20
  SAD → Mood < 30
  
Key Methods:
  - update(): Apply decay and state logic
  - feed/clean/sleep/play(): Actions
  - add_exp(): Handle leveling
  - to_dict/from_dict(): Serialization
```

#### `game_manager.py`

```python
Purpose: Central coordinator
Responsibilities:
  - Own TigerPet instance
  - Track game time
  - Call pet.update() on timer
  - Delegate actions to pet
  - Handle save/load
  - Calculate offline progress
  
Key Features:
  - Auto-save every 30 seconds
  - Offline decay (max 1 hour)
  - Pause/resume functionality
```

### 6. Services Layer (`services/`)

#### `save_manager.py`

```python
Purpose: JSON persistence
Save Location: ~/.macan_ternak/savegame.json
Methods:
  - save_game(data): Write JSON
  - load_game(): Read JSON
  - delete_save(): Remove file
  - save_exists(): Check file
```

#### `settings_manager.py`

```python
Purpose: Game settings persistence
Settings Managed:
  - sound_enabled
  - music/sfx volume
  - auto_save settings
  - graphics quality
  - language
  
Future Use: Can control game behavior
```

## 🔄 Communication Flow

### Example: User Clicks "Feed" Button

```
1. User clicks Feed button
   ↓
2. ControlPanel emits feed_clicked signal
   ↓
3. GameWindow._on_feed() receives signal
   ↓
4. Calls game_manager.feed_pet()
   ↓
5. GameManager delegates to pet.feed()
   ↓
6. TigerPet checks hunger level
   ↓
7. If valid: increase hunger, add XP
   ↓
8. Return (success, message)
   ↓
9. GameWindow receives response
   ↓
10. Calls stats_panel.show_notification(message)
    ↓
11. Next game tick: UI updates reflect new stats
    ↓
12. Viewport updates tiger color if needed
```

## 🎨 Styling Architecture

### CSS-Like Styling (Qt Stylesheets)

All visual styling uses Qt's stylesheet system:

```python
# Example from control_panel.py
button.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")
```

Benefits:
- Easy to modify colors/fonts
- No recompilation needed
- Designer-friendly
- Consistent theming

## 🔌 Extension Points

### Adding New Pet Type

```python
# 1. Create new pet class
class LionPet(TigerPet):
    def __init__(self):
        super().__init__()
        # Override attributes
        self.hunger_decay_rate = 0.2

# 2. Modify GameManager
self.pet = LionPet()  # Instead of TigerPet()

# 3. Modify Viewport
def _draw_lion(self):
    # Different 3D model
    pass
```

### Adding New Action

```python
# 1. In tiger_pet.py
def train(self):
    if self.energy < 20:
        return False, "Too tired!"
    self.energy -= 20
    self.add_exp(15)
    return True, "Training complete!"

# 2. In control_panel.py
self.train_btn = QPushButton("🏋️ Train")
train_clicked = Signal()

# 3. In game_window.py
def _on_train(self):
    success, msg = self.game_manager.train_pet()
    self.stats_panel.show_notification(msg, success)
```

### Adding 3D Models

```python
# In viewport.py
import pywavefront

class Viewport3D(QOpenGLWidget):
    def __init__(self):
        self.tiger_model = pywavefront.Wavefront('assets/models/tiger.obj')
    
    def _draw_tiger(self):
        for mesh in self.tiger_model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                # Render vertices
            glEnd()
```

### Adding Sound System

```python
# Create services/sound_manager.py
from PySide6.QtMultimedia import QSoundEffect

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self._load_sounds()
    
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

# In game_window.py
self.sound_manager = SoundManager()
# In action handlers:
self.sound_manager.play('feed')
```

## 🧪 Testing Strategy

### Unit Tests Structure

```python
# tests/test_tiger_pet.py
def test_hunger_decay():
    pet = TigerPet()
    initial = pet.hunger
    pet.update(1.0)
    assert pet.hunger < initial

def test_feeding():
    pet = TigerPet()
    pet.hunger = 50
    success, msg = pet.feed()
    assert success == True
    assert pet.hunger == 90
```

### Integration Tests

```python
# tests/test_game_manager.py
def test_save_load():
    gm = GameManager(SaveManager())
    gm.pet.hunger = 75
    gm.save_game()
    
    gm2 = GameManager(SaveManager())
    gm2.load_game()
    assert gm2.pet.hunger == 75
```

## 📈 Performance Considerations

### Current Performance

- **Update Loop**: 1 second interval (lightweight)
- **3D Rendering**: ~60 FPS (16ms animation timer)
- **Memory**: ~50-100 MB typical usage

### Optimization Opportunities

1. **3D Rendering**
   - Use vertex buffer objects (VBO)
   - Batch draw calls
   - LOD system for complex models

2. **Game Logic**
   - Use fixed-point math for stats
   - Cache state calculations
   - Lazy evaluation for UI updates

3. **Save System**
   - Compress JSON (gzip)
   - Binary format for large saves
   - Incremental saves (only changed data)

## 🚀 Scaling Up

### Multi-Pet Support

```python
class GameManager:
    def __init__(self):
        self.pets = []
        self.active_pet_index = 0
    
    @property
    def pet(self):
        return self.pets[self.active_pet_index]
    
    def add_pet(self, pet_type):
        new_pet = pet_type()
        self.pets.append(new_pet)
```

### Online Features

```python
# Add services/network_manager.py
class NetworkManager:
    def __init__(self):
        self.api_url = "https://api.macanternak.com"
    
    def sync_save(self, save_data):
        # Upload to cloud
        pass
    
    def get_leaderboard(self):
        # Fetch rankings
        pass
```

## 🎓 Learning Resources

### For Beginners

1. **Python OOP**: Learn classes, inheritance, signals
2. **PySide6 Basics**: Qt widgets, layouts, signals/slots
3. **OpenGL Fundamentals**: 3D coordinates, transformations, lighting

### For Advanced

1. **Game Architecture**: State machines, component systems
2. **3D Graphics**: Shaders, skeletal animation, physics
3. **Optimization**: Profiling, memory management, GPU utilization

## 📝 Code Quality

### Conventions Used

- **Classes**: PascalCase (`TigerPet`, `GameManager`)
- **Functions/Methods**: snake_case (`update_stats`, `feed_pet`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_HUNGER`)
- **Private Methods**: Leading underscore (`_update_state`)

### Documentation

- All classes have docstrings
- Complex methods explained
- Key algorithms commented
- Type hints (future improvement)

## 🔐 Security & Privacy

### Data Storage

- All data stored locally
- No analytics or tracking
- Save files are plain JSON (human-readable)
- No network communication

### Future Considerations

If adding online features:
- Encrypt save data
- Validate all server responses
- Implement authentication
- Rate limit API calls

---

This architecture is designed to be:
- **Modular**: Easy to modify individual components
- **Extensible**: Simple to add new features
- **Maintainable**: Clear separation of concerns
- **Educational**: Good patterns for learning

Happy coding! 🐯
