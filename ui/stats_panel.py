"""
Right stats panel showing pet status
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QProgressBar, QGroupBox, QSpacerItem,
                               QSizePolicy, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont

class StatsPanel(QWidget):
    """Stats panel displaying pet attributes"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        """Create stats panel UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📊 Stats")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Level info
        level_group = QGroupBox("Level & Experience")
        level_layout = QVBoxLayout(level_group)
        
        self.level_label = QLabel("Level: 1")
        self.level_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        level_layout.addWidget(self.level_label)
        
        self.exp_bar = self._create_progress_bar("#FFD700")
        level_layout.addWidget(self.exp_bar)
        
        self.exp_label = QLabel("0 / 100 XP")
        self.exp_label.setStyleSheet("font-size: 11px; color: #666;")
        level_layout.addWidget(self.exp_label)
        
        layout.addWidget(level_group)
        
        # Stats group
        stats_group = QGroupBox("Vital Stats")
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(12)
        
        # Hunger
        hunger_label = QLabel("🍖 Hunger")
        stats_layout.addWidget(hunger_label)
        self.hunger_bar = self._create_progress_bar("#4CAF50")
        stats_layout.addWidget(self.hunger_bar)
        
        # Energy
        energy_label = QLabel("⚡ Energy")
        stats_layout.addWidget(energy_label)
        self.energy_bar = self._create_progress_bar("#9C27B0")
        stats_layout.addWidget(self.energy_bar)
        
        # Mood
        mood_label = QLabel("😊 Mood")
        stats_layout.addWidget(mood_label)
        self.mood_bar = self._create_progress_bar("#FF9800")
        stats_layout.addWidget(self.mood_bar)
        
        # Cleanliness
        clean_label = QLabel("✨ Cleanliness")
        stats_layout.addWidget(clean_label)
        self.clean_bar = self._create_progress_bar("#2196F3")
        stats_layout.addWidget(self.clean_bar)
        
        layout.addWidget(stats_group)
        
        # Notification label
        self.notification_label = QLabel("")
        self.notification_label.setAlignment(Qt.AlignCenter)
        self.notification_label.setWordWrap(True)
        self.notification_label.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.notification_label.hide()
        layout.addWidget(self.notification_label)
        
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
    def _create_progress_bar(self, color):
        """Create a styled progress bar"""
        bar = QProgressBar()
        bar.setMinimum(0)
        bar.setMaximum(100)
        bar.setValue(100)
        bar.setTextVisible(True)
        bar.setFormat("%v%")
        bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        return bar
        
    def update_stats(self, hunger, energy, mood, cleanliness, level, exp, exp_to_next):
        """Update all stat displays"""
        self.hunger_bar.setValue(int(hunger))
        self.energy_bar.setValue(int(energy))
        self.mood_bar.setValue(int(mood))
        self.clean_bar.setValue(int(cleanliness))
        self.level_label.setText(f"Level: {level}")
        self.exp_bar.setValue(int((exp / exp_to_next) * 100))
        self.exp_label.setText(f"{int(exp)} / {int(exp_to_next)} XP")
        
        # Update bar colors based on values
        self._update_bar_color(self.hunger_bar, hunger, "#4CAF50")
        self._update_bar_color(self.energy_bar, energy, "#9C27B0")
        self._update_bar_color(self.mood_bar, mood, "#FF9800")
        self._update_bar_color(self.clean_bar, cleanliness, "#2196F3")
        
    def _update_bar_color(self, bar, value, normal_color):
        """Change bar color based on value"""
        if value < 20:
            color = "#F44336"  # Red for critical
        elif value < 40:
            color = "#FF9800"  # Orange for low
        else:
            color = normal_color
            
        bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        
    def show_notification(self, message, success=True):
        """Show a temporary notification"""
        color = "#4CAF50" if success else "#F44336"
        self.notification_label.setStyleSheet(f"""
            background-color: {color};
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.notification_label.setText(message)
        self.notification_label.show()
        
        # Fade out animation
        effect = QGraphicsOpacityEffect(self.notification_label)
        self.notification_label.setGraphicsEffect(effect)
        
        self.fade_animation = QPropertyAnimation(effect, b"opacity")
        self.fade_animation.setDuration(2000)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.finished.connect(self.notification_label.hide)
        self.fade_animation.start()