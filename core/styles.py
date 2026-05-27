
PRIMARY_BG = "#FFFFFF"
SECONDARY_BG = "#7FFF00"
ACCENT = "#00FA9A"

DISCOUNT_HIGHLIGHT_BG = "#2E8B57"
OUT_OF_STOCK_BG = "#ADD8E6"

FONT_FAMILY = "Times New Roman"
FONT_SIZE = 12

APP_QSS = f"""
* {{
    font-family: "{FONT_FAMILY}";
    font-size: {FONT_SIZE}pt;
}}
QMainWindow, QDialog, QWidget#central {{
    background-color: {PRIMARY_BG};
}}
QPushButton {{
    background-color: {SECONDARY_BG};
    border: 1px solid #4d9900;
    padding: 6px 14px;
    border-radius: 4px;
}}
QPushButton:hover {{
    background-color: {ACCENT};
}}
QPushButton:disabled {{
    background-color: #d0d0d0;
    color: #777;
}}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QPlainTextEdit, QTextEdit {{
    background-color: {PRIMARY_BG};
    border: 1px solid #999;
    padding: 4px;
    border-radius: 3px;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
QDoubleSpinBox:focus, QPlainTextEdit:focus {{
    border: 1px solid {ACCENT};
}}
QComboBox::drop-down {{
    width: 22px;
    border-left: 1px solid #cfcfcf;
    background-color: {PRIMARY_BG};
}}
QComboBox QAbstractItemView {{
    background-color: {PRIMARY_BG};
    border: 1px solid #999;
    selection-background-color: {ACCENT};
    selection-color: #000;
    outline: 0;
    padding: 2px;
}}
QComboBox QAbstractItemView::item {{
    min-height: 24px;
    padding: 4px 8px;
    color: #000;
    background-color: {PRIMARY_BG};
}}
QComboBox QAbstractItemView::item:selected,
QComboBox QAbstractItemView::item:hover {{
    background-color: {SECONDARY_BG};
    color: #000;
}}
QLabel#header {{
    font-weight: bold;
    font-size: 16pt;
}}
QFrame#card {{
    border: 1px solid #cfcfcf;
    border-radius: 6px;
    background-color: {PRIMARY_BG};
    margin: 4px;
}}
QFrame#card[discountHighlight="true"] {{
    background-color: {DISCOUNT_HIGHLIGHT_BG};
    color: white;
}}
QFrame#card[discountHighlight="true"] QLabel {{
    color: white;
}}
QFrame#card[outOfStock="true"] {{
    background-color: {OUT_OF_STOCK_BG};
}}
"""
