"""
Pantalla de Login para NutriSmart con PyQt6.
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QLineEdit, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from ui.styles import Colores
from ui.icons import Ph
from ui.components import BotonPrimario, BotonSecundario, InputConLabel, Card
from database.models import verificar_credenciales


class LoginWidget(QWidget):
    """Widget de inicio de sesión."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet(f"background-color: {Colores.FONDO};")
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz de usuario."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Panel izquierdo (decorativo) ──────────────────────────────────
        panel_izq = QFrame()
        panel_izq.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2e7d32, stop:0.65 #256427, stop:1 #1b5e20);
                border: none;
            }
        """)
        panel_izq.setMinimumWidth(420)
        panel_izq.setMaximumWidth(480)

        panel_izq_layout = QVBoxLayout(panel_izq)
        panel_izq_layout.setContentsMargins(50, 60, 50, 40)
        panel_izq_layout.setSpacing(0)

        # Logo PNG
        logo_label = QLabel()
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'assets', 'imgs', 'nutrismart.png'
        )
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                110, 110,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText(Ph.LEAF)
            logo_label.setFont(QFont('Phosphor', 64))
            logo_label.setStyleSheet("color: white; background: transparent;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("background: transparent;")
        panel_izq_layout.addWidget(logo_label)

        panel_izq_layout.addSpacing(22)

        # Nombre de la app
        titulo = QLabel("NutriSmart")
        titulo.setFont(QFont('Inter', 30, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("color: white; background: transparent;")
        panel_izq_layout.addWidget(titulo)

        panel_izq_layout.addSpacing(8)

        # Tagline
        subtitulo = QLabel("Tu asistente de nutrición inteligente")
        subtitulo.setFont(QFont('Inter', 13))
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setStyleSheet("color: rgba(255,255,255,0.78); background: transparent;")
        panel_izq_layout.addWidget(subtitulo)

        panel_izq_layout.addSpacing(36)

        # Separador decorativo
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setFrameShape(QFrame.Shape.NoFrame)
        sep.setStyleSheet("background-color: rgba(255,255,255,0.22);")
        panel_izq_layout.addWidget(sep)

        panel_izq_layout.addSpacing(30)

        # Features con iconos Phosphor
        features = [
            (Ph.CHART_BAR, "Cálculo de calorías y macros"),
            (Ph.FORK_KNIFE, "Recetas y comidas personalizadas"),
            (Ph.BARBELL,    "Planes según tu actividad física"),
            (Ph.TROPHY,     "Sistema de logros y rachas"),
        ]

        for icono, texto in features:
            feat_row = QHBoxLayout()
            feat_row.setSpacing(14)

            icon_lbl = QLabel(icono)
            icon_lbl.setFont(QFont('Phosphor', 17))
            icon_lbl.setFixedWidth(28)
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_lbl.setStyleSheet("color: rgba(255,255,255,0.88); background: transparent;")
            feat_row.addWidget(icon_lbl)

            feat_lbl = QLabel(texto)
            feat_lbl.setFont(QFont('Inter', 12))
            feat_lbl.setStyleSheet("color: rgba(255,255,255,0.80); background: transparent;")
            feat_row.addWidget(feat_lbl, 1)

            panel_izq_layout.addLayout(feat_row)
            panel_izq_layout.addSpacing(16)

        panel_izq_layout.addStretch()

        # Pie del panel
        version_label = QLabel("NutriSmart  ·  v1.0")
        version_label.setFont(QFont('Inter', 10))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: rgba(255,255,255,0.35); background: transparent;")
        panel_izq_layout.addWidget(version_label)

        layout.addWidget(panel_izq)

        # ── Panel derecho (formulario) ────────────────────────────────────
        panel_der = QFrame()
        panel_der.setStyleSheet(f"background-color: {Colores.FONDO}; border: none;")

        panel_der_layout = QVBoxLayout(panel_der)
        panel_der_layout.setContentsMargins(60, 60, 60, 60)
        panel_der_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card del formulario
        form_card = Card()
        form_card.setFixedWidth(400)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(18)

        # Ícono de acento dentro de la card
        card_icon = QLabel(Ph.LEAF)
        card_icon.setFont(QFont('Phosphor', 22))
        card_icon.setStyleSheet(f"color: {Colores.PRIMARIO}; background: transparent;")
        form_layout.addWidget(card_icon)

        form_layout.addSpacing(2)

        # Título
        titulo_form = QLabel("Iniciar Sesión")
        titulo_form.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        titulo_form.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        form_layout.addWidget(titulo_form)

        subtitulo_form = QLabel("Ingresa tus credenciales para continuar")
        subtitulo_form.setFont(QFont('Inter', 12))
        subtitulo_form.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        form_layout.addWidget(subtitulo_form)

        form_layout.addSpacing(6)

        # Email
        self.email_input = InputConLabel("Correo electrónico", "ejemplo@email.com")
        form_layout.addWidget(self.email_input)

        # Password
        self.password_input = InputConLabel("Contraseña", "••••••••", password=True)
        form_layout.addWidget(self.password_input)

        # Mensaje de error
        self.error_label = QLabel("")
        self.error_label.setFont(QFont('Inter', 11))
        self.error_label.setStyleSheet(f"color: {Colores.ERROR}; background-color: transparent;")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        form_layout.addWidget(self.error_label)

        form_layout.addSpacing(4)

        # Botón login
        self.btn_login = BotonPrimario("Iniciar Sesión")
        self.btn_login.clicked.connect(self._iniciar_sesion)
        form_layout.addWidget(self.btn_login)

        # Separador "o"
        separador_layout = QHBoxLayout()
        linea1 = QFrame()
        linea1.setFixedHeight(1)
        linea1.setFrameShape(QFrame.Shape.NoFrame)
        linea1.setStyleSheet(f"background-color: {Colores.BORDE};")
        separador_layout.addWidget(linea1)

        o_label = QLabel("o")
        o_label.setFont(QFont('Inter', 11))
        o_label.setContentsMargins(10, 0, 10, 0)
        o_label.setStyleSheet(f"color: {Colores.TEXTO_CLARO}; background-color: transparent;")
        separador_layout.addWidget(o_label)

        linea2 = QFrame()
        linea2.setFixedHeight(1)
        linea2.setFrameShape(QFrame.Shape.NoFrame)
        linea2.setStyleSheet(f"background-color: {Colores.BORDE};")
        separador_layout.addWidget(linea2)

        form_layout.addLayout(separador_layout)

        # Botón registro
        self.btn_registro = BotonSecundario("Crear una cuenta")
        self.btn_registro.clicked.connect(self._ir_a_registro)
        form_layout.addWidget(self.btn_registro)

        panel_der_layout.addWidget(form_card)
        layout.addWidget(panel_der, 1)

    def _iniciar_sesion(self):
        """Procesa el inicio de sesión."""
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            self._mostrar_error("Por favor completa todos los campos")
            return

        usuario = verificar_credenciales(email, password)

        if usuario:
            self.error_label.hide()
            self.controller.iniciar_sesion(usuario)
        else:
            self._mostrar_error("Credenciales incorrectas. Verifica tu email y contraseña.")

    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error."""
        self.error_label.setText(mensaje)
        self.error_label.show()

    def _ir_a_registro(self):
        """Navega a la pantalla de registro."""
        self.error_label.hide()
        self.controller.mostrar_registro()

    def limpiar_campos(self):
        """Limpia los campos del formulario."""
        self.email_input.clear()
        self.password_input.clear()
        self.error_label.hide()
