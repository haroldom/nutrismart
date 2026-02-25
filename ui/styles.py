"""
Estilos QSS globales para NutriSmart con PyQt6.
"""

class Colores:
    """Paleta de colores de la aplicación."""
    PRIMARIO = '#2e7d32'
    PRIMARIO_OSCURO = '#1b5e20'
    PRIMARIO_CLARO = '#4caf50'
    SECUNDARIO = '#3498db'
    SECUNDARIO_OSCURO = '#2980b9'
    FONDO = '#f5f5f5'
    FONDO_CARD = '#ffffff'
    TEXTO = '#333333'
    TEXTO_SECUNDARIO = '#666666'
    TEXTO_CLARO = '#999999'
    EXITO = '#27ae60'
    ADVERTENCIA = '#f39c12'
    ERROR = '#e74c3c'
    BORDE = '#e0e0e0'


GLOBAL_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

/* Labels */
QLabel {
    color: #333333;
    background-color: transparent;
}

QLabel#titulo {
    font-size: 24px;
    font-weight: bold;
    color: #333333;
}

QLabel#subtitulo {
    font-size: 16px;
    font-weight: bold;
    color: #333333;
}

QLabel#texto-secundario {
    color: #666666;
    font-size: 12px;
}

/* Line Edits */
QLineEdit {
    padding: 12px 15px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    background-color: white;
    color: #333333;
    font-size: 14px;
}

QLineEdit:focus {
    border: 2px solid #2e7d32;
    padding: 11px 14px;
}

QLineEdit:hover {
    border-color: #bdbdbd;
}

/* Combo Box */
QComboBox {
    padding: 12px 15px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    background-color: white;
    color: #333333;
    font-size: 14px;
    min-width: 150px;
}

QComboBox:focus {
    border: 2px solid #2e7d32;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #e0e0e0;
    selection-background-color: #e8f5e9;
    selection-color: #2e7d32;
}

/* Spin Box */
QSpinBox, QDoubleSpinBox {
    padding: 12px 15px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    background-color: white;
    color: #333333;
    font-size: 14px;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #2e7d32;
}

/* Push Buttons */
QPushButton {
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#primario {
    background-color: #2e7d32;
    color: white;
}

QPushButton#primario:hover {
    background-color: #1b5e20;
}

QPushButton#primario:pressed {
    background-color: #0d3d10;
}

QPushButton#secundario {
    background-color: transparent;
    border: 2px solid #2e7d32;
    color: #2e7d32;
}

QPushButton#secundario:hover {
    background-color: #e8f5e9;
}

QPushButton#peligro {
    background-color: #e74c3c;
    color: white;
}

QPushButton#peligro:hover {
    background-color: #c0392b;
}

QPushButton#small {
    padding: 8px 16px;
    font-size: 12px;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background-color: #f5f5f5;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #c0c0c0;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a0a0a0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* Cards */
QFrame#card {
    background-color: white;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}

QFrame#card:hover {
    border-color: #bdbdbd;
}

/* Navigation */
QFrame#nav-item {
    background-color: white;
    border: none;
    padding: 12px 20px;
}

QFrame#nav-item:hover {
    background-color: #f0f0f0;
}

QFrame#nav-item-active {
    background-color: #e8f5e9;
    border-left: 4px solid #2e7d32;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #e0e0e0;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    border-radius: 4px;
    background-color: #2e7d32;
}

/* Tab Widget */
QTabWidget::pane {
    border: none;
    background-color: white;
}

QTabBar::tab {
    padding: 10px 20px;
    background-color: #f5f5f5;
    border: none;
    color: #666666;
}

QTabBar::tab:selected {
    background-color: white;
    color: #2e7d32;
    border-bottom: 3px solid #2e7d32;
}

QTabBar::tab:hover:!selected {
    background-color: #e8e8e8;
}

/* Text Edit */
QTextEdit {
    padding: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    background-color: white;
    color: #333333;
    font-size: 14px;
}

QTextEdit:focus {
    border: 2px solid #2e7d32;
}

/* Message Box */
QMessageBox {
    background-color: white;
}

QMessageBox QLabel {
    color: #333333;
}

/* Tool Tip */
QToolTip {
    background-color: #333333;
    color: white;
    border: none;
    padding: 8px;
    border-radius: 4px;
}
"""

# Estilos específicos para componentes
NAV_STYLE = """
QFrame#sidebar {
    background-color: white;
    border-right: 1px solid #e0e0e0;
}

QLabel#logo {
    font-size: 20px;
    font-weight: bold;
    color: #2e7d32;
    padding: 20px;
}

QLabel#user-name {
    font-size: 14px;
    font-weight: bold;
    color: #333333;
}

QLabel#user-email {
    font-size: 12px;
    color: #666666;
}
"""

CARD_STAT_STYLE = """
QFrame#stat-card {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
}

QLabel#stat-value {
    font-size: 28px;
    font-weight: bold;
}

QLabel#stat-label {
    font-size: 12px;
    color: #666666;
}

QLabel#stat-icon {
    font-size: 24px;
}
"""

RECIPE_CARD_STYLE = """
QFrame#recipe-card {
    background-color: white;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}

QFrame#recipe-card:hover {
    border-color: #2e7d32;
}

QLabel#recipe-name {
    font-size: 16px;
    font-weight: bold;
    color: #333333;
}

QLabel#recipe-info {
    font-size: 12px;
    color: #666666;
}

QLabel#recipe-type {
    font-size: 10px;
    font-weight: bold;
    padding: 4px 8px;
    border-radius: 4px;
}
"""

LOGIN_STYLE = """
QFrame#login-container {
    background-color: white;
    border-radius: 15px;
}

QLabel#login-title {
    font-size: 28px;
    font-weight: bold;
    color: #2e7d32;
}

QLabel#login-subtitle {
    font-size: 14px;
    color: #666666;
}
"""
