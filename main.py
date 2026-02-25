"""
NutriSmart - Aplicación de nutrición personalizada
Punto de entrada principal con PyQt6
"""
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase

from database.db import init_db, poblar_comidas, actualizar_comidas_default
from database.models import crear_meta_diaria
from services.calculadora import calcular_todo
from ui.styles import GLOBAL_STYLE, Colores
from ui.login import LoginWidget
from ui.registro import RegistroWidget
from ui.main_window import MainAppWidget


class NutriSmartApp(QMainWindow):
    """Aplicación principal de NutriSmart."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NutriSmart - Tu Asistente Nutricional")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)

        # Variables de estado
        self.usuario_actual = None
        self.resultados = None
        self.menu = None

        # Widget principal con stack
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Crear vistas de autenticación
        self.login_widget = LoginWidget(self)
        self.registro_widget = RegistroWidget(self)
        self.main_app_widget = None  # Se crea al iniciar sesión

        # Agregar al stack
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.registro_widget)

        # Mostrar login
        self.mostrar_login()

        # Centrar ventana
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def mostrar_login(self):
        """Muestra la pantalla de login."""
        self.stack.setCurrentWidget(self.login_widget)

    def mostrar_registro(self):
        """Muestra la pantalla de registro."""
        self.stack.setCurrentWidget(self.registro_widget)

    def iniciar_sesion(self, usuario):
        """Inicia sesión con el usuario dado."""
        self.usuario_actual = usuario

        # Crear/actualizar meta diaria con los objetivos actuales del usuario
        resultados = calcular_todo(
            usuario['peso'], usuario['altura'], usuario['edad'],
            usuario['sexo'], usuario['objetivo'],
            usuario.get('nivel_actividad', 'sedentario')
        )
        crear_meta_diaria(
            usuario['id'],
            resultados['calorias_objetivo'],
            resultados['proteinas_g'],
            resultados['carbohidratos_g'],
            resultados['grasas_g']
        )

        # Crear o actualizar el widget principal
        if self.main_app_widget:
            self.stack.removeWidget(self.main_app_widget)
            self.main_app_widget.deleteLater()

        self.main_app_widget = MainAppWidget(self)
        self.stack.addWidget(self.main_app_widget)
        self.stack.setCurrentWidget(self.main_app_widget)

    def navegar_a(self, seccion):
        """Navega a una sección de la app principal."""
        if self.main_app_widget:
            self.main_app_widget._navegar_a(seccion)

    def cerrar_sesion(self):
        """Cierra la sesión actual."""
        self.usuario_actual = None
        self.resultados = None
        self.menu = None

        if self.main_app_widget:
            self.stack.removeWidget(self.main_app_widget)
            self.main_app_widget.deleteLater()
            self.main_app_widget = None

        self.login_widget.limpiar_campos()
        self.mostrar_login()

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """Muestra un mensaje al usuario."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        if tipo == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif tipo == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif tipo == "success":
            msg_box.setIcon(QMessageBox.Icon.Information)
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)

        btn_ok = msg_box.button(QMessageBox.StandardButton.Ok)
        btn_ok.setText("Aceptar")
        btn_ok.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colores.PRIMARIO};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                min-height: 36px;
                min-width: 90px;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {Colores.PRIMARIO_OSCURO}; }}
        """)

        msg_box.exec()


def main():
    """Función principal."""
    # Inicializar base de datos
    init_db()
    poblar_comidas()
    actualizar_comidas_default()

    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Registrar fuentes personalizadas
    fonts_dir = os.path.join(os.path.dirname(__file__), 'assets', 'fonts')
    QFontDatabase.addApplicationFont(os.path.join(fonts_dir, 'Inter.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(fonts_dir, 'Phosphor.ttf'))

    # Establecer Inter como fuente por defecto
    app.setFont(QFont('Inter', 11))

    # Aplicar estilos globales
    app.setStyleSheet(GLOBAL_STYLE)

    # Crear y mostrar ventana principal
    window = NutriSmartApp()
    window.show()

    # Ejecutar loop de eventos
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
