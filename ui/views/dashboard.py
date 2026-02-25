"""
Vista del Dashboard principal.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.styles import Colores
from ui.icons import Ph
from ui.components import (
    Card, StatCard, MacroCard, ProgressBarCustom,
    TituloSeccion, BotonPrimario, BotonSecundario
)
from services.calculadora import calcular_todo, calcular_imc
from database.models import (
    obtener_registro_hoy, obtener_meta_diaria, calcular_racha,
    obtener_estadisticas_semana
)


class DashboardView(QWidget):
    """Vista principal del dashboard."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz del dashboard."""
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

        # El contenido se llenará en actualizar_datos
        self._crear_contenido_placeholder()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _crear_contenido_placeholder(self):
        """Crea contenido placeholder inicial."""
        loading = QLabel("Cargando...")
        loading.setFont(QFont('Inter', 14))
        loading.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(loading)

    def _limpiar_contenido(self):
        """Limpia el contenido actual."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._limpiar_sublayout(item.layout())

    def _limpiar_sublayout(self, layout):
        """Limpia recursivamente un sublayout y sus widgets."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._limpiar_sublayout(item.layout())

    def actualizar_datos(self):
        """Actualiza los datos del dashboard."""
        self._limpiar_contenido()

        usuario = self.controller.usuario_actual
        if not usuario:
            return

        # Header de bienvenida
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        bienvenida = QLabel(f"Hola, {usuario['nombre'].split()[0]} 👋")
        bienvenida.setFont(QFont('Inter', 26, QFont.Weight.Bold))
        bienvenida.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        header_layout.addWidget(bienvenida)
        header_layout.addStretch()

        # Racha actual
        racha = calcular_racha(usuario['id'])
        if racha > 0:
            racha_widget = QFrame()
            racha_widget.setStyleSheet(f"""
                background-color: {Colores.ADVERTENCIA};
                border-radius: 20px;
                padding: 8px 16px;
            """)
            racha_layout = QHBoxLayout(racha_widget)
            racha_layout.setContentsMargins(15, 8, 15, 8)

            racha_label = QLabel(f'<span style="font-family: Phosphor;">{Ph.FIRE}</span>&nbsp; {racha} días de racha')
            racha_label.setTextFormat(Qt.TextFormat.RichText)
            racha_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
            racha_label.setStyleSheet("color: white; background: transparent;")
            racha_layout.addWidget(racha_label)

            header_layout.addWidget(racha_widget)

        self.content_layout.addWidget(header)

        # Calcular datos nutricionales
        resultados = calcular_todo(
            usuario['peso'], usuario['altura'], usuario['edad'],
            usuario['sexo'], usuario['objetivo'],
            usuario.get('nivel_actividad', 'sedentario')
        )

        # Cards de estadísticas principales
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        # Calorías objetivo
        cal_card = StatCard(
            "Calorías Objetivo",
            resultados['calorias_objetivo'],
            "kcal/día",
            Ph.FIRE,
            Colores.PRIMARIO
        )
        stats_layout.addWidget(cal_card)

        # TMB
        tmb_card = StatCard(
            "Metabolismo Basal",
            resultados['tmb'],
            "kcal",
            Ph.LIGHTNING,
            Colores.SECUNDARIO
        )
        stats_layout.addWidget(tmb_card)

        # Agua recomendada
        agua_card = StatCard(
            "Agua Recomendada",
            resultados['agua_litros'],
            "litros",
            Ph.DROP,
            "#3498db"
        )
        stats_layout.addWidget(agua_card)

        # IMC
        imc_data = calcular_imc(usuario['peso'], usuario['altura'])
        imc_card = StatCard(
            "IMC",
            imc_data['imc'],
            imc_data['clasificacion'],
            Ph.SCALES,
            imc_data['color']
        )
        stats_layout.addWidget(imc_card)

        self.content_layout.addLayout(stats_layout)

        # Progreso del día
        self.content_layout.addWidget(TituloSeccion("Progreso de Hoy"))

        progreso_card = Card()
        progreso_layout = QVBoxLayout(progreso_card)
        progreso_layout.setContentsMargins(25, 20, 25, 20)
        progreso_layout.setSpacing(20)

        # Obtener registro del día
        registro_hoy = obtener_registro_hoy(usuario['id'])
        calorias_consumidas = registro_hoy.get('total_calorias', 0) if registro_hoy else 0
        objetivo = resultados['calorias_objetivo']
        porcentaje = min(int((calorias_consumidas / objetivo) * 100), 100) if objetivo > 0 else 0

        # Calorías
        cal_progreso = QWidget()
        cal_progreso.setStyleSheet("background-color: transparent;")
        cal_prog_layout = QHBoxLayout(cal_progreso)
        cal_prog_layout.setContentsMargins(0, 0, 0, 0)

        cal_info = QVBoxLayout()
        cal_titulo = QLabel("Calorías consumidas")
        cal_titulo.setFont(QFont('Inter', 12))
        cal_titulo.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        cal_info.addWidget(cal_titulo)

        cal_valor = QLabel(f"{calorias_consumidas} / {objetivo} kcal")
        cal_valor.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        cal_valor.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        cal_info.addWidget(cal_valor)

        cal_prog_layout.addLayout(cal_info)
        cal_prog_layout.addStretch()

        pct_label = QLabel(f"{porcentaje}%")
        pct_label.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        color_pct = Colores.EXITO if porcentaje >= 80 else (Colores.ADVERTENCIA if porcentaje >= 50 else Colores.ERROR)
        pct_label.setStyleSheet(f"color: {color_pct}; background-color: transparent;")
        cal_prog_layout.addWidget(pct_label)

        progreso_layout.addWidget(cal_progreso)

        # Barra de progreso
        progress_bar = ProgressBarCustom(color_pct)
        progress_bar.setMaximum(100)
        progress_bar.setValue(porcentaje)
        progreso_layout.addWidget(progress_bar)

        self.content_layout.addWidget(progreso_card)

        # Acciones rápidas
        self.content_layout.addWidget(TituloSeccion("Acciones Rápidas"))

        acciones_layout = QHBoxLayout()
        acciones_layout.setSpacing(15)

        btn_registrar = BotonPrimario("+ Registrar Comida")
        btn_registrar.clicked.connect(lambda: self.controller.navegar_a('tracker'))
        acciones_layout.addWidget(btn_registrar)

        btn_recetas = BotonSecundario("Ver Recetas / Crear Comida")
        btn_recetas.clicked.connect(lambda: self.controller.navegar_a('recetas'))
        acciones_layout.addWidget(btn_recetas)

        acciones_layout.addStretch()
        self.content_layout.addLayout(acciones_layout)

        # Macronutrientes
        self.content_layout.addWidget(TituloSeccion("Distribución de Macronutrientes"))

        macros_layout = QHBoxLayout()
        macros_layout.setSpacing(20)

        dist = resultados['distribucion']
        macros_data = [
            ("Proteínas", resultados['proteinas_g'], dist['proteinas_pct'], "#e74c3c"),
            ("Carbohidratos", resultados['carbohidratos_g'], dist['carbs_pct'], "#f39c12"),
            ("Grasas", resultados['grasas_g'], dist['grasas_pct'], "#9b59b6"),
        ]

        for nombre, gramos, pct, color in macros_data:
            card = MacroCard(nombre, gramos, pct, color)
            macros_layout.addWidget(card)

        macros_layout.addStretch()
        self.content_layout.addLayout(macros_layout)

        # Info del nivel de actividad
        actividad_card = Card()
        actividad_layout = QHBoxLayout(actividad_card)
        actividad_layout.setContentsMargins(25, 20, 25, 20)

        actividad_icon = QLabel(Ph.BARBELL)
        actividad_icon.setFont(QFont('Phosphor', 28))
        actividad_icon.setStyleSheet(f"color: {Colores.PRIMARIO}; background-color: transparent;")
        actividad_layout.addWidget(actividad_icon)

        actividad_info = QVBoxLayout()
        actividad_titulo = QLabel("Nivel de Actividad")
        actividad_titulo.setFont(QFont('Inter', 11))
        actividad_titulo.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        actividad_info.addWidget(actividad_titulo)

        actividad_valor = QLabel(resultados['nivel_actividad'])
        actividad_valor.setFont(QFont('Inter', 16, QFont.Weight.Bold))
        actividad_valor.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        actividad_info.addWidget(actividad_valor)

        actividad_layout.addLayout(actividad_info)
        actividad_layout.addStretch()

        objetivo_info = QVBoxLayout()
        objetivo_titulo = QLabel("Objetivo")
        objetivo_titulo.setFont(QFont('Inter', 11))
        objetivo_titulo.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        objetivo_info.addWidget(objetivo_titulo)

        objetivos_texto = {'bajar': 'Bajar de peso', 'mantener': 'Mantener peso', 'subir': 'Subir de peso'}
        objetivo_valor = QLabel(objetivos_texto.get(usuario['objetivo'], 'Mantener peso'))
        objetivo_valor.setFont(QFont('Inter', 16, QFont.Weight.Bold))
        objetivo_valor.setStyleSheet(f"color: {Colores.PRIMARIO}; background-color: transparent;")
        objetivo_info.addWidget(objetivo_valor)

        actividad_layout.addLayout(objetivo_info)

        self.content_layout.addWidget(actividad_card)

        # Espaciador final
        self.content_layout.addStretch()
