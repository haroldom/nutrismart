"""
Ventana principal de la aplicación con navegación lateral.
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QStackedWidget, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from ui.styles import Colores
from ui.icons import Ph
from ui.components import NavItem, BotonSmall, Separador
from ui.views.dashboard import DashboardView
from ui.views.perfil import PerfilView
from ui.views.tracker import TrackerView
from ui.views.recetas import RecetasView
from ui.views.logros import LogrosView


class MainAppWidget(QWidget):
    """Widget principal de la aplicación con sidebar y contenido."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.nav_items = {}
        self._crear_ui()

    def _crear_ui(self):
        """Crea la interfaz principal."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = self._crear_sidebar()
        layout.addWidget(self.sidebar)

        # Contenido principal
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"background-color: {Colores.FONDO};")

        # Crear vistas
        self.dashboard_view = DashboardView(self.controller)
        self.perfil_view = PerfilView(self.controller)
        self.tracker_view = TrackerView(self.controller)
        self.recetas_view = RecetasView(self.controller)
        self.logros_view = LogrosView(self.controller)

        # Agregar al stack
        self.content_stack.addWidget(self.dashboard_view)
        self.content_stack.addWidget(self.perfil_view)
        self.content_stack.addWidget(self.tracker_view)
        self.content_stack.addWidget(self.recetas_view)
        self.content_stack.addWidget(self.logros_view)

        layout.addWidget(self.content_stack, 1)

        # Mostrar dashboard por defecto
        self._navegar_a('dashboard')

    def _crear_sidebar(self):
        """Crea la barra lateral de navegación."""
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colores.FONDO_CARD};
                border-right: 1px solid {Colores.BORDE};
            }}
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header con logo
        header = QFrame()
        header.setStyleSheet(f"background-color: {Colores.PRIMARIO}; border: none;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 25, 20, 25)

        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(10)

        logo_label = QLabel()
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'assets', 'imgs', 'nutrismart.png'
        )
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                36, 36,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText(Ph.LEAF)
            logo_label.setFont(QFont('Phosphor', 28))
            logo_label.setStyleSheet("color: white; background: transparent;")
        logo_label.setStyleSheet("background: transparent;")
        logo_layout.addWidget(logo_label)

        titulo = QLabel("NutriSmart")
        titulo.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        titulo.setStyleSheet("color: white; background: transparent;")
        logo_layout.addWidget(titulo)
        logo_layout.addStretch()

        header_layout.addLayout(logo_layout)

        # Info del usuario
        usuario = self.controller.usuario_actual
        if usuario:
            user_name = QLabel(usuario['nombre'])
            user_name.setFont(QFont('Inter', 12, QFont.Weight.Bold))
            user_name.setStyleSheet("color: rgba(255,255,255,0.95); background: transparent;")
            header_layout.addWidget(user_name)

            user_email = QLabel(usuario['email'])
            user_email.setFont(QFont('Inter', 10))
            user_email.setStyleSheet("color: rgba(255,255,255,0.7); background: transparent;")
            header_layout.addWidget(user_email)

        layout.addWidget(header)

        # Navegación
        nav_container = QWidget()
        nav_container.setStyleSheet("background: transparent;")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 15, 0, 15)
        nav_layout.setSpacing(5)

        # Items de navegación
        nav_items_data = [
            ('dashboard', 'Dashboard',    Ph.HOUSE),
            ('perfil',    'Mi Perfil',    Ph.USER),
            ('tracker',   'Seguimiento',  Ph.LIST),
            ('recetas',   'Recetas',      Ph.FORK_KNIFE),
            ('logros',    'Logros',       Ph.TROPHY),
        ]

        for key, texto, icono in nav_items_data:
            item = NavItem(texto, icono, activo=(key == 'dashboard'))
            item.clicked.connect(lambda checked=False, k=key: self._navegar_a(k))
            nav_layout.addWidget(item)
            self.nav_items[key] = item

        nav_layout.addStretch()

        # Separador
        sep = Separador()
        nav_layout.addWidget(sep)

        # Botón cerrar sesión
        logout_container = QWidget()
        logout_container.setStyleSheet("background: transparent;")
        logout_layout = QHBoxLayout(logout_container)
        logout_layout.setContentsMargins(15, 15, 15, 15)

        logout_btn = BotonSmall("Cerrar Sesión", color=Colores.ERROR)
        logout_btn.clicked.connect(self._cerrar_sesion)
        logout_layout.addWidget(logout_btn)
        logout_layout.addStretch()

        nav_layout.addWidget(logout_container)

        layout.addWidget(nav_container, 1)

        return sidebar

    def _navegar_a(self, seccion):
        """Navega a una sección específica."""
        # Actualizar estados de navegación
        for key, item in self.nav_items.items():
            item.set_activo(key == seccion)

        # Cambiar vista
        vistas = {
            'dashboard': (0, self.dashboard_view),
            'perfil': (1, self.perfil_view),
            'tracker': (2, self.tracker_view),
            'recetas': (3, self.recetas_view),
            'logros': (4, self.logros_view),
        }

        if seccion in vistas:
            index, vista = vistas[seccion]
            self.content_stack.setCurrentIndex(index)

            # Actualizar datos si la vista tiene el método
            if hasattr(vista, 'actualizar_datos'):
                vista.actualizar_datos()

    def _cerrar_sesion(self):
        """Cierra la sesión del usuario."""
        self.controller.cerrar_sesion()
