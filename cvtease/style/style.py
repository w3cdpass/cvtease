from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

ICON_PATH = "cvtease/asset/laugh.ico"
def apply_window_icon(window):
    icon = QIcon(ICON_PATH)
    window.setWindowIcon(icon)
    
def apply_app_icon(app):
    icon = QIcon(ICON_PATH)
    app.setWindowIcon(icon)
    app.setWindowIcon(icon)
# Window Style
WINDOW_TITLE = "Face Detection App"
WINDOW_GEOMETRY = (100, 100, 800, 600)

# Label Styles
IMAGE_LABEL_ALIGNMENT = Qt.AlignCenter

DEV_LABEL_STYLE = """
    This tool is under development, be patience
"""

# Button Styles
BUTTON_STYLE = """
    QPushButton {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        margin: 10px;
    }
    QPushButton:hover {
        background-color: #0056b3;
    }
    QPushButton:pressed {
        background-color: #004080;
    }
"""

# Slider Settings
SLIDER_RANGE = (0, 100)
SLIDER_DEFAULT_VALUE = 50
SLIDER_TICK_INTERVAL = 10
SLIDER_TICK_POSITION = Qt.Horizontal

# Slider Style
SLIDER_STYLE = """
    QSlider::groove:horizontal {
        border: 1px solid #999999;
        height: 8px;
        background: #cccccc;
        margin: 2px 0;
    }
    QSlider::handle:horizontal {
        background: #007BFF;
        border: 1px solid #007BFF;
        width: 18px;
        margin: -2px 0;
        border-radius: 3px;
    }
"""

# ComboBox Items
COMBO_BOX_ITEMS = ["Tesselation", "Contours", "Iris"]

# ComboBox Style
COMBO_BOX_STYLE = """
    QComboBox {
        padding: 5px;
        margin: 10px;
        border: 1px solid #007BFF;
        border-radius: 5px;
    }
    QComboBox::drop-down {
        border: 0px;
    }
    QComboBox QAbstractItemView {
        border: 1px solid #007BFF;
        selection-background-color: #007BFF;
    }
"""
# Add this to your style.py

ROUND_BUTTON_STYLE = """
QPushButton {
    font-size: 18px;
    text-align: center;
    
    background-color: #5A9;
    color: white;
    padding: 10px;
    border-radius: 20px; /* Half of width/height */
    min-width: 25px;
    min-height: 25px;
}
QPushButton:hover {
    background-color: #7AB;
}
QPushButton:pressed {
    background-color: #489;
}
"""
