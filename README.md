# Macan Ternak - 3D Pet Simulator

A fully-featured 3D virtual pet simulator built with Python, PySide6, and OpenGL.

## 🎮 Features

- **3D Graphics**: Real-time OpenGL rendering with orbital camera controls
- **Pet System**: Complete tiger pet with hunger, energy, mood, and cleanliness stats
- **Progression**: Level up system with experience points
- **Auto-Save**: Automatic JSON-based save system
- **Offline Progress**: Pets continue to decay while you're away (limited)
- **Interactive Actions**: Feed, clean, play with, and let your tiger sleep
- **Visual Feedback**: Pet changes color based on mood and health
- **Modern UI**: Clean, responsive interface with progress bars and notifications

## 📁 Project Structure

```
macan-ternak/
├── main.py                      # Entry point
├── app/
│   ├── __init__.py
│   └── game_window.py           # Main window orchestrator
├── ui/
│   ├── __init__.py
│   ├── control_panel.py         # Left control panel
│   └── stats_panel.py           # Right stats panel
├── engine3d/
│   ├── __init__.py
│   └── viewport.py              # 3D OpenGL viewport
├── logic/
│   ├── __init__.py
│   ├── tiger_pet.py             # Pet state machine
│   └── game_manager.py          # Game coordinator
├── services/
│   ├── __init__.py
│   ├── save_manager.py          # JSON save system
│   └── settings_manager.py      # Settings management
└── assets/                      # Future: models, textures, sounds
```

## 📸 Screenshot
<img width="1365" height="767" alt="Screenshot 2025-12-09 201122" src="https://github.com/user-attachments/assets/a13f9320-18d4-474a-9828-db24336b0281" />



## 🚀 Installation

### Prerequisites

```bash
Python 3.8+
PySide6
PyOpenGL
PyOpenGL-accelerate (optional, for better performance)
```

### Install Dependencies

```bash
pip install PySide6 PyOpenGL PyOpenGL-accelerate
```

## ▶️ Running the Game

```bash
python main.py
```

## 🎯 How to Play

### Controls

- **Feed Tiger** 🍖: Increase hunger stat (+40 hunger, +5 XP)
- **Clean Tiger** 🛁: Increase cleanliness (+50 clean, +10 mood, +3 XP)
- **Let Sleep** 😴: Restore energy (+60 energy, +15 mood, +4 XP)
- **Play** 🎾: Boost mood significantly (+30 mood, -15 energy, -10 hunger, +8 XP)

### 3D Viewport Controls

- **Left Mouse Drag**: Rotate camera around tiger
- **Mouse Wheel**: Zoom in/out
- **Auto-Rotation**: Tiger slowly rotates for full view

### Stats System

All stats decay over time:
- **Hunger**: Decreases 0.15/sec (feed when below 90)
- **Energy**: Decreases 0.1/sec (sleep when below 90)
- **Mood**: Decreases 0.08/sec (affected by other stats)
- **Cleanliness**: Decreases 0.05/sec (clean when below 90)

### Leveling System

- Gain XP by interacting with your pet
- Level up when XP reaches threshold
- Each level: 
  - Increases XP requirement (exponential)
  - Boosts all stats by 20
  - Slightly reduces decay rates
  - Makes your tiger stronger!

### Pet States

Your tiger's emotional state changes based on stats:
- 😊 **Happy**: All stats above 70, mood > 70
- 😐 **Neutral**: Moderate stats
- 🍖 **Hungry**: Hunger < 20
- 😴 **Tired**: Energy < 20
- 🛁 **Dirty**: Cleanliness < 20
- 😢 **Sad**: Mood < 30

## 🔧 Architecture & Extensibility

### Modular Design

The project uses clean OOP principles with separation of concerns:

- **UI Layer** (`ui/`): All visual components, no game logic
- **Engine Layer** (`engine3d/`): 3D rendering, independent of game rules
- **Logic Layer** (`logic/`): Pure game mechanics, no UI dependencies
- **Services Layer** (`services/`): Persistence and settings

### Easy Extensions

#### Adding New Pet Types

1. Create new class inheriting from `TigerPet`
2. Override decay rates and behaviors
3. Add to game manager with pet selection UI

```python
class LionPet(TigerPet):
    def __init__(self):
        super().__init__()
        self.hunger_decay_rate = 0.2  # Lions eat more
```

#### Adding New Actions

1. Add method to `TigerPet` class
2. Add button to `ControlPanel`
3. Connect signal in `GameWindow`

```python
# In tiger_pet.py
def train(self):
    if self.energy < 30:
        return False, "Too tired to train!"
    self.exp += 20
    self.energy -= 30
    return True, "Training complete!"
```

#### Adding 3D Models

Replace the `_draw_tiger()` method in `viewport.py`:

```python
# Load .obj model
from OpenGL.GL import *
import pywavefront

def _draw_tiger_model(self):
    scene = pywavefront.Wavefront('assets/tiger.obj')
    # Render model...
```

#### Adding Animations

Extend the animation system in `Viewport3D`:

```python
def _animate_action(self, action_type):
    if action_type == "feed":
        # Play eating animation
        self.current_animation = "eating"
```

#### Adding Inventory System

1. Create `inventory.py` in `logic/`
2. Add inventory UI panel
3. Items can affect pet stats

```python
class Inventory:
    def __init__(self):
        self.items = {}
    
    def use_item(self, item_id, pet):
        # Apply item effects to pet
        pass
```

## 💾 Save System

- **Auto-save**: Every 30 seconds
- **Manual save**: On window close
- **Location**: `~/.macan_ternak/savegame.json`
- **Offline decay**: Up to 1 hour of decay is calculated when loading

### Save Data Structure

```json
{
  "pet": {
    "hunger": 85.5,
    "energy": 92.3,
    "mood": 88.1,
    "cleanliness": 95.0,
    "level": 5,
    "exp": 234.5,
    "exp_to_next_level": 248.8,
    "age": 3600
  },
  "last_save_time": 1234567890.123
}
```

## 🎨 Customization

### Colors and Styling

All UI styling is in respective widget files using Qt stylesheets:

```python
# Change button colors in control_panel.py
self.feed_btn.setStyleSheet("""
    QPushButton {
        background-color: #FF5722;  # New color
        ...
    }
""")
```

### Game Balance

Adjust decay rates and rewards in `tiger_pet.py`:

```python
class TigerPet:
    def __init__(self):
        self.hunger_decay_rate = 0.15  # Adjust this
        # ...
    
    def feed(self):
        self.hunger += 40  # Adjust reward
        self.add_exp(5)    # Adjust XP gain
```

## 🐛 Troubleshooting

### OpenGL Issues

If you see a black screen:
```bash
# Install OpenGL accelerate
pip install PyOpenGL-accelerate

# On Linux, install GLUT
sudo apt-get install freeglut3-dev
```

### Import Errors

```bash
# Make sure all __init__.py files exist
touch app/__init__.py
touch ui/__init__.py
touch engine3d/__init__.py
touch logic/__init__.py
touch services/__init__.py
```

### Performance Issues

- Reduce animation frame rate in `viewport.py`
- Disable lighting effects
- Lower polygon count in 3D models

## 🚀 Future Enhancements

### Planned Features

- [ ] Multiple pet types (Lion, Leopard, Cheetah)
- [ ] Real 3D animated models with skeletal animation
- [ ] Sound effects and background music
- [ ] Mini-games for earning XP
- [ ] Shop system for buying items
- [ ] Multiple environments (savanna, jungle, mountain)
- [ ] Pet breeding system
- [ ] Multiplayer pet battles
- [ ] Achievement system
- [ ] Cloud save support

### Technical Improvements

- [ ] Add unit tests
- [ ] Implement proper animation system
- [ ] Add model loader for .fbx/.obj files
- [ ] Particle effects for actions
- [ ] Better camera system with smooth transitions
- [ ] Shader support for advanced graphics
- [ ] Resource management system

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Areas that need help:
- 3D models and animations
- Sound design
- Balancing game mechanics
- Adding new features
- Bug fixes

## 📧 Contact

Created for learning and fun! Enjoy raising your virtual tiger! 🐯
