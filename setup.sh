#!/bin/bash
# Quick setup script for Macan Ternak

echo "🐯 Setting up Macan Ternak - 3D Pet Simulator"
echo "=============================================="
echo ""

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p app ui engine3d logic services assets/models assets/textures assets/sounds assets/music

# Create __init__.py files
echo "📝 Creating package files..."

cat > app/__init__.py << 'EOF'
"""App package - Main application window and core"""
from .game_window import GameWindow
__all__ = ['GameWindow']
EOF

cat > ui/__init__.py << 'EOF'
"""UI package - User interface widgets and panels"""
from .control_panel import ControlPanel
from .stats_panel import StatsPanel
__all__ = ['ControlPanel', 'StatsPanel']
EOF

cat > engine3d/__init__.py << 'EOF'
"""Engine3D package - 3D rendering and scene management"""
from .viewport import Viewport3D
__all__ = ['Viewport3D']
EOF

cat > logic/__init__.py << 'EOF'
"""Logic package - Game logic and pet mechanics"""
from .tiger_pet import TigerPet, PetState
from .game_manager import GameManager
__all__ = ['TigerPet', 'PetState', 'GameManager']
EOF

cat > services/__init__.py << 'EOF'
"""Services package - Save system and settings"""
from .save_manager import SaveManager
from .settings_manager import SettingsManager
__all__ = ['SaveManager', 'SettingsManager']
EOF

cat > assets/README.txt << 'EOF'
This folder is for game assets:

- models/     - 3D models (.obj, .fbx)
- textures/   - Image files for texturing
- sounds/     - Sound effects (.wav, .mp3)
- music/      - Background music

Currently, the game uses procedurally generated placeholder graphics.
Add your own assets here to replace them!
EOF

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the game:"
echo "  python main.py"
echo ""
echo "Have fun with your virtual tiger! 🐯"