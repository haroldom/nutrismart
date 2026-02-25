"""
Vista de Seguimiento/Tracker de comidas.
"""
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QPushButton, QDialog, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.styles import Colores
from ui.icons import Ph
from ui.components import (
    Card, ComidaCard, TituloSeccion, SubtituloSeccion,
    BotonPrimario, BotonSecundario, ProgressBarCustom, StatCard, BotonSmall
)
from database.models import (
    obtener_comidas, obtener_registro_hoy, registrar_comida_diaria,
    obtener_meta_diaria, obtener_recetas_usuario, eliminar_registro,
    verificar_meta_cumplida, actualizar_rachas_usuario
)
from services.calculadora import calcular_todo


class AgregarComidaDialog(QDialog):
    """Diálogo para agregar una comida al registro."""

    def __init__(self, comidas, parent=None):
        super().__init__(parent)
        self.comida_seleccionada = None
        self.comidas = comidas
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz del diálogo."""
        self.setWindowTitle("Agregar Comida")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        titulo = QLabel("Selecciona una comida para agregar")
        titulo.setFont(QFont('Inter', 16, QFont.Weight.Bold))
        titulo.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        layout.addWidget(titulo)

        # Filtro por tipo
        filtro_layout = QHBoxLayout()
        filtro_label = QLabel("Filtrar por tipo:")
        filtro_label.setFont(QFont('Inter', 11))
        filtro_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        filtro_layout.addWidget(filtro_label)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Todos", "Desayuno", "Almuerzo", "Cena", "Snack"])
        self.tipo_combo.setMinimumHeight(40)
        self.tipo_combo.currentTextChanged.connect(self._filtrar_comidas)
        filtro_layout.addWidget(self.tipo_combo, 1)

        layout.addLayout(filtro_layout)

        # Scroll de comidas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: 1px solid #e0e0e0; border-radius: 5px; }")

        scroll_content = QWidget()
        self.comidas_layout = QVBoxLayout(scroll_content)
        self.comidas_layout.setSpacing(10)
        self.comidas_layout.setContentsMargins(10, 10, 10, 10)

        self._mostrar_comidas(self.comidas)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.addStretch()

        btn_cancelar = BotonSecundario("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancelar)

        layout.addLayout(botones_layout)

    def _mostrar_comidas(self, comidas):
        """Muestra las comidas en la lista."""
        # Limpiar layout
        while self.comidas_layout.count():
            item = self.comidas_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Agregar comidas
        for comida in comidas:
            card = ComidaCard(comida, mostrar_add=False)
            card.clicked.connect(self._seleccionar_comida)
            self.comidas_layout.addWidget(card)

        self.comidas_layout.addStretch()

    def _filtrar_comidas(self, tipo_texto):
        """Filtra las comidas por tipo."""
        if tipo_texto == "Todos":
            comidas_filtradas = self.comidas
        else:
            tipo = tipo_texto.lower()
            comidas_filtradas = [c for c in self.comidas if c['tipo'] == tipo]

        self._mostrar_comidas(comidas_filtradas)

    def _seleccionar_comida(self, comida):
        """Selecciona una comida y cierra el diálogo."""
        self.comida_seleccionada = comida
        self.accept()


class TrackerView(QWidget):
    """Vista de seguimiento de comidas."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz del tracker."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header fijo FUERA del scroll
        header_widget = QWidget()
        header_widget.setStyleSheet(f"background-color: {Colores.FONDO};")
        header_outer = QVBoxLayout(header_widget)
        header_outer.setContentsMargins(30, 25, 30, 15)
        header_outer.setSpacing(5)

        header_layout = QHBoxLayout()
        titulo = TituloSeccion("Seguimiento Diario")
        header_layout.addWidget(titulo)
        header_layout.addStretch()

        btn_agregar = BotonPrimario("+ Agregar Comida")
        btn_agregar.clicked.connect(self._mostrar_dialogo_agregar)
        header_layout.addWidget(btn_agregar)

        header_outer.addLayout(header_layout)

        subtitulo = SubtituloSeccion(f"Registro de hoy - {datetime.now().strftime('%d/%m/%Y')}")
        header_outer.addWidget(subtitulo)

        layout.addWidget(header_widget)

        # Scroll area solo para el contenido dinámico
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {Colores.FONDO};")
        self.content_layout = QVBoxLayout(scroll_content)
        self.content_layout.setContentsMargins(30, 10, 30, 30)
        self.content_layout.setSpacing(25)

        # Resumen del día (se crea en actualizar_datos)
        self.resumen_container = QWidget()
        self.resumen_layout = QVBoxLayout(self.resumen_container)
        self.resumen_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.resumen_container)

        # Comidas registradas
        self.comidas_titulo = TituloSeccion("Comidas Registradas Hoy")
        self.content_layout.addWidget(self.comidas_titulo)

        self.comidas_container = QWidget()
        self.comidas_list_layout = QVBoxLayout(self.comidas_container)
        self.comidas_list_layout.setContentsMargins(0, 0, 0, 0)
        self.comidas_list_layout.setSpacing(10)
        self.content_layout.addWidget(self.comidas_container)

        self.content_layout.addStretch()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)

    def actualizar_datos(self):
        """Actualiza los datos del tracker."""
        usuario = self.controller.usuario_actual
        if not usuario:
            return

        # Limpiar contenido previo
        self._limpiar_layout(self.resumen_layout)
        self._limpiar_layout(self.comidas_list_layout)

        # Obtener datos
        registro_hoy = obtener_registro_hoy(usuario['id'])
        resultados = calcular_todo(
            usuario['peso'], usuario['altura'], usuario['edad'],
            usuario['sexo'], usuario['objetivo'],
            usuario.get('nivel_actividad', 'sedentario')
        )

        # Resumen de calorías y macros
        objetivo_cal = resultados['calorias_objetivo']
        consumidas_cal = registro_hoy.get('total_calorias', 0) if registro_hoy else 0
        restantes_cal = max(0, objetivo_cal - consumidas_cal)
        porcentaje = min(int((consumidas_cal / objetivo_cal) * 100), 100) if objetivo_cal > 0 else 0

        # Card de resumen
        resumen_card = Card()
        resumen_card_layout = QVBoxLayout(resumen_card)
        resumen_card_layout.setContentsMargins(25, 20, 25, 20)
        resumen_card_layout.setSpacing(15)

        # Título del resumen
        resumen_titulo = QLabel("Resumen Nutricional")
        resumen_titulo.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        resumen_titulo.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        resumen_card_layout.addWidget(resumen_titulo)

        # Stats de calorías - mini cards con color
        cal_stats_layout = QHBoxLayout()
        cal_stats_layout.setSpacing(15)

        color_restantes = Colores.EXITO if restantes_cal > 0 else Colores.ERROR
        stats_data = [
            ("Calorías Objetivo",  objetivo_cal,   "kcal", Ph.FIRE,       Colores.PRIMARIO),
            ("Consumidas Hoy",     consumidas_cal, "kcal", Ph.FORK_KNIFE, Colores.SECUNDARIO),
            ("Restantes",          restantes_cal,  "kcal", Ph.CHART_BAR,  color_restantes),
        ]

        for titulo, valor, unidad, icono, color in stats_data:
            stat = StatCard(titulo, valor, unidad, icono, color)
            cal_stats_layout.addWidget(stat)

        cal_stats_layout.addStretch()
        resumen_card_layout.addLayout(cal_stats_layout)

        # Barra de progreso
        progress_label = QLabel(f"Progreso: {porcentaje}%")
        progress_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        color_prog = Colores.EXITO if porcentaje >= 80 else (Colores.ADVERTENCIA if porcentaje >= 50 else Colores.ERROR)
        progress_label.setStyleSheet(f"color: {color_prog}; background-color: transparent;")
        resumen_card_layout.addWidget(progress_label)

        progress_bar = ProgressBarCustom(color_prog)
        progress_bar.setMaximum(100)
        progress_bar.setValue(porcentaje)
        resumen_card_layout.addWidget(progress_bar)

        # Macros - mini cards con color
        if registro_hoy:
            macros_layout = QHBoxLayout()
            macros_layout.setSpacing(15)

            macros_data = [
                ("Proteínas",     registro_hoy.get('total_proteinas', 0), resultados['proteinas_g'],     Ph.BARBELL, "#e74c3c"),
                ("Carbohidratos", registro_hoy.get('total_carbs', 0),     resultados['carbohidratos_g'], Ph.BOWL,    "#f39c12"),
                ("Grasas",        registro_hoy.get('total_grasas', 0),    resultados['grasas_g'],        Ph.DROP,    "#9b59b6"),
            ]

            for nombre, consumido, objetivo, icono, color in macros_data:
                macro_card = StatCard(nombre, consumido, f"/ {objetivo}g", icono, color)
                macros_layout.addWidget(macro_card)

            macros_layout.addStretch()
            resumen_card_layout.addLayout(macros_layout)

        self.resumen_layout.addWidget(resumen_card)

        # Lista de comidas registradas
        if registro_hoy and 'comidas' in registro_hoy:
            for reg in registro_hoy['comidas']:
                reg_id = reg.get('id')

                row_card = Card()
                row_layout = QHBoxLayout(row_card)
                row_layout.setContentsMargins(15, 12, 15, 12)
                row_layout.setSpacing(15)

                # Icono tipo
                icono_lbl = QLabel(Ph.FORK_KNIFE)
                icono_lbl.setFont(QFont('Phosphor', 20))
                icono_lbl.setStyleSheet(f"color: {Colores.PRIMARIO}; background: transparent;")
                icono_lbl.setFixedWidth(28)
                icono_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                row_layout.addWidget(icono_lbl)

                # Info nombre + macros
                info_col = QVBoxLayout()
                info_col.setSpacing(3)

                nombre_lbl = QLabel(reg.get('nombre_comida', ''))
                nombre_lbl.setFont(QFont('Inter', 13, QFont.Weight.Bold))
                nombre_lbl.setStyleSheet(f"color: {Colores.TEXTO}; background: transparent;")
                info_col.addWidget(nombre_lbl)

                tipo_txt = reg.get('tipo_comida', '').title()
                cals = reg.get('calorias', 0)
                prot = reg.get('proteinas', 0)
                carbs_v = reg.get('carbs', 0)
                grasas_v = reg.get('grasas', 0)
                macros_lbl = QLabel(
                    f"{tipo_txt}  ·  {cals} kcal  ·  P {prot}g  C {carbs_v}g  G {grasas_v}g"
                )
                macros_lbl.setFont(QFont('Inter', 10))
                macros_lbl.setStyleSheet(
                    f"color: {Colores.TEXTO_SECUNDARIO}; background: transparent;"
                )
                info_col.addWidget(macros_lbl)

                row_layout.addLayout(info_col, 1)

                # Hora
                hora = reg.get('hora', '')
                if hora:
                    hora_lbl = QLabel(hora)
                    hora_lbl.setFont(QFont('Inter', 10))
                    hora_lbl.setStyleSheet(
                        f"color: {Colores.TEXTO_CLARO}; background: transparent;"
                    )
                    hora_lbl.setAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    row_layout.addWidget(hora_lbl)

                # Botón eliminar
                btn_del = BotonSmall("Eliminar", color=Colores.ERROR)
                btn_del.clicked.connect(
                    lambda checked=False, rid=reg_id: self._eliminar_registro(rid)
                )
                row_layout.addWidget(btn_del)

                self.comidas_list_layout.addWidget(row_card)
        else:
            empty_label = QLabel("No has registrado ninguna comida hoy")
            empty_label.setFont(QFont('Inter', 12))
            empty_label.setStyleSheet(f"color: {Colores.TEXTO_CLARO}; background-color: transparent;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setMinimumHeight(100)
            self.comidas_list_layout.addWidget(empty_label)

    def _limpiar_layout(self, layout):
        """Limpia un layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _mostrar_dialogo_agregar(self):
        """Muestra el diálogo para agregar una comida."""
        usuario = self.controller.usuario_actual
        if not usuario:
            return

        comidas_sistema = obtener_comidas()
        comidas_personalizadas = obtener_recetas_usuario(usuario['id'])
        comidas = comidas_sistema + comidas_personalizadas
        dialogo = AgregarComidaDialog(comidas, self)

        if dialogo.exec() == QDialog.DialogCode.Accepted and dialogo.comida_seleccionada:
            comida = dialogo.comida_seleccionada

            # Registrar la comida
            try:
                registrar_comida_diaria(
                    usuario['id'],
                    comida['id'],
                    comida['nombre'],
                    comida['tipo'],
                    comida['calorias'],
                    comida['proteinas'],
                    comida['carbs'],
                    comida['grasas']
                )

                self.controller.mostrar_mensaje(
                    "Comida agregada",
                    f"Se agregó {comida['nombre']} a tu registro diario.",
                    "success"
                )

                # Actualizar vista
                self.actualizar_datos()

            except Exception as e:
                self.controller.mostrar_mensaje(
                    "Error",
                    f"Error al agregar comida: {str(e)}",
                    "error"
                )

    def _eliminar_registro(self, reg_id):
        """Elimina un registro de comida del día."""
        usuario = self.controller.usuario_actual
        if not usuario or not reg_id:
            return

        try:
            eliminar_registro(reg_id, usuario['id'])
            self.actualizar_datos()
        except Exception as e:
            self.controller.mostrar_mensaje(
                "Error",
                f"Error al eliminar registro: {str(e)}",
                "error"
            )
