"""
Vista del Perfil de usuario.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QSpinBox, QDoubleSpinBox, QComboBox,
    QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.styles import Colores
from ui.icons import Ph
from ui.components import (
    Card, StatCard, TituloSeccion, SubtituloSeccion,
    BotonPrimario, BotonSecundario, Separador
)
from database.models import actualizar_usuario, crear_meta_diaria
from services.calculadora import obtener_factores_actividad, calcular_imc, calcular_todo


class PerfilView(QWidget):
    """Vista del perfil de usuario."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz del perfil."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {Colores.FONDO};")
        self.content_layout = QVBoxLayout(scroll_content)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(25)

        # Título
        titulo = TituloSeccion("Mi Perfil")
        self.content_layout.addWidget(titulo)

        subtitulo = SubtituloSeccion("Actualiza tu información personal y objetivos")
        self.content_layout.addWidget(subtitulo)

        # Card del perfil
        perfil_card = Card()
        perfil_card.setMaximumWidth(800)
        perfil_layout = QVBoxLayout(perfil_card)
        perfil_layout.setContentsMargins(30, 30, 30, 30)
        perfil_layout.setSpacing(20)

        # Avatar y nombre
        header_layout = QHBoxLayout()

        avatar = QLabel(Ph.USER)
        avatar.setFont(QFont('Phosphor', 40))
        avatar.setFixedSize(80, 80)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(f"""
            background-color: {Colores.FONDO};
            border-radius: 40px;
        """)
        header_layout.addWidget(avatar)

        info_layout = QVBoxLayout()
        self.nombre_label = QLabel("")
        self.nombre_label.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        self.nombre_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        info_layout.addWidget(self.nombre_label)

        self.email_label = QLabel("")
        self.email_label.setFont(QFont('Inter', 12))
        self.email_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        info_layout.addWidget(self.email_label)

        header_layout.addLayout(info_layout)
        header_layout.addStretch()

        perfil_layout.addLayout(header_layout)

        perfil_layout.addWidget(Separador())

        # Formulario de edición
        form_titulo = QLabel("Datos Personales")
        form_titulo.setFont(QFont('Inter', 16, QFont.Weight.Bold))
        form_titulo.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        perfil_layout.addWidget(form_titulo)

        # Edad y Sexo
        row1 = QHBoxLayout()
        row1.setSpacing(20)

        edad_widget = QWidget()
        edad_widget.setStyleSheet("background-color: transparent;")
        edad_layout = QVBoxLayout(edad_widget)
        edad_layout.setContentsMargins(0, 0, 0, 0)
        edad_layout.setSpacing(8)
        edad_label = QLabel("Edad (años)")
        edad_label.setFont(QFont('Inter', 11))
        edad_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        edad_layout.addWidget(edad_label)
        self.edad_spin = QSpinBox()
        self.edad_spin.setRange(10, 120)
        self.edad_spin.setMinimumHeight(45)
        edad_layout.addWidget(self.edad_spin)
        row1.addWidget(edad_widget)

        sexo_widget = QWidget()
        sexo_widget.setStyleSheet("background-color: transparent;")
        sexo_layout = QVBoxLayout(sexo_widget)
        sexo_layout.setContentsMargins(0, 0, 0, 0)
        sexo_layout.setSpacing(8)
        sexo_label = QLabel("Sexo")
        sexo_label.setFont(QFont('Inter', 11))
        sexo_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        sexo_layout.addWidget(sexo_label)
        self.sexo_combo = QComboBox()
        self.sexo_combo.addItems(["Masculino", "Femenino"])
        self.sexo_combo.setMinimumHeight(45)
        self.sexo_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 12px 15px;
                border: 1px solid {Colores.BORDE};
                border-radius: 6px;
                background-color: {Colores.FONDO_CARD};
                color: {Colores.TEXTO};
                font-size: 14px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colores.FONDO_CARD};
                border: 1px solid {Colores.BORDE};
                selection-background-color: #e8f5e9;
                selection-color: {Colores.PRIMARIO};
                color: {Colores.TEXTO};
            }}
        """)
        sexo_layout.addWidget(self.sexo_combo)
        row1.addWidget(sexo_widget)

        perfil_layout.addLayout(row1)

        # Peso y Altura
        row2 = QHBoxLayout()
        row2.setSpacing(20)

        peso_widget = QWidget()
        peso_widget.setStyleSheet("background-color: transparent;")
        peso_layout = QVBoxLayout(peso_widget)
        peso_layout.setContentsMargins(0, 0, 0, 0)
        peso_layout.setSpacing(8)
        peso_label = QLabel("Peso (kg)")
        peso_label.setFont(QFont('Inter', 11))
        peso_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        peso_layout.addWidget(peso_label)
        self.peso_spin = QDoubleSpinBox()
        self.peso_spin.setRange(20, 300)
        self.peso_spin.setDecimals(1)
        self.peso_spin.setMinimumHeight(45)
        peso_layout.addWidget(self.peso_spin)
        row2.addWidget(peso_widget)

        altura_widget = QWidget()
        altura_widget.setStyleSheet("background-color: transparent;")
        altura_layout = QVBoxLayout(altura_widget)
        altura_layout.setContentsMargins(0, 0, 0, 0)
        altura_layout.setSpacing(8)
        altura_label = QLabel("Altura (cm)")
        altura_label.setFont(QFont('Inter', 11))
        altura_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        altura_layout.addWidget(altura_label)
        self.altura_spin = QSpinBox()
        self.altura_spin.setRange(100, 250)
        self.altura_spin.setMinimumHeight(45)
        altura_layout.addWidget(self.altura_spin)
        row2.addWidget(altura_widget)

        perfil_layout.addLayout(row2)

        # Nivel de actividad
        actividad_widget = QWidget()
        actividad_widget.setStyleSheet("background-color: transparent;")
        actividad_layout = QVBoxLayout(actividad_widget)
        actividad_layout.setContentsMargins(0, 0, 0, 0)
        actividad_layout.setSpacing(8)
        actividad_label = QLabel("Nivel de actividad física")
        actividad_label.setFont(QFont('Inter', 11))
        actividad_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        actividad_layout.addWidget(actividad_label)
        self.actividad_combo = QComboBox()

        factores = obtener_factores_actividad()
        for key, data in factores.items():
            self.actividad_combo.addItem(f"{data['nombre']} - {data['descripcion']}", key)

        self.actividad_combo.setMinimumHeight(45)
        self.actividad_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 12px 15px;
                border: 1px solid {Colores.BORDE};
                border-radius: 6px;
                background-color: {Colores.FONDO_CARD};
                color: {Colores.TEXTO};
                font-size: 14px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colores.FONDO_CARD};
                border: 1px solid {Colores.BORDE};
                selection-background-color: #e8f5e9;
                selection-color: {Colores.PRIMARIO};
                color: {Colores.TEXTO};
            }}
        """)
        actividad_layout.addWidget(self.actividad_combo)
        perfil_layout.addWidget(actividad_widget)

        # Objetivo
        objetivo_widget = QWidget()
        objetivo_widget.setStyleSheet("background-color: transparent;")
        objetivo_layout = QVBoxLayout(objetivo_widget)
        objetivo_layout.setContentsMargins(0, 0, 0, 0)
        objetivo_layout.setSpacing(8)
        objetivo_label = QLabel("Objetivo")
        objetivo_label.setFont(QFont('Inter', 11))
        objetivo_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        objetivo_layout.addWidget(objetivo_label)

        self.objetivo_group = QButtonGroup()
        objetivos_layout = QHBoxLayout()
        objetivos_layout.setSpacing(15)

        objetivos = [("Bajar peso", "bajar"), ("Mantener", "mantener"), ("Subir peso", "subir")]
        for i, (texto, valor) in enumerate(objetivos):
            radio = QRadioButton(texto)
            radio.setProperty("valor", valor)
            radio.setFont(QFont('Inter', 11))
            radio.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
            self.objetivo_group.addButton(radio, i)
            objetivos_layout.addWidget(radio)

        objetivos_layout.addStretch()
        objetivo_layout.addLayout(objetivos_layout)
        perfil_layout.addWidget(objetivo_widget)

        # Mensaje de resultado
        self.resultado_label = QLabel("")
        self.resultado_label.setFont(QFont('Inter', 11))
        self.resultado_label.setWordWrap(True)
        self.resultado_label.hide()
        perfil_layout.addWidget(self.resultado_label)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(15)

        btn_guardar = BotonPrimario("Guardar Cambios")
        btn_guardar.clicked.connect(self._guardar_cambios)
        botones_layout.addWidget(btn_guardar)

        btn_cancelar = BotonSecundario("Cancelar")
        btn_cancelar.clicked.connect(self.actualizar_datos)
        botones_layout.addWidget(btn_cancelar)

        botones_layout.addStretch()

        perfil_layout.addLayout(botones_layout)

        self.content_layout.addWidget(perfil_card)

        # Estadísticas IMC
        self.imc_card = None

        self.content_layout.addStretch()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def actualizar_datos(self):
        """Actualiza los datos del perfil."""
        usuario = self.controller.usuario_actual
        if not usuario:
            return

        # Actualizar labels
        self.nombre_label.setText(usuario['nombre'])
        self.email_label.setText(usuario['email'])

        # Actualizar campos
        self.edad_spin.setValue(int(usuario['edad']))
        self.peso_spin.setValue(float(usuario['peso']))
        self.altura_spin.setValue(int(usuario['altura']))
        self.sexo_combo.setCurrentIndex(0 if usuario['sexo'] == 'masculino' else 1)

        # Nivel de actividad
        nivel_act = usuario.get('nivel_actividad', 'sedentario')
        for i in range(self.actividad_combo.count()):
            if self.actividad_combo.itemData(i) == nivel_act:
                self.actividad_combo.setCurrentIndex(i)
                break

        # Objetivo
        obj_map = {'bajar': 0, 'mantener': 1, 'subir': 2}
        if usuario['objetivo'] in obj_map:
            self.objetivo_group.button(obj_map[usuario['objetivo']]).setChecked(True)

        self.resultado_label.hide()

        # Actualizar/crear card de IMC
        self._actualizar_imc_card(usuario)

    def _actualizar_imc_card(self, usuario):
        """Actualiza la tarjeta de IMC."""
        if self.imc_card:
            self.content_layout.removeWidget(self.imc_card)
            self.imc_card.deleteLater()

        imc_data = calcular_imc(usuario['peso'], usuario['altura'])

        imc_card = Card()
        imc_card.setMaximumWidth(800)
        imc_layout = QHBoxLayout(imc_card)
        imc_layout.setContentsMargins(30, 25, 30, 25)

        icon = QLabel(Ph.SCALES)
        icon.setFont(QFont('Phosphor', 36))
        icon.setStyleSheet(f"color: {Colores.PRIMARIO}; background-color: transparent;")
        imc_layout.addWidget(icon)

        info = QVBoxLayout()
        titulo = QLabel("Índice de Masa Corporal (IMC)")
        titulo.setFont(QFont('Inter', 12))
        titulo.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        info.addWidget(titulo)

        valor = QLabel(f"{imc_data['imc']}")
        valor.setFont(QFont('Inter', 32, QFont.Weight.Bold))
        valor.setStyleSheet(f"color: {imc_data['color']}; background-color: transparent;")
        info.addWidget(valor)

        clasificacion = QLabel(imc_data['clasificacion'])
        clasificacion.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        clasificacion.setStyleSheet(f"color: {imc_data['color']}; background-color: transparent;")
        info.addWidget(clasificacion)

        imc_layout.addLayout(info)
        imc_layout.addStretch()

        self.content_layout.insertWidget(self.content_layout.count() - 1, imc_card)
        self.imc_card = imc_card

    def _guardar_cambios(self):
        """Guarda los cambios del perfil."""
        usuario = self.controller.usuario_actual
        if not usuario:
            return

        edad = self.edad_spin.value()
        peso = self.peso_spin.value()
        altura = self.altura_spin.value()
        sexo = "masculino" if self.sexo_combo.currentIndex() == 0 else "femenino"
        nivel_actividad = self.actividad_combo.currentData()

        # Obtener objetivo
        objetivo = "mantener"
        for btn in self.objetivo_group.buttons():
            if btn.isChecked():
                objetivo = btn.property("valor")
                break

        try:
            actualizar_usuario(
                usuario['id'],
                edad=edad,
                peso=peso,
                altura=altura,
                sexo=sexo,
                objetivo=objetivo,
                nivel_actividad=nivel_actividad
            )

            # Actualizar usuario actual
            self.controller.usuario_actual['edad'] = edad
            self.controller.usuario_actual['peso'] = peso
            self.controller.usuario_actual['altura'] = altura
            self.controller.usuario_actual['sexo'] = sexo
            self.controller.usuario_actual['objetivo'] = objetivo
            self.controller.usuario_actual['nivel_actividad'] = nivel_actividad

            self.resultado_label.setText("✓ Cambios guardados correctamente")
            self.resultado_label.setStyleSheet(f"color: {Colores.EXITO}; background-color: transparent;")
            self.resultado_label.show()

            # Actualizar IMC
            self._actualizar_imc_card(self.controller.usuario_actual)

            # Recalcular y actualizar meta diaria con los nuevos datos del perfil
            usuario_actualizado = self.controller.usuario_actual
            resultados = calcular_todo(
                usuario_actualizado['peso'], usuario_actualizado['altura'],
                usuario_actualizado['edad'], usuario_actualizado['sexo'],
                usuario_actualizado['objetivo'],
                usuario_actualizado.get('nivel_actividad', 'sedentario')
            )
            crear_meta_diaria(
                usuario_actualizado['id'],
                resultados['calorias_objetivo'],
                resultados['proteinas_g'],
                resultados['carbohidratos_g'],
                resultados['grasas_g']
            )

        except Exception as e:
            self.resultado_label.setText(f"✗ Error al guardar: {str(e)}")
            self.resultado_label.setStyleSheet(f"color: {Colores.ERROR}; background-color: transparent;")
            self.resultado_label.show()
