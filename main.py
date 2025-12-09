"""
Macan Ternak - 3D Pet Simulator
Entry point for the application
"""
import sys
from PySide6.QtWidgets import QApplication
from app.game_window import GameWindow

def main():
    """Initialize and run the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Macan Ternak")
    app.setOrganizationName("MacanAngkasa")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = GameWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()