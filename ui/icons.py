"""
Iconos de Phosphor Icons para NutriSmart.
Uso:
    from ui.icons import Ph, icono_label
    icon = icono_label(Ph.FIRE, size=18, color="#f39c12")
"""
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Ph:
    """Codepoints del font Phosphor Icons (Regular)."""
    FIRE        = chr(0xe242)
    STAR        = chr(0xe46a)
    TROPHY      = chr(0xe67e)
    MEDAL       = chr(0xe320)
    FORK_KNIFE  = chr(0xe262)
    USER        = chr(0xe4c2)
    CHART_BAR   = chr(0xe150)
    HEART       = chr(0xe2a8)
    CHECK       = chr(0xe182)
    APPLE       = chr(0xe516)
    BOWL        = chr(0xeaa4)
    BARBELL     = chr(0xe0b6)
    CLOCK       = chr(0xe19a)
    LIGHTNING   = chr(0xe2de)
    ARROW_RIGHT = chr(0xe06c)
    HOUSE       = chr(0xe2c2)
    LIST        = chr(0xe2f0)
    GEAR        = chr(0xe270)
    SIGN_OUT    = chr(0xe42a)
    PLUS        = chr(0xe3d4)
    TRASH       = chr(0xe4a6)
    X           = chr(0xe4f6)
    LEAF        = chr(0xe2d6)
    PERSON      = chr(0xe3c2)
    CALENDAR    = chr(0xe124)
    DROP        = chr(0xe210)
    SCALES      = chr(0xe406)
    CHEF_HAT    = chr(0xe18a)


# Mapping de strings de la DB → codepoints Phosphor
ICON_MAP = {
    'star':    Ph.STAR,
    'fire':    Ph.FIRE,
    'trophy':  Ph.TROPHY,
    'medal':   Ph.MEDAL,
    'chef':    Ph.CHEF_HAT,
    'heart':   Ph.HEART,
    'barbell': Ph.BARBELL,
    'leaf':    Ph.LEAF,
    'check':   Ph.CHECK,
}


def resolver_icono(nombre_icono: str) -> str:
    """Convierte un nombre de ícono (de la DB) al codepoint Phosphor correspondiente."""
    return ICON_MAP.get(nombre_icono, Ph.STAR)


def icono_label(codepoint: str, size: int = 16, color: str = None, parent=None) -> QLabel:
    """
    Crea un QLabel con un icono de Phosphor.

    Args:
        codepoint: Caracter del icono (usar constantes de Ph)
        size: Tamaño del font en puntos
        color: Color CSS (ej: '#2d6a2d'). Si None, hereda del padre.
        parent: Widget padre opcional
    Returns:
        QLabel listo para insertar en un layout
    """
    label = QLabel(codepoint, parent)
    label.setFont(QFont('Phosphor', size))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    style = "background-color: transparent;"
    if color:
        style += f" color: {color};"
    label.setStyleSheet(style)
    return label

