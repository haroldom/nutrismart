"""
Componentes reutilizables de UI para NutriSmart con PyQt6.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QProgressBar, QGraphicsDropShadowEffect,
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QCursor

from ui.styles import Colores
from ui.icons import resolver_icono, Ph


class BotonPrimario(QPushButton):
    """Botón primario estilizado."""

    def __init__(self, texto, parent=None):
        super().__init__(texto, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(45)
        self.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colores.PRIMARIO};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
            }}
            QPushButton:hover {{
                background-color: {Colores.PRIMARIO_OSCURO};
            }}
            QPushButton:pressed {{
                background-color: #0d3d10;
            }}
        """)


class BotonSecundario(QPushButton):
    """Botón secundario (outline)."""

    def __init__(self, texto, parent=None):
        super().__init__(texto, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(45)
        self.setFont(QFont('Inter', 11))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colores.PRIMARIO};
                border: 2px solid {Colores.PRIMARIO};
                border-radius: 6px;
                padding: 12px 24px;
            }}
            QPushButton:hover {{
                background-color: #e8f5e9;
            }}
        """)


class BotonPeligro(QPushButton):
    """Botón de acción peligrosa."""

    def __init__(self, texto, parent=None):
        super().__init__(texto, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(45)
        self.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colores.ERROR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)


class BotonSmall(QPushButton):
    """Botón pequeño."""

    def __init__(self, texto, color=None, parent=None):
        super().__init__(texto, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFont(QFont('Inter', 10))

        if color:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }}
                QPushButton:hover {{
                    background-color: {self._oscurecer_color(color)};
                }}
            """)
        else:
            self.setObjectName("small")

    def _oscurecer_color(self, color):
        """Oscurece un color hex."""
        c = QColor(color)
        return c.darker(120).name()


class Card(QFrame):
    """Contenedor tipo tarjeta con sombra."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet("""
            QFrame#card {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)

        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)


class StatCard(Card):
    """Tarjeta para mostrar una estadística."""

    def __init__(self, titulo, valor, unidad='', icono='', color=None, parent=None):
        super().__init__(parent)

        if color is None:
            color = Colores.PRIMARIO

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        # Header con icono y título
        header = QHBoxLayout()
        header.setSpacing(8)

        if icono:
            icono_label = QLabel(icono)
            icono_label.setFont(QFont('Phosphor', 18))
            icono_label.setStyleSheet(f"color: {color}; background-color: transparent;")
            header.addWidget(icono_label)

        titulo_label = QLabel(titulo)
        titulo_label.setFont(QFont('Inter', 11))
        titulo_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent")
        header.addWidget(titulo_label)
        header.addStretch()

        layout.addLayout(header)

        # Valor
        valor_layout = QHBoxLayout()
        valor_layout.setSpacing(5)

        if isinstance(valor, float):
            valor_str = str(int(valor)) if valor == int(valor) else str(round(valor, 1))
        else:
            valor_str = str(valor)
        self.valor_label = QLabel(valor_str)
        self.valor_label.setFont(QFont('Inter', 28, QFont.Weight.Bold))
        self.valor_label.setStyleSheet(f"color: {color}; background-color: transparent")
        valor_layout.addWidget(self.valor_label)

        if unidad:
            unidad_label = QLabel(unidad)
            unidad_label.setFont(QFont('Inter', 12))
            unidad_label.setStyleSheet(f"color: {Colores.TEXTO_CLARO}; background-color: transparent")
            unidad_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
            valor_layout.addWidget(unidad_label)

        valor_layout.addStretch()
        layout.addLayout(valor_layout)

    def set_valor(self, valor):
        """Actualiza el valor mostrado."""
        self.valor_label.setText(str(valor))


class MacroCard(Card):
    """Tarjeta para mostrar un macronutriente."""

    def __init__(self, nombre, gramos, porcentaje, color, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)

        # Barra de color superior
        color_bar = QFrame()
        color_bar.setFixedHeight(4)
        color_bar.setFrameShape(QFrame.Shape.NoFrame)
        color_bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
        layout.addWidget(color_bar)

        # Nombre
        nombre_label = QLabel(nombre)
        nombre_label.setFont(QFont('Inter', 11))
        nombre_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent")
        layout.addWidget(nombre_label)

        # Gramos
        self.gramos_label = QLabel(f"{gramos}g")
        self.gramos_label.setFont(QFont('Inter', 22, QFont.Weight.Bold))
        self.gramos_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        layout.addWidget(self.gramos_label)

        # Porcentaje
        pct_label = QLabel(f"{porcentaje}%")
        pct_label.setFont(QFont('Inter', 10))
        pct_label.setStyleSheet(f"color: {color}; background-color: transparent")
        layout.addWidget(pct_label)


class ProgressBarCustom(QProgressBar):
    """Barra de progreso personalizada."""

    def __init__(self, color=None, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setFixedHeight(8)

        if color is None:
            color = Colores.PRIMARIO

        self.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: #e0e0e0;
            }}
            QProgressBar::chunk {{
                border-radius: 4px;
                background-color: {color};
            }}
        """)


class NavItem(QFrame):
    """Item de navegación para el menú lateral."""

    clicked = pyqtSignal()

    def __init__(self, texto, icono, activo=False, parent=None):
        super().__init__(parent)
        self.texto = texto
        self.activo = activo

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(50)
        self.setFrameShape(QFrame.Shape.NoFrame)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 15, 0)
        layout.setSpacing(0)

        # Indicador lateral
        self.indicador = QFrame()
        self.indicador.setFixedWidth(4)
        self.indicador.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(self.indicador)

        # Contenido
        contenido = QHBoxLayout()
        contenido.setContentsMargins(15, 0, 0, 0)
        contenido.setSpacing(12)

        self.icono_label = QLabel(icono)
        self.icono_label.setFont(QFont('Phosphor', 16))
        contenido.addWidget(self.icono_label)

        self.texto_label = QLabel(texto)
        self.texto_label.setFont(QFont('Inter', 12))
        contenido.addWidget(self.texto_label)
        contenido.addStretch()

        layout.addLayout(contenido)

        self._actualizar_estilo()

    def _actualizar_estilo(self):
        """Actualiza el estilo según el estado activo."""
        if self.activo:
            self.setStyleSheet(f"background-color: #e8f5e9; border: none;")
            self.indicador.setStyleSheet(f"background-color: {Colores.PRIMARIO};")
            self.icono_label.setStyleSheet(f"color: {Colores.PRIMARIO}; background-color: transparent")
            self.texto_label.setStyleSheet(f"color: {Colores.PRIMARIO}; font-weight: bold; background-color: transparent")
        else:
            self.setStyleSheet("background-color: transparent; border: none;")
            self.indicador.setStyleSheet("background-color: transparent;")
            self.icono_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent")
            self.texto_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")

    def set_activo(self, activo):
        """Establece el estado activo."""
        self.activo = activo
        self._actualizar_estilo()

    def enterEvent(self, event):
        """Hover enter."""
        if not self.activo:
            self.setStyleSheet("background-color: #f5f5f5; border: none;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Hover leave."""
        self._actualizar_estilo()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Click handler."""
        self.clicked.emit()
        super().mousePressEvent(event)


class ComidaCard(Card):
    """Tarjeta para mostrar una comida/receta."""

    clicked = pyqtSignal(dict)
    add_clicked = pyqtSignal(dict)

    def __init__(self, comida, mostrar_add=True, parent=None):
        super().__init__(parent)
        self.comida = comida
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)

        # Indicador de tipo
        tipo_colors = {
            'desayuno': '#f39c12',
            'almuerzo': '#e74c3c',
            'cena': '#3498db',
            'snack': '#9b59b6'
        }
        tipo_color = tipo_colors.get(comida.get('tipo', ''), Colores.TEXTO_SECUNDARIO)

        indicador = QFrame()
        indicador.setFixedWidth(4)
        indicador.setFrameShape(QFrame.Shape.NoFrame)
        indicador.setStyleSheet(f"background-color: {tipo_color}; border-radius: 2px;")
        layout.addWidget(indicador)

        # Contenido principal
        contenido = QVBoxLayout()
        contenido.setSpacing(4)

        # Nombre
        nombre = QLabel(comida['nombre'])
        nombre.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        nombre.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        contenido.addWidget(nombre)

        # Info nutricional
        info = f"{comida['calorias']} kcal  |  P: {comida['proteinas']}g  |  C: {comida['carbs']}g  |  G: {comida['grasas']}g"
        info_label = QLabel(info)
        info_label.setFont(QFont('Inter', 10))
        info_label.setStyleSheet(f"color: {Colores.TEXTO_CLARO}; background-color: transparent")
        contenido.addWidget(info_label)

        # Tipo
        tipo_label = QLabel(comida.get('tipo', '').upper())
        tipo_label.setFont(QFont('Inter', 9, QFont.Weight.Bold))
        tipo_label.setStyleSheet(f"color: {tipo_color}; background-color: transparent")
        contenido.addWidget(tipo_label)

        layout.addLayout(contenido, 1)

        # Botón agregar
        if mostrar_add:
            add_btn = BotonSmall("+", color=Colores.PRIMARIO)
            add_btn.setFixedSize(36, 36)
            add_btn.clicked.connect(lambda: self.add_clicked.emit(self.comida))
            layout.addWidget(add_btn)

    def mousePressEvent(self, event):
        """Emite señal de click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.comida)
        super().mousePressEvent(event)


class LogroCard(Card):
    """Tarjeta para mostrar un logro."""

    def __init__(self, logro, desbloqueado=False, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Icono
        icono_char = resolver_icono(logro.get('icono', 'trophy'))
        icono_label = QLabel(icono_char)
        icono_label.setFont(QFont('Phosphor', 28))
        color_icono = Colores.PRIMARIO if desbloqueado else Colores.TEXTO_CLARO
        icono_label.setStyleSheet(f"color: {color_icono}; background-color: transparent;")
        layout.addWidget(icono_label)

        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        nombre = QLabel(logro['nombre'])
        nombre.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        color = Colores.TEXTO if desbloqueado else Colores.TEXTO_CLARO
        nombre.setStyleSheet(f"color: {color}; background-color: transparent")
        info_layout.addWidget(nombre)

        desc = QLabel(logro['descripcion'])
        desc.setFont(QFont('Inter', 11))
        desc.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent")
        desc.setWordWrap(True)
        info_layout.addWidget(desc)

        if desbloqueado and logro.get('fecha_desbloqueo'):
            fecha = QLabel(f"Desbloqueado: {logro['fecha_desbloqueo']}")
            fecha.setFont(QFont('Inter', 9))
            fecha.setStyleSheet(f"color: {Colores.EXITO}; background-color: transparent")
            info_layout.addWidget(fecha)

        layout.addLayout(info_layout, 1)

        # Estado
        if desbloqueado:
            check = QLabel(Ph.CHECK)
            check.setFont(QFont('Phosphor', 20))
            check.setStyleSheet(f"color: {Colores.EXITO}; background-color: transparent;")
            layout.addWidget(check)


class Separador(QFrame):
    """Línea separadora horizontal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(1)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(f"background-color: {Colores.BORDE};")


class InputConLabel(QWidget):
    """Campo de entrada con label."""

    def __init__(self, label, placeholder="", password=False, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Label
        label_widget = QLabel(label)
        label_widget.setFont(QFont('Inter', 11))
        label_widget.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        layout.addWidget(label_widget)

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setMinimumHeight(45)
        if password:
            self.input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input)

    def text(self):
        """Retorna el texto del input."""
        return self.input.text()

    def setText(self, text):
        """Establece el texto del input."""
        self.input.setText(text)

    def clear(self):
        """Limpia el input."""
        self.input.clear()


class TituloSeccion(QLabel):
    """Título de sección."""

    def __init__(self, texto, parent=None):
        super().__init__(texto, parent)
        self.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        self.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")


class SubtituloSeccion(QLabel):
    """Subtítulo de sección."""

    def __init__(self, texto, parent=None):
        super().__init__(texto, parent)
        self.setFont(QFont('Inter', 14))
        self.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
