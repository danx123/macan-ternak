"""
Left control panel with improved UI
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QPushButton, QGroupBox, QSpacerItem, 
                               QSizePolicy)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

class ControlPanel(QWidget):
    
    feed_clicked = Signal()
    clean_clicked = Signal()
    sleep_clicked = Signal()
    play_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🕹️ Actions")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Action buttons group
        actions_group = QGroupBox()
        actions_group.setStyleSheet("""
            QGroupBox {
                border: none;
            }
        """)
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setSpacing(12)
        
        # Helper to create styled buttons
        def create_btn(text, color, hover_color, signal):
            btn = QPushButton(text)
            btn.setMinimumHeight(55)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 20px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                    margin-left: 2px;
                }}
                QPushButton:pressed {{
                    background-color: {color};
                    margin-top: 2px;
                }}
            """)
            btn.clicked.connect(signal.emit)
            return btn
        
        # Buttons with Material Colors
        self.feed_btn = create_btn("🍖  Feed", "#4CAF50", "#45a049", self.feed_clicked)
        actions_layout.addWidget(self.feed_btn)
        
        self.clean_btn = create_btn("🛁  Clean", "#2196F3", "#1976D2", self.clean_clicked)
        actions_layout.addWidget(self.clean_btn)
        
        self.sleep_btn = create_btn("😴  Sleep", "#9C27B0", "#7B1FA2", self.sleep_clicked)
        actions_layout.addWidget(self.sleep_btn)
        
        self.play_btn = create_btn("🎾  Play", "#FF9800", "#F57C00", self.play_clicked)
        actions_layout.addWidget(self.play_btn)
        
        layout.addWidget(actions_group)
        
        # Info Box
        info_box = QLabel(
            "💡 <b>Tips:</b><br>"
            "Keep your tiger happy to earn more coins! "
            "Use coins in the shop."
        )
        info_box.setWordWrap(True)
        info_box.setStyleSheet("""
            background-color: #ECEFF1;
            border-radius: 8px;
            padding: 10px;
            color: #455A64;
            font-size: 12px;
        """)
        layout.addWidget(info_box)
        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))