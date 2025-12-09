"""
Right stats panel with modern UI
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QProgressBar, QGroupBox, QSpacerItem,
                               QSizePolicy, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont

class StatsPanel(QWidget):
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📊 Status")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Level Badge
        self.level_container = QWidget()
        self.level_container.setStyleSheet("""
            background-color: #673AB7;
            border-radius: 10px;
        """)
        lvl_layout = QVBoxLayout(self.level_container)
        self.level_label = QLabel("LEVEL 1")
        self.level_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        self.level_label.setAlignment(Qt.AlignCenter)
        lvl_layout.addWidget(self.level_label)
        
        self.exp_label = QLabel("0 / 100 XP")
        self.exp_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 11px;")
        self.exp_label.setAlignment(Qt.AlignCenter)
        lvl_layout.addWidget(self.exp_label)
        
        layout.addWidget(self.level_container)
        
        # Stats Group
        stats_group = QGroupBox()
        stats_group.setStyleSheet("border: none;")
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(15)
        
        def create_stat(label_text, color):
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-weight: bold; color: #555;")
            bar = QProgressBar()
            bar.setFixedHeight(12)
            bar.setTextVisible(False)
            bar.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    background-color: #E0E0E0;
                    border-radius: 6px;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 6px;
                }}
            """)
            stats_layout.addWidget(lbl)
            stats_layout.addWidget(bar)
            return bar
            
        self.hunger_bar = create_stat("🍖 Hunger", "#4CAF50")
        self.energy_bar = create_stat("⚡ Energy", "#9C27B0")
        self.mood_bar = create_stat("😊 Mood", "#FF9800")
        self.clean_bar = create_stat("✨ Hygiene", "#2196F3")
        
        layout.addWidget(stats_group)
        
        # Notification Bubble
        self.notification_label = QLabel("")
        self.notification_label.setAlignment(Qt.AlignCenter)
        self.notification_label.setWordWrap(True)
        self.notification_label.setStyleSheet("""
            background-color: #333;
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-size: 12px;
            margin-top: 10px;
        """)
        self.notification_label.hide()
        layout.addWidget(self.notification_label)
        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
    def update_stats(self, hunger, energy, mood, cleanliness, level, exp, exp_to_next):
        """Update stat visuals"""
        self.hunger_bar.setValue(int(hunger))
        self.energy_bar.setValue(int(energy))
        self.mood_bar.setValue(int(mood))
        self.clean_bar.setValue(int(cleanliness))
        
        self.level_label.setText(f"LEVEL {level}")
        self.exp_label.setText(f"{int(exp)} / {int(exp_to_next)} XP")
        
    def show_notification(self, message, success=True):
        color = "#2E7D32" if success else "#C62828"
        self.notification_label.setStyleSheet(f"""
            background-color: {color};
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
        """)
        self.notification_label.setText(message)
        self.notification_label.show()
        
        effect = QGraphicsOpacityEffect(self.notification_label)
        self.notification_label.setGraphicsEffect(effect)
        
        self.fade_animation = QPropertyAnimation(effect, b"opacity")
        self.fade_animation.setDuration(2500)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InQuad)
        self.fade_animation.finished.connect(self.notification_label.hide)
        self.fade_animation.start()