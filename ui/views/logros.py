"""
Vista de Logros y Rachas.
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
    Card, LogroCard, StatCard, TituloSeccion, SubtituloSeccion, Separador
)
from database.models import (
    obtener_logros_usuario, obtener_todos_logros,
    calcular_racha, obtener_estadisticas_semana
)


class LogrosView(QWidget):
    """Vista de logros y rachas."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz de logros."""
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
        titulo = TituloSeccion("Logros y Rachas")
        self.content_layout.addWidget(titulo)

        subtitulo = SubtituloSeccion("Rastrea tu progreso y desbloquea logros")
        self.content_layout.addWidget(subtitulo)

        # Container de estadísticas de racha (se llena en actualizar_datos)
        self.racha_container = QWidget()
        self.racha_layout = QVBoxLayout(self.racha_container)
        self.racha_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.racha_container)

        # Estadísticas semanales
        self.stats_titulo = TituloSeccion("Estadísticas de la Semana")
        self.content_layout.addWidget(self.stats_titulo)

        self.stats_container = QWidget()
        self.stats_layout = QHBoxLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setSpacing(20)
        self.content_layout.addWidget(self.stats_container)

        # Logros
        self.logros_titulo = TituloSeccion("Tus Logros")
        self.content_layout.addWidget(self.logros_titulo)

        self.logros_container = QWidget()
        self.logros_layout = QVBoxLayout(self.logros_container)
        self.logros_layout.setContentsMargins(0, 0, 0, 0)
        self.logros_layout.setSpacing(15)
        self.content_layout.addWidget(self.logros_container)

        self.content_layout.addStretch()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def actualizar_datos(self):
        """Actualiza los datos de logros."""
        usuario = self.controller.usuario_actual
        if not usuario:
            return

        # Limpiar contenedores
        self._limpiar_layout(self.racha_layout)
        self._limpiar_layout(self.stats_layout)
        self._limpiar_layout(self.logros_layout)

        # Racha actual
        racha_actual = calcular_racha(usuario['id'])
        racha_maxima = usuario.get('racha_maxima', 0)

        # Card de racha - diseño con fondo cálido
        racha_card = Card()
        racha_card.setStyleSheet("""
            QFrame#card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fff8e1, stop:1 #fff3cd);
                border-radius: 12px;
                border: 1px solid #ffe082;
            }
        """)
        racha_card_layout = QVBoxLayout(racha_card)
        racha_card_layout.setContentsMargins(30, 25, 30, 25)
        racha_card_layout.setSpacing(20)

        # Header con icono y título
        racha_header = QHBoxLayout()
        racha_icon_lbl = QLabel(Ph.FIRE)
        racha_icon_lbl.setFont(QFont('Phosphor', 28))
        racha_icon_lbl.setStyleSheet(f"color: {Colores.ADVERTENCIA}; background-color: transparent;")
        racha_header.addWidget(racha_icon_lbl)

        racha_titulo = QLabel("Tu Racha")
        racha_titulo.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        racha_titulo.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        racha_header.addWidget(racha_titulo)
        racha_header.addStretch()
        racha_card_layout.addLayout(racha_header)

        # Stats lado a lado
        racha_stats_layout = QHBoxLayout()
        racha_stats_layout.setSpacing(30)

        # Racha actual
        actual_widget = QWidget()
        actual_widget.setStyleSheet("background-color: transparent;")
        actual_layout = QVBoxLayout(actual_widget)
        actual_layout.setContentsMargins(0, 0, 0, 0)
        actual_layout.setSpacing(4)

        actual_label = QLabel("Racha Actual")
        actual_label.setFont(QFont('Inter', 12))
        actual_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        actual_layout.addWidget(actual_label)

        actual_valor = QLabel(f"{racha_actual}")
        actual_valor.setFont(QFont('Inter', 56, QFont.Weight.Bold))
        color_racha = Colores.EXITO if racha_actual > 0 else Colores.TEXTO_CLARO
        actual_valor.setStyleSheet(f"color: {color_racha}; background-color: transparent;")
        actual_layout.addWidget(actual_valor)

        actual_dias = QLabel("días consecutivos")
        actual_dias.setFont(QFont('Inter', 11))
        actual_dias.setStyleSheet(f"color: {Colores.TEXTO_CLARO}; background-color: transparent;")
        actual_layout.addWidget(actual_dias)

        racha_stats_layout.addWidget(actual_widget)

        # Separador vertical
        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setFrameShape(QFrame.Shape.NoFrame)
        sep.setStyleSheet(f"background-color: {Colores.BORDE};")
        sep.setMinimumHeight(80)
        racha_stats_layout.addWidget(sep)

        # Racha máxima
        maxima_widget = QWidget()
        maxima_widget.setStyleSheet("background-color: transparent;")
        maxima_layout = QVBoxLayout(maxima_widget)
        maxima_layout.setContentsMargins(0, 0, 0, 0)
        maxima_layout.setSpacing(4)

        maxima_label = QLabel("Mejor Racha")
        maxima_label.setFont(QFont('Inter', 12))
        maxima_label.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
        maxima_layout.addWidget(maxima_label)

        maxima_valor = QLabel(f"{racha_maxima}")
        maxima_valor.setFont(QFont('Inter', 56, QFont.Weight.Bold))
        maxima_valor.setStyleSheet(f"color: {Colores.ADVERTENCIA}; background-color: transparent;")
        maxima_layout.addWidget(maxima_valor)

        maxima_dias = QLabel("días")
        maxima_dias.setFont(QFont('Inter', 11))
        maxima_dias.setStyleSheet(f"color: {Colores.TEXTO_CLARO}; background-color: transparent;")
        maxima_layout.addWidget(maxima_dias)

        racha_stats_layout.addWidget(maxima_widget)
        racha_stats_layout.addStretch()
        racha_card_layout.addLayout(racha_stats_layout)

        # Mensaje motivacional
        if racha_actual > 0:
            msg = QLabel(f"¡Excelente! Llevas {racha_actual} día(s) cumpliendo tu meta. ¡Sigue así!")
            msg.setFont(QFont('Inter', 11))
            msg.setStyleSheet(f"color: {Colores.EXITO}; background-color: transparent;")
            msg.setWordWrap(True)
            racha_card_layout.addWidget(msg)
        else:
            msg = QLabel("Registra tus comidas hoy para comenzar una nueva racha.")
            msg.setFont(QFont('Inter', 11))
            msg.setStyleSheet(f"color: {Colores.TEXTO_SECUNDARIO}; background-color: transparent;")
            msg.setWordWrap(True)
            racha_card_layout.addWidget(msg)

        self.racha_layout.addWidget(racha_card)

        # Estadísticas semanales
        stats_semana = obtener_estadisticas_semana(usuario['id'])

        stats_data = [
            ("Días Activos", stats_semana.get('dias_activos', 0), "días", Ph.CALENDAR, Colores.PRIMARIO),
            ("Comidas Registradas", stats_semana.get('comidas_totales', 0), "comidas", Ph.FORK_KNIFE, Colores.SECUNDARIO),
            ("Promedio Calorías", stats_semana.get('promedio_calorias', 0), "kcal", Ph.FIRE, "#f39c12"),
        ]

        for titulo, valor, unidad, icono, color in stats_data:
            card = StatCard(titulo, valor, unidad, icono, color)
            self.stats_layout.addWidget(card)

        self.stats_layout.addStretch()

        # Logros
        logros_usuario = obtener_logros_usuario(usuario['id'])
        todos_logros = obtener_todos_logros()

        # Separar logros desbloqueados y bloqueados
        ids_desbloqueados = {l['logro_id'] for l in logros_usuario}
        logros_desbloqueados = []
        logros_bloqueados = []

        for logro in todos_logros:
            if logro['id'] in ids_desbloqueados:
                # Encontrar fecha de desbloqueo
                for lu in logros_usuario:
                    if lu['logro_id'] == logro['id']:
                        logro['fecha_desbloqueo'] = lu['fecha_desbloqueo']
                        break
                logros_desbloqueados.append(logro)
            else:
                logros_bloqueados.append(logro)

        # Contador de logros
        total = len(todos_logros)
        desbloqueados = len(logros_desbloqueados)
        porcentaje = int((desbloqueados / total) * 100) if total > 0 else 0

        contador_layout = QHBoxLayout()
        contador_label = QLabel(f"Has desbloqueado {desbloqueados} de {total} logros ({porcentaje}%)")
        contador_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        contador_label.setStyleSheet(f"color: {Colores.TEXTO}; background-color: transparent;")
        contador_layout.addWidget(contador_label)
        contador_layout.addStretch()

        self.logros_layout.addLayout(contador_layout)

        # Mostrar logros desbloqueados primero
        if logros_desbloqueados:
            desb_titulo = QLabel("✨ Desbloqueados")
            desb_titulo.setFont(QFont('Inter', 14, QFont.Weight.Bold))
            desb_titulo.setStyleSheet(f"color: {Colores.EXITO}; background-color: transparent;")
            self.logros_layout.addWidget(desb_titulo)

            for logro in logros_desbloqueados:
                card = LogroCard(logro, desbloqueado=True)
                self.logros_layout.addWidget(card)

        # Mostrar logros bloqueados
        if logros_bloqueados:
            bloq_titulo = QLabel("🔒 Por Desbloquear")
            bloq_titulo.setFont(QFont('Inter', 14, QFont.Weight.Bold))
            bloq_titulo.setStyleSheet(f"color: {Colores.TEXTO_CLARO}; background-color: transparent;")
            self.logros_layout.addWidget(bloq_titulo)

            for logro in logros_bloqueados:
                card = LogroCard(logro, desbloqueado=False)
                self.logros_layout.addWidget(card)

    def _limpiar_layout(self, layout):
        """Limpia un layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
