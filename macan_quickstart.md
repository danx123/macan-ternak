# 🚀 Quick Start Guide - Macan Ternak

Get up and running in 5 minutes!

## Step 1: Install Python

Make sure you have Python 3.8 or higher installed:

```bash
python --version
# Should show: Python 3.8.x or higher
```

## Step 2: Set Up Project

### Option A: Automatic Setup (Linux/Mac)

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Option B: Manual Setup (Windows/Linux/Mac)

```bash
# Create directories
mkdir -p app ui engine3d logic services assets

# Create __init__.py files
touch app/__init__.py
touch ui/__init__.py
touch engine3d/__init__.py
touch logic/__init__.py
touch services/__init__.py

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Create the Files

Copy all the provided Python files into their respective directories:

```
macan-ternak/
├── main.py
├── app/
│   ├── __init__.py
│   └── game_window.py
├── ui/
│   ├── __init__.py
│   ├── control_panel.py
│   └── stats_panel.py
├── engine3d/
│   ├── __init__.py
│   └── viewport.py
├── logic/
│   ├── __init__.py
│   ├── tiger_pet.py
│   └── game_manager.py
└── services/
    ├── __init__.py
    ├── save_manager.py
    └── settings_manager.py
```

## Step 4: Run the Game!

```bash
python main.py
```

## 🎮 First Time Playing

1. **Window Opens**: You'll see a 3D tiger in the center viewport
2. **Check Stats**: Right panel shows hunger, energy, mood, cleanliness
3. **Interact**: Use buttons on the left panel
4. **Camera**: Drag with mouse to rotate, scroll to zoom
5. **Watch Stats**: They decay over time - keep your tiger happy!

## 🔧 Troubleshooting

### Black 3D Screen

```bash
# Install OpenGL accelerate
pip install PyOpenGL-accelerate

# On Ubuntu/Debian
sudo apt-get install freeglut3-dev python3-opengl

# On macOS (if needed)
brew install freeglut
```

### Module Import Errors

Make sure all `__init__.py` files exist:

```bash
# Check files exist
ls app/__init__.py
ls ui/__init__.py
ls engine3d/__init__.py
ls logic/__init__.py
ls services/__init__.py
```

### PySide6 Installation Issues

```bash
# Try upgrading pip first
pip install --upgrade pip

# Install PySide6
pip install PySide6

# Or use conda
conda install -c conda-forge pyside6
```

## 📖 Basic Gameplay

### Understanding Stats

- **Hunger** 🍖: Feed when below 90 (decays 0.15/sec)
- **Energy** ⚡: Sleep when below 90 (decays 0.1/sec)
- **Mood** 😊: Play to boost (decays 0.08/sec, affected by other stats)
- **Cleanliness** ✨: Clean when below 90 (decays 0.05/sec)

### Actions & XP

| Action | Effect | XP Gain |
|--------|--------|---------|
| Feed   | +40 hunger | 5 XP |
| Clean  | +50 clean, +10 mood | 3 XP |
| Sleep  | +60 energy, +15 mood | 4 XP |
| Play   | +30 mood, -15 energy, -10 hunger | 8 XP |

### Leveling Up

- Collect XP by interacting with your tiger
- Each level requires more XP (exponential growth)
- Level up bonuses:
  - All stats +20
  - Decay rates decrease slightly
  - Your tiger becomes more resilient!

## 🎯 Pro Tips

1. **Balance is Key**: Don't max out one stat while others are low
2. **Play Wisely**: Playing gives most XP but costs energy and hunger
3. **Watch Mood**: Low hunger/energy/cleanliness will tank mood
4. **Level Up Fast**: Keep all stats high for passive XP gain
5. **Offline Progress**: Game continues for up to 1 hour when closed

## 💾 Save Location

Your save file is stored at:

- **Linux/Mac**: `~/.macan_ternak/savegame.json`
- **Windows**: `C:\Users\YourName\.macan_ternak\savegame.json`

## 🎨 Next Steps

Once you're comfortable:

1. Read the full README.md for architecture details
2. Try modifying decay rates in `logic/tiger_pet.py`
3. Change UI colors in `ui/control_panel.py` and `ui/stats_panel.py`
4. Add new actions by extending the TigerPet class
5. Import 3D models to replace the placeholder cube tiger

## 🆘 Need Help?

Common issues and solutions:

**Q: The tiger looks blocky**  
A: That's the placeholder! Replace `_draw_tiger()` in `engine3d/viewport.py` with your own 3D model

**Q: Stats decay too fast**  
A: Adjust decay rates in `logic/tiger_pet.py` __init__ method

**Q: Can't interact with buttons**  
A: Make sure the game isn't paused (it auto-pauses on certain errors)

**Q: Want to reset progress**  
A: Delete the save file at `~/.macan_ternak/savegame.json`

## 🎉 You're Ready!

Enjoy raising your virtual tiger! The modular architecture makes it easy to add:
- New pet types
- Additional actions
- Inventory systems
- Mini-games
- And much more!

Happy coding! 🐯
