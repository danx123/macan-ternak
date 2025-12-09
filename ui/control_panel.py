"""
Left control panel with action buttons
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QPushButton, QGroupBox, QSpacerItem, 
                               QSizePolicy)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

class ControlPanel(QWidget):
    """Control panel with pet interaction buttons"""
    
    # Signals
    feed_clicked = Signal()
    clean_clicked = Signal()
    sleep_clicked = Signal()
    play_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        """Create control panel UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🐯 Controls")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Action buttons group
        actions_group = QGroupBox("Pet Actions")
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setSpacing(10)
        
        # Feed button
        self.feed_btn = QPushButton("🍖 Feed Tiger")
        self.feed_btn.setMinimumHeight(50)
        self.feed_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.feed_btn.clicked.connect(self.feed_clicked.emit)
        actions_layout.addWidget(self.feed_btn)
        
        # Clean button
        self.clean_btn = QPushButton("🛁 Clean Tiger")
        self.clean_btn.setMinimumHeight(50)
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6bc2;
            }
        """)
        self.clean_btn.clicked.connect(self.clean_clicked.emit)
        actions_layout.addWidget(self.clean_btn)
        
        # Sleep button
        self.sleep_btn = QPushButton("😴 Let Sleep")
        self.sleep_btn.setMinimumHeight(50)
        self.sleep_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e24aa;
            }
            QPushButton:pressed {
                background-color: #7b1fa2;
            }
        """)
        self.sleep_btn.clicked.connect(self.sleep_clicked.emit)
        actions_layout.addWidget(self.sleep_btn)
        
        # Play button
        self.play_btn = QPushButton("🎾 Play")
        self.play_btn.setMinimumHeight(50)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:pressed {
                background-color: #e65100;
            }
        """)
        self.play_btn.clicked.connect(self.play_clicked.emit)
        actions_layout.addWidget(self.play_btn)
        
        layout.addWidget(actions_group)
        
        # Info section
        info_group = QGroupBox("Instructions")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel(
            "• Feed when hungry\n"
            "• Clean when dirty\n"
            "• Sleep when tired\n"
            "• Play to boost mood\n\n"
            "Keep all stats high\n"
            "to level up faster!"
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("font-size: 12px; color: #666;")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))