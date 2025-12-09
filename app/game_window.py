"""
Main game window that orchestrates all components
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from ui.control_panel import ControlPanel
from ui.stats_panel import StatsPanel
from engine3d.viewport import Viewport3D
from logic.game_manager import GameManager
from services.save_manager import SaveManager

class GameWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macan Ternak - 3D Pet Simulator")
        self.setMinimumSize(1200, 700)
        
        # Initialize managers
        self.save_manager = SaveManager()
        self.game_manager = GameManager(self.save_manager)
        
        # Setup UI
        self._setup_ui()
        
        # Load saved game or start new
        self.game_manager.load_game()
        
        # Setup game loop timer
        self._setup_game_loop()
        
        # Initial UI update
        self._update_ui()
        
    def _setup_ui(self):
        """Create and arrange all UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left control panel
        self.control_panel = ControlPanel()
        self.control_panel.setFixedWidth(250)
        main_layout.addWidget(self.control_panel)
        
        # Center 3D viewport
        self.viewport = Viewport3D(self.game_manager)
        main_layout.addWidget(self.viewport, stretch=1)
        
        # Right stats panel
        self.stats_panel = StatsPanel()
        self.stats_panel.setFixedWidth(250)
        main_layout.addWidget(self.stats_panel)
        
        # Connect signals
        self._connect_signals()
        
    def _connect_signals(self):
        """Connect UI signals to game logic"""
        self.control_panel.feed_clicked.connect(self._on_feed)
        self.control_panel.clean_clicked.connect(self._on_clean)
        self.control_panel.sleep_clicked.connect(self._on_sleep)
        self.control_panel.play_clicked.connect(self._on_play)
        
    def _setup_game_loop(self):
        """Setup main game update loop"""
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self._game_update)
        self.game_timer.start(1000)  # Update every second
        
    def _game_update(self):
        """Called every game tick"""
        self.game_manager.update()
        self._update_ui()
        self.viewport.update_scene()
        
    def _update_ui(self):
        """Update all UI elements with current game state"""
        pet = self.game_manager.pet
        self.stats_panel.update_stats(
            hunger=pet.hunger,
            energy=pet.energy,
            mood=pet.mood,
            cleanliness=pet.cleanliness,
            level=pet.level,
            exp=pet.exp,
            exp_to_next=pet.exp_to_next_level
        )
        
    def _on_feed(self):
        """Handle feed action"""
        success, message = self.game_manager.feed_pet()
        self.stats_panel.show_notification(message, success)
        
    def _on_clean(self):
        """Handle clean action"""
        success, message = self.game_manager.clean_pet()
        self.stats_panel.show_notification(message, success)
        
    def _on_sleep(self):
        """Handle sleep action"""
        success, message = self.game_manager.sleep_pet()
        self.stats_panel.show_notification(message, success)
        
    def _on_play(self):
        """Handle play action"""
        success, message = self.game_manager.play_with_pet()
        self.stats_panel.show_notification(message, success)
        
    def closeEvent(self, event):
        """Save game before closing"""
        self.game_manager.save_game()
        event.accept()