"""
Pantalla de Registro para NutriSmart con PyQt6.
"""
import os
import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QLineEdit, QComboBox, QRadioButton, QButtonGroup,
    QScrollArea, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from ui.styles import Colores
from ui.icons import Ph
from ui.components import BotonPrimario, BotonSecundario, InputConLabel, Card
from database.models import crear_usuario, email_existe
from services.calculadora import obtener_factores_actividad


class RegistroWidget(QWidget):
    """Widget de registro de usuario."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet(f"background-color: {Colores.FONDO};")
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz de usuario."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Panel izquierdo (decorativo) — idéntico al de login
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

        titulo = QLabel("NutriSmart")
        titulo.setFont(QFont('Inter', 30, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("color: white; background: transparent;")
        panel_izq_layout.addWidget(titulo)

        panel_izq_layout.addSpacing(8)

        subtitulo = QLabel("Tu asistente de nutrición inteligente")
        subtitulo.setFont(QFont('Inter', 13))
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setStyleSheet("color: rgba(255,255,255,0.78); background: transparent;")
        panel_izq_layout.addWidget(subtitulo)

        panel_izq_layout.addSpacing(36)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setFrameShape(QFrame.Shape.NoFrame)
        sep.setStyleSheet("background-color: rgba(255,255,255,0.22);")
        panel_izq_layout.addWidget(sep)

        panel_izq_layout.addSpacing(30)

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

        version_label = QLabel("NutriSmart  ·  v1.0")
        version_label.setFont(QFont('Inter', 10))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: rgba(255,255,255,0.35); background: transparent;")
        panel_izq_layout.addWidget(version_label)

        layout.addWidget(panel_izq)

        # Panel derecho (formulario con scroll)
        panel_der = QFrame()
        panel_der.setStyleSheet(f"background-color: {Colores.FONDO};")

        panel_der_layout = QVBoxLayout(panel_der)
        panel_der_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(60, 40, 60, 40)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Card del formulario
        form_card = Card()
        form_card.setFixedWidth(500)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(40, 30, 40, 30)
        form_layout.setSpacing(15)

        # Título
        titulo_form = QLabel("Crear Cuenta")
        titulo_form.setFont(QFont('Inter', 22, QFont.Weight.Bold))
        titulo_form.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        form_layout.addWidget(titulo_form)

        subtitulo_form = QLabel("Completa tus datos para personalizar tu plan nutricional")
        subtitulo_form.setFont(QFont('Inter', 11))
        subtitulo_form.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent")
        subtitulo_form.setWordWrap(True)
        form_layout.addWidget(subtitulo_form)

        form_layout.addSpacing(5)

        # Nombre
        self.nombre_input = InputConLabel("Nombre completo", "Tu nombre")
        form_layout.addWidget(self.nombre_input)

        # Email
        self.email_input = InputConLabel("Correo electrónico", "ejemplo@email.com")
        form_layout.addWidget(self.email_input)

        # Password
        self.password_input = InputConLabel("Contraseña", "Mínimo 4 caracteres", password=True)
        form_layout.addWidget(self.password_input)

        # Datos físicos en dos columnas
        datos_layout = QHBoxLayout()
        datos_layout.setSpacing(20)

        # Columna izquierda
        col_izq = QVBoxLayout()
        col_izq.setSpacing(15)

        # Edad
        edad_widget = QWidget()
        edad_widget.setStyleSheet("background-color: transparent;")
        edad_layout = QVBoxLayout(edad_widget)
        edad_layout.setContentsMargins(0, 0, 0, 0)
        edad_layout.setSpacing(8)
        edad_label = QLabel("Edad (años)")
        edad_label.setFont(QFont('Inter', 11))
        edad_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        edad_layout.addWidget(edad_label)
        self.edad_spin = QSpinBox()
        self.edad_spin.setRange(10, 120)
        self.edad_spin.setValue(25)
        self.edad_spin.setMinimumHeight(45)
        edad_layout.addWidget(self.edad_spin)
        col_izq.addWidget(edad_widget)

        # Peso
        peso_widget = QWidget()
        peso_widget.setStyleSheet("background-color: transparent;")
        peso_layout = QVBoxLayout(peso_widget)
        peso_layout.setContentsMargins(0, 0, 0, 0)
        peso_layout.setSpacing(8)
        peso_label = QLabel("Peso (kg)")
        peso_label.setFont(QFont('Inter', 11))
        peso_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        peso_layout.addWidget(peso_label)
        self.peso_spin = QDoubleSpinBox()
        self.peso_spin.setRange(20, 300)
        self.peso_spin.setValue(70)
        self.peso_spin.setDecimals(1)
        self.peso_spin.setMinimumHeight(45)
        peso_layout.addWidget(self.peso_spin)
        col_izq.addWidget(peso_widget)

        datos_layout.addLayout(col_izq)

        # Columna derecha
        col_der = QVBoxLayout()
        col_der.setSpacing(15)

        # Altura
        altura_widget = QWidget()
        altura_widget.setStyleSheet("background-color: transparent;")
        altura_layout = QVBoxLayout(altura_widget)
        altura_layout.setContentsMargins(0, 0, 0, 0)
        altura_layout.setSpacing(8)
        altura_label = QLabel("Altura (cm)")
        altura_label.setFont(QFont('Inter', 11))
        altura_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        altura_layout.addWidget(altura_label)
        self.altura_spin = QSpinBox()
        self.altura_spin.setRange(100, 250)
        self.altura_spin.setValue(170)
        self.altura_spin.setMinimumHeight(45)
        altura_layout.addWidget(self.altura_spin)
        col_der.addWidget(altura_widget)

        # Sexo
        sexo_widget = QWidget()
        sexo_widget.setStyleSheet("background-color: transparent;")
        sexo_layout = QVBoxLayout(sexo_widget)
        sexo_layout.setContentsMargins(0, 0, 0, 0)
        sexo_layout.setSpacing(8)
        sexo_label = QLabel("Sexo")
        sexo_label.setFont(QFont('Inter', 11))
        sexo_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        sexo_layout.addWidget(sexo_label)
        self.sexo_combo = QComboBox()
        self.sexo_combo.addItems(["Masculino", "Femenino"])
        self.sexo_combo.setMinimumHeight(45)
        sexo_layout.addWidget(self.sexo_combo)
        col_der.addWidget(sexo_widget)

        datos_layout.addLayout(col_der)
        form_layout.addLayout(datos_layout)

        # Nivel de actividad
        actividad_widget = QWidget()
        actividad_widget.setStyleSheet("background-color: transparent;")
        actividad_layout = QVBoxLayout(actividad_widget)
        actividad_layout.setContentsMargins(0, 0, 0, 0)
        actividad_layout.setSpacing(8)
        actividad_label = QLabel("Nivel de actividad física")
        actividad_label.setFont(QFont('Inter', 11))
        actividad_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        actividad_layout.addWidget(actividad_label)
        self.actividad_combo = QComboBox()

        factores = obtener_factores_actividad()
        for key, data in factores.items():
            self.actividad_combo.addItem(f"{data['nombre']} - {data['descripcion']}", key)

        self.actividad_combo.setMinimumHeight(45)
        actividad_layout.addWidget(self.actividad_combo)
        form_layout.addWidget(actividad_widget)

        # Objetivo
        objetivo_widget = QWidget()
        objetivo_widget.setStyleSheet("background-color: transparent;")
        objetivo_layout = QVBoxLayout(objetivo_widget)
        objetivo_layout.setContentsMargins(0, 0, 0, 0)
        objetivo_layout.setSpacing(8)
        objetivo_label = QLabel("Objetivo")
        objetivo_label.setFont(QFont('Inter', 11))
        objetivo_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
        objetivo_layout.addWidget(objetivo_label)

        self.objetivo_group = QButtonGroup()
        objetivos_layout = QHBoxLayout()
        objetivos_layout.setSpacing(15)

        objetivos = [("Bajar peso", "bajar"), ("Mantener", "mantener"), ("Subir peso", "subir")]
        for i, (texto, valor) in enumerate(objetivos):
            radio = QRadioButton(texto)
            radio.setProperty("valor", valor)
            radio.setFont(QFont('Inter', 11))
            radio.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent")
            if valor == "mantener":
                radio.setChecked(True)
            self.objetivo_group.addButton(radio, i)
            objetivos_layout.addWidget(radio)

        objetivos_layout.addStretch()
        objetivo_layout.addLayout(objetivos_layout)
        form_layout.addWidget(objetivo_widget)

        # Mensaje de error
        self.error_label = QLabel("")
        self.error_label.setFont(QFont('Inter', 11))
        self.error_label.setStyleSheet(f"color: {Colores.ERROR}; background-color: transparent")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        form_layout.addWidget(self.error_label)

        form_layout.addSpacing(5)

        # Botón registrar
        self.btn_registrar = BotonPrimario("Crear Cuenta")
        self.btn_registrar.clicked.connect(self._registrar)
        form_layout.addWidget(self.btn_registrar)

        # Link a login
        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ya_cuenta = QLabel("¿Ya tienes cuenta?")
        ya_cuenta.setFont(QFont('Inter', 11))
        ya_cuenta.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent")
        login_layout.addWidget(ya_cuenta)

        login_link = QLabel("Inicia sesión")
        login_link.setFont(QFont('Inter', 11))
        login_link.setStyleSheet(f"color: {Colores.PRIMARIO}; text-decoration: underline; background-color: transparent")
        login_link.setCursor(Qt.CursorShape.PointingHandCursor)
        login_link.mousePressEvent = lambda e: self._ir_a_login()
        login_layout.addWidget(login_link)

        form_layout.addLayout(login_layout)

        scroll_layout.addWidget(form_card)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        panel_der_layout.addWidget(scroll)

        layout.addWidget(panel_der, 1)

    def _validar_email(self, email):
        """Valida el formato del email."""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    def _registrar(self):
        """Procesa el registro del usuario."""
        nombre = self.nombre_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        edad = self.edad_spin.value()
        peso = self.peso_spin.value()
        altura = self.altura_spin.value()
        sexo = "masculino" if self.sexo_combo.currentIndex() == 0 else "femenino"
        nivel_actividad = self.actividad_combo.currentData()

        # Obtener objetivo seleccionado
        objetivo = "mantener"
        for btn in self.objetivo_group.buttons():
            if btn.isChecked():
                objetivo = btn.property("valor")
                break

        # Validaciones
        if not nombre:
            self._mostrar_error("Por favor ingresa tu nombre")
            return

        if not email or not self._validar_email(email):
            self._mostrar_error("Por favor ingresa un email válido")
            return

        if len(password) < 4:
            self._mostrar_error("La contraseña debe tener al menos 4 caracteres")
            return

        if email_existe(email):
            self._mostrar_error("Este email ya está registrado")
            return

        # Crear usuario
        try:
            user_id = crear_usuario(
                nombre, edad, peso, altura, sexo, objetivo,
                nivel_actividad, email, password
            )
            self.error_label.hide()
            self.controller.mostrar_mensaje(
                "Cuenta creada",
                "Tu cuenta ha sido creada correctamente. Ahora puedes iniciar sesión.",
                "success"
            )
            self._limpiar_campos()
            self.controller.mostrar_login()
        except Exception as e:
            self._mostrar_error(f"Error al crear la cuenta: {str(e)}")

    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error."""
        self.error_label.setText(mensaje)
        self.error_label.show()

    def _ir_a_login(self):
        """Navega a la pantalla de login."""
        self.error_label.hide()
        self.controller.mostrar_login()

    def _limpiar_campos(self):
        """Limpia los campos del formulario."""
        self.nombre_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.edad_spin.setValue(25)
        self.peso_spin.setValue(70)
        self.altura_spin.setValue(170)
        self.sexo_combo.setCurrentIndex(0)
        self.actividad_combo.setCurrentIndex(0)
        self.objetivo_group.buttons()[1].setChecked(True)  # Mantener
        self.error_label.hide()
