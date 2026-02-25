"""
Vista de Recetas con detalles clickeables.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QDialog, QComboBox, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.styles import Colores
from ui.icons import Ph
from ui.components import (
    Card, ComidaCard, TituloSeccion, SubtituloSeccion,
    BotonPrimario, BotonSecundario, BotonPeligro, Separador
)
from database.models import obtener_comidas, crear_comida, obtener_recetas_usuario, eliminar_comida


class CrearComidaDialog(QDialog):
    """Diálogo para crear una comida personalizada."""

    def __init__(self, usuario_id, parent=None):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz del diálogo."""
        self.setWindowTitle("Crear Comida Personalizada")
        self.setMinimumSize(700, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        titulo = QLabel("Nueva Comida")
        titulo.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        titulo.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        layout.addWidget(titulo)

        # Scroll area para el formulario
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QWidget()
        form_layout = QVBoxLayout(scroll_content)
        form_layout.setSpacing(15)

        # Nombre
        nombre_label = QLabel("Nombre de la comida *")
        nombre_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        nombre_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        form_layout.addWidget(nombre_label)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ej: Ensalada de pollo")
        self.nombre_input.setMinimumHeight(40)
        form_layout.addWidget(self.nombre_input)

        # Tipo
        tipo_label = QLabel("Tipo de comida *")
        tipo_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        tipo_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        form_layout.addWidget(tipo_label)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Desayuno", "Almuerzo", "Cena", "Snack"])
        self.tipo_combo.setMinimumHeight(40)
        form_layout.addWidget(self.tipo_combo)

        # Información nutricional
        nutri_label = QLabel("Información Nutricional *")
        nutri_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        nutri_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        form_layout.addWidget(nutri_label)

        nutri_grid = QHBoxLayout()
        nutri_grid.setSpacing(15)

        # Calorías
        cal_widget = QWidget()
        cal_layout = QVBoxLayout(cal_widget)
        cal_layout.setContentsMargins(0, 0, 0, 0)
        cal_layout.setSpacing(5)
        cal_lbl = QLabel("Calorías (kcal)")
        cal_lbl.setFont(QFont('Inter', 10))
        cal_layout.addWidget(cal_lbl)
        self.calorias_spin = QSpinBox()
        self.calorias_spin.setRange(0, 5000)
        self.calorias_spin.setValue(200)
        self.calorias_spin.setMinimumHeight(40)
        cal_layout.addWidget(self.calorias_spin)
        nutri_grid.addWidget(cal_widget)

        # Proteínas
        prot_widget = QWidget()
        prot_layout = QVBoxLayout(prot_widget)
        prot_layout.setContentsMargins(0, 0, 0, 0)
        prot_layout.setSpacing(5)
        prot_lbl = QLabel("Proteínas (g)")
        prot_lbl.setFont(QFont('Inter', 10))
        prot_layout.addWidget(prot_lbl)
        self.proteinas_spin = QDoubleSpinBox()
        self.proteinas_spin.setRange(0, 500)
        self.proteinas_spin.setValue(10)
        self.proteinas_spin.setDecimals(1)
        self.proteinas_spin.setMinimumHeight(40)
        prot_layout.addWidget(self.proteinas_spin)
        nutri_grid.addWidget(prot_widget)

        # Carbohidratos
        carb_widget = QWidget()
        carb_layout = QVBoxLayout(carb_widget)
        carb_layout.setContentsMargins(0, 0, 0, 0)
        carb_layout.setSpacing(5)
        carb_lbl = QLabel("Carbohidratos (g)")
        carb_lbl.setFont(QFont('Inter', 10))
        carb_layout.addWidget(carb_lbl)
        self.carbs_spin = QDoubleSpinBox()
        self.carbs_spin.setRange(0, 500)
        self.carbs_spin.setValue(20)
        self.carbs_spin.setDecimals(1)
        self.carbs_spin.setMinimumHeight(40)
        carb_layout.addWidget(self.carbs_spin)
        nutri_grid.addWidget(carb_widget)

        # Grasas
        gras_widget = QWidget()
        gras_layout = QVBoxLayout(gras_widget)
        gras_layout.setContentsMargins(0, 0, 0, 0)
        gras_layout.setSpacing(5)
        gras_lbl = QLabel("Grasas (g)")
        gras_lbl.setFont(QFont('Inter', 10))
        gras_layout.addWidget(gras_lbl)
        self.grasas_spin = QDoubleSpinBox()
        self.grasas_spin.setRange(0, 500)
        self.grasas_spin.setValue(5)
        self.grasas_spin.setDecimals(1)
        self.grasas_spin.setMinimumHeight(40)
        gras_layout.addWidget(self.grasas_spin)
        nutri_grid.addWidget(gras_widget)

        form_layout.addLayout(nutri_grid)

        # Ingredientes (opcional)
        ingr_label = QLabel("Ingredientes (opcional)")
        ingr_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        ingr_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        form_layout.addWidget(ingr_label)

        ingr_help = QLabel("Separa cada ingrediente con '|' (pipe). Ej: 200g pollo | 100g lechuga | 1 tomate")
        ingr_help.setFont(QFont('Inter', 9))
        ingr_help.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        ingr_help.setWordWrap(True)
        form_layout.addWidget(ingr_help)

        self.ingredientes_input = QTextEdit()
        self.ingredientes_input.setPlaceholderText("200g pechuga de pollo | 100g lechuga | 1 tomate | 2 cucharadas aceite de oliva")
        self.ingredientes_input.setMinimumHeight(80)
        form_layout.addWidget(self.ingredientes_input)

        # Preparación (opcional)
        prep_label = QLabel("Preparación (opcional)")
        prep_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        prep_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        form_layout.addWidget(prep_label)

        prep_help = QLabel("Separa cada paso con '|'. Ej: Cocinar el pollo | Cortar las verduras | Mezclar todo")
        prep_help.setFont(QFont('Inter', 9))
        prep_help.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        prep_help.setWordWrap(True)
        form_layout.addWidget(prep_help)

        self.preparacion_input = QTextEdit()
        self.preparacion_input.setPlaceholderText("Cocinar el pollo a la plancha | Cortar las verduras | Mezclar todo en un bowl")
        self.preparacion_input.setMinimumHeight(100)
        form_layout.addWidget(self.preparacion_input)

        # Tiempo y dificultad
        extra_layout = QHBoxLayout()
        extra_layout.setSpacing(15)

        # Tiempo
        tiempo_widget = QWidget()
        tiempo_layout = QVBoxLayout(tiempo_widget)
        tiempo_layout.setContentsMargins(0, 0, 0, 0)
        tiempo_layout.setSpacing(5)
        tiempo_label = QLabel("Tiempo (minutos)")
        tiempo_label.setFont(QFont('Inter', 10))
        tiempo_layout.addWidget(tiempo_label)
        self.tiempo_spin = QSpinBox()
        self.tiempo_spin.setRange(1, 300)
        self.tiempo_spin.setValue(30)
        self.tiempo_spin.setMinimumHeight(40)
        tiempo_layout.addWidget(self.tiempo_spin)
        extra_layout.addWidget(tiempo_widget)

        # Dificultad
        dif_widget = QWidget()
        dif_layout = QVBoxLayout(dif_widget)
        dif_layout.setContentsMargins(0, 0, 0, 0)
        dif_layout.setSpacing(5)
        dif_label = QLabel("Dificultad")
        dif_label.setFont(QFont('Inter', 10))
        dif_layout.addWidget(dif_label)
        self.dificultad_combo = QComboBox()
        self.dificultad_combo.addItems(["Fácil", "Media", "Difícil"])
        self.dificultad_combo.setCurrentIndex(1)
        self.dificultad_combo.setMinimumHeight(40)
        dif_layout.addWidget(self.dificultad_combo)
        extra_layout.addWidget(dif_widget)

        form_layout.addLayout(extra_layout)

        # Mensaje de error
        self.error_label = QLabel("")
        self.error_label.setFont(QFont('Inter', 11))
        self.error_label.setStyleSheet(f"color: {Colores.ERROR}; background-color: transparent;")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        form_layout.addWidget(self.error_label)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.addStretch()

        btn_cancelar = BotonSecundario("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancelar)

        btn_guardar = BotonPrimario("Guardar Comida")
        btn_guardar.clicked.connect(self._guardar_comida)
        botones_layout.addWidget(btn_guardar)

        layout.addLayout(botones_layout)

    def _guardar_comida(self):
        """Guarda la comida personalizada."""
        nombre = self.nombre_input.text().strip()
        if not nombre:
            self.error_label.setText("Por favor ingresa un nombre para la comida")
            self.error_label.show()
            return

        tipo = self.tipo_combo.currentText().lower()
        calorias = self.calorias_spin.value()
        proteinas = self.proteinas_spin.value()
        carbs = self.carbs_spin.value()
        grasas = self.grasas_spin.value()
        ingredientes = self.ingredientes_input.toPlainText().strip()
        preparacion = self.preparacion_input.toPlainText().strip()
        tiempo = self.tiempo_spin.value()
        dificultad = self.dificultad_combo.currentText().lower()

        try:
            crear_comida(
                nombre, tipo, calorias, proteinas, carbs, grasas,
                ingredientes, preparacion, tiempo, dificultad, self.usuario_id
            )
            self.accept()
        except Exception as e:
            self.error_label.setText(f"Error al guardar: {str(e)}")
            self.error_label.show()


class DetalleRecetaDialog(QDialog):
    """Diálogo para mostrar el detalle de una receta."""

    def __init__(self, comida, usuario_id=None, parent=None):
        super().__init__(parent)
        self.comida = comida
        self.usuario_id = usuario_id
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz del diálogo."""
        self.setWindowTitle(self.comida['nombre'])
        self.setMinimumSize(700, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {Colores.FONDO};")
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Header
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(10)

        # Nombre
        nombre = QLabel(self.comida['nombre'])
        nombre.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        nombre.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        nombre.setWordWrap(True)
        header_layout.addWidget(nombre)

        # Tipo y tiempo
        meta_layout = QHBoxLayout()

        tipo_label = QLabel(f'<span style="font-family: Phosphor;">{Ph.FORK_KNIFE}</span>&nbsp;&nbsp;{self.comida["tipo"].title()}')
        tipo_label.setTextFormat(Qt.TextFormat.RichText)
        tipo_label.setFont(QFont('Inter', 12))
        tipo_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        meta_layout.addWidget(tipo_label)

        if self.comida.get('tiempo_preparacion'):
            tiempo_label = QLabel(f'<span style="font-family: Phosphor;">{Ph.CLOCK}</span>&nbsp;&nbsp;{self.comida["tiempo_preparacion"]} min')
            tiempo_label.setTextFormat(Qt.TextFormat.RichText)
            tiempo_label.setFont(QFont('Inter', 12))
            tiempo_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
            meta_layout.addWidget(tiempo_label)

        if self.comida.get('dificultad'):
            dificultad_label = QLabel(f'<span style="font-family: Phosphor;">{Ph.CHEF_HAT}</span>&nbsp;&nbsp;{self.comida["dificultad"].title()}')
            dificultad_label.setTextFormat(Qt.TextFormat.RichText)
            dificultad_label.setFont(QFont('Inter', 12))
            dificultad_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
            meta_layout.addWidget(dificultad_label)

        meta_layout.addStretch()
        header_layout.addLayout(meta_layout)

        content_layout.addWidget(header)

        # Info nutricional
        nutri_card = Card()
        nutri_layout = QHBoxLayout(nutri_card)
        nutri_layout.setContentsMargins(20, 15, 20, 15)
        nutri_layout.setSpacing(30)

        nutri_data = [
            ("Calorías", f"{self.comida['calorias']} kcal", Colores.PRIMARIO),
            ("Proteínas", f"{self.comida['proteinas']}g", "#e74c3c"),
            ("Carbohidratos", f"{self.comida['carbs']}g", "#f39c12"),
            ("Grasas", f"{self.comida['grasas']}g", "#9b59b6"),
        ]

        for titulo, valor, color in nutri_data:
            nutri_widget = QWidget()
            nutri_widget_layout = QVBoxLayout(nutri_widget)
            nutri_widget_layout.setSpacing(5)

            titulo_label = QLabel(titulo)
            titulo_label.setFont(QFont('Inter', 10))
            titulo_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
            nutri_widget_layout.addWidget(titulo_label)

            valor_label = QLabel(valor)
            valor_label.setFont(QFont('Inter', 16, QFont.Weight.Bold))
            valor_label.setStyleSheet(f"color: {color}; background-color: transparent;")
            nutri_widget_layout.addWidget(valor_label)

            nutri_layout.addWidget(nutri_widget)

        nutri_layout.addStretch()
        content_layout.addWidget(nutri_card)

        # Ingredientes
        if self.comida.get('ingredientes'):
            ingredientes_titulo = QLabel(f'<span style="font-family: Phosphor;">{Ph.BOWL}</span>&nbsp; Ingredientes')
            ingredientes_titulo.setTextFormat(Qt.TextFormat.RichText)
            ingredientes_titulo.setFont(QFont('Inter', 18, QFont.Weight.Bold))
            ingredientes_titulo.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
            content_layout.addWidget(ingredientes_titulo)

            ingredientes_card = Card()
            ingredientes_layout = QVBoxLayout(ingredientes_card)
            ingredientes_layout.setContentsMargins(25, 20, 25, 20)
            ingredientes_layout.setSpacing(10)

            ingredientes_lista = self.comida['ingredientes'].split('|')
            for ingrediente in ingredientes_lista:
                ing_layout = QHBoxLayout()

                bullet = QLabel("•")
                bullet.setFont(QFont('Inter', 14, QFont.Weight.Bold))
                bullet.setStyleSheet(f"color: {Colores.PRIMARIO}; background-color: transparent;")
                bullet.setFixedWidth(20)
                ing_layout.addWidget(bullet)

                ing_label = QLabel(ingrediente.strip())
                ing_label.setFont(QFont('Inter', 12))
                ing_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
                ing_label.setWordWrap(True)
                ing_layout.addWidget(ing_label, 1)

                ingredientes_layout.addLayout(ing_layout)

            content_layout.addWidget(ingredientes_card)

        # Preparación
        if self.comida.get('preparacion'):
            preparacion_titulo = QLabel(f'<span style="font-family: Phosphor;">{Ph.CHEF_HAT}</span>&nbsp; Preparación')
            preparacion_titulo.setTextFormat(Qt.TextFormat.RichText)
            preparacion_titulo.setFont(QFont('Inter', 18, QFont.Weight.Bold))
            preparacion_titulo.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
            content_layout.addWidget(preparacion_titulo)

            preparacion_card = Card()
            preparacion_layout = QVBoxLayout(preparacion_card)
            preparacion_layout.setContentsMargins(25, 20, 25, 20)
            preparacion_layout.setSpacing(15)

            pasos = self.comida['preparacion'].split('|')
            for i, paso in enumerate(pasos, 1):
                paso_layout = QHBoxLayout()
                paso_layout.setSpacing(15)

                # Número de paso
                numero = QLabel(str(i))
                numero.setFont(QFont('Inter', 16, QFont.Weight.Bold))
                numero.setFixedSize(35, 35)
                numero.setAlignment(Qt.AlignmentFlag.AlignCenter)
                numero.setStyleSheet(f"""
                    background-color: {Colores.PRIMARIO};
                    color: white;
                    border-radius: 17px;
                """)
                paso_layout.addWidget(numero)

                # Texto del paso
                paso_label = QLabel(paso.strip())
                paso_label.setFont(QFont('Inter', 12))
                paso_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
                paso_label.setWordWrap(True)
                paso_layout.addWidget(paso_label, 1)

                preparacion_layout.addLayout(paso_layout)

            content_layout.addWidget(preparacion_card)

        content_layout.addStretch()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setContentsMargins(30, 15, 30, 20)

        # Botón eliminar (solo para recetas personalizadas del usuario)
        if self.comida.get('es_personalizada') and self.usuario_id:
            btn_eliminar = BotonPeligro("Eliminar Receta")
            btn_eliminar.clicked.connect(self._eliminar_receta)
            botones_layout.addWidget(btn_eliminar)

        botones_layout.addStretch()

        btn_cerrar = BotonPrimario("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        botones_layout.addWidget(btn_cerrar)

        layout.addLayout(botones_layout)

    def _eliminar_receta(self):
        """Confirma y elimina la receta personalizada."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Eliminar receta")
        msg.setText(f"¿Estás seguro de que quieres eliminar '{self.comida['nombre']}'?")
        msg.setInformativeText("Esta acción no se puede deshacer.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        estilo_base = """
            QPushButton {
                min-height: 36px;
                min-width: 90px;
                border-radius: 6px;
                padding: 6px 18px;
                font-size: 13px;
            }
        """
        btn_yes = msg.button(QMessageBox.StandardButton.Yes)
        btn_yes.setText("Sí, eliminar")
        btn_yes.setStyleSheet(estilo_base + f"""
            QPushButton {{
                background-color: {Colores.ERROR};
                color: white;
                border: none;
            }}
            QPushButton:hover {{ background-color: #c0392b; }}
        """)

        btn_no = msg.button(QMessageBox.StandardButton.No)
        btn_no.setText("Cancelar")
        btn_no.setStyleSheet(estilo_base + f"""
            QPushButton {{
                background-color: transparent;
                color: {Colores.PRIMARIO};
                border: 2px solid {Colores.PRIMARIO};
            }}
            QPushButton:hover {{ background-color: #e8f5e9; }}
        """)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            eliminar_comida(self.comida['id'], self.usuario_id)
            self.done(2)  # Código 2 = receta eliminada


class RecetasView(QWidget):
    """Vista de recetas."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.todas_comidas = []
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz de recetas."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header fijo FUERA del scroll
        header_widget = QWidget()
        header_widget.setStyleSheet(f"background-color: {Colores.FONDO};")
        header_outer = QVBoxLayout(header_widget)
        header_outer.setContentsMargins(30, 25, 30, 15)
        header_outer.setSpacing(10)

        # Título y botón
        header_layout = QHBoxLayout()
        titulo = TituloSeccion("Recetas")
        header_layout.addWidget(titulo)
        header_layout.addStretch()

        btn_crear = BotonPrimario("+ Crear Comida")
        btn_crear.clicked.connect(self._mostrar_dialogo_crear)
        header_layout.addWidget(btn_crear)

        header_outer.addLayout(header_layout)

        subtitulo = SubtituloSeccion("Explora recetas peruanas saludables con ingredientes y pasos detallados")
        header_outer.addWidget(subtitulo)

        # Filtros
        filtros_card = Card()
        filtros_layout = QHBoxLayout(filtros_card)
        filtros_layout.setContentsMargins(20, 15, 20, 15)
        filtros_layout.setSpacing(20)

        tipo_label = QLabel("Filtrar por tipo:")
        tipo_label.setFont(QFont('Inter', 11))
        tipo_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        filtros_layout.addWidget(tipo_label)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Todos", "Desayuno", "Almuerzo", "Cena", "Snack"])
        self.tipo_combo.setMinimumHeight(40)
        self.tipo_combo.setMinimumWidth(200)
        self.tipo_combo.currentTextChanged.connect(self._filtrar_recetas)
        filtros_layout.addWidget(self.tipo_combo)

        buscar_label = QLabel("Buscar:")
        buscar_label.setFont(QFont('Inter', 11))
        buscar_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        filtros_layout.addWidget(buscar_label)

        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Nombre de la receta...")
        self.buscar_input.setMinimumHeight(40)
        self.buscar_input.setMinimumWidth(250)
        self.buscar_input.textChanged.connect(self._filtrar_recetas)
        filtros_layout.addWidget(self.buscar_input)

        filtros_layout.addStretch()
        header_outer.addWidget(filtros_card)

        self.contador_label = QLabel("")
        self.contador_label.setFont(QFont('Inter', 11))
        self.contador_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        header_outer.addWidget(self.contador_label)

        layout.addWidget(header_widget)

        # Scroll area solo para las tarjetas de recetas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {Colores.FONDO};")
        self.recetas_container = scroll_content
        self.recetas_layout = QVBoxLayout(scroll_content)
        self.recetas_layout.setContentsMargins(30, 10, 30, 30)
        self.recetas_layout.setSpacing(15)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)

    def actualizar_datos(self):
        """Actualiza los datos de recetas."""
        # Obtener todas las comidas (del sistema y personalizadas del usuario)
        comidas_sistema = obtener_comidas()
        usuario = self.controller.usuario_actual
        if usuario:
            comidas_personalizadas = obtener_recetas_usuario(usuario['id'])
            self.todas_comidas = comidas_sistema + comidas_personalizadas
        else:
            self.todas_comidas = comidas_sistema
        self._filtrar_recetas()

    def _filtrar_recetas(self):
        """Filtra las recetas según los criterios."""
        # Limpiar layout
        while self.recetas_layout.count():
            item = self.recetas_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Aplicar filtros
        comidas_filtradas = self.todas_comidas

        # Filtro por tipo
        tipo_texto = self.tipo_combo.currentText()
        if tipo_texto != "Todos":
            tipo = tipo_texto.lower()
            comidas_filtradas = [c for c in comidas_filtradas if c['tipo'] == tipo]

        # Filtro por búsqueda
        busqueda = self.buscar_input.text().strip().lower()
        if busqueda:
            comidas_filtradas = [c for c in comidas_filtradas if busqueda in c['nombre'].lower()]

        # Actualizar contador
        self.contador_label.setText(f"Mostrando {len(comidas_filtradas)} receta(s)")

        # Mostrar recetas
        if comidas_filtradas:
            for comida in comidas_filtradas:
                card = ComidaCard(comida, mostrar_add=False)
                card.clicked.connect(self._mostrar_detalle)
                self.recetas_layout.addWidget(card)
        else:
            empty_label = QLabel("No se encontraron recetas")
            empty_label.setFont(QFont('Inter', 12))
            empty_label.setStyleSheet(f"color: {Colores.TEXTO_CLARO}; background-color: transparent;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setMinimumHeight(100)
            self.recetas_layout.addWidget(empty_label)

    def _mostrar_dialogo_crear(self):
        """Muestra el diálogo para crear una comida personalizada."""
        usuario = self.controller.usuario_actual
        if not usuario:
            return
        dialogo = CrearComidaDialog(usuario['id'], self)
        if dialogo.exec() == CrearComidaDialog.DialogCode.Accepted:
            self.actualizar_datos()

    def _mostrar_detalle(self, comida):
        """Muestra el detalle de una receta."""
        usuario = self.controller.usuario_actual
        usuario_id = usuario['id'] if usuario else None
        dialogo = DetalleRecetaDialog(comida, usuario_id, self)
        resultado = dialogo.exec()
        if resultado == 2:  # Receta eliminada
            self.actualizar_datos()
