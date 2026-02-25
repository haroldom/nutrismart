import tkinter as tk
from tkinter import ttk
from services.menu_generator import generar_menu_diario


class ResultadosFrame(tk.Frame):
    """Frame de resultados nutricionales y menú."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        self.crear_widgets()

    def crear_boton(self, parent, texto, comando, color='#3498db', hover_color='#2980b9'):
        """Crea un botón con Frame para que el color funcione en macOS."""
        btn_frame = tk.Frame(parent, bg=color)
        btn = tk.Label(
            btn_frame,
            text=texto,
            font=('Helvetica', 11),
            bg=color,
            fg='white',
            cursor='hand2',
            padx=20,
            pady=10
        )
        btn.pack()
        btn.bind('<Button-1>', lambda e: comando())
        btn.bind('<Enter>', lambda e: btn.config(bg=hover_color))
        btn.bind('<Leave>', lambda e: btn.config(bg=color))
        return btn_frame

    def crear_boton_small(self, parent, texto, comando, color='#1b5e20', hover_color='#0d3d10'):
        """Crea un botón pequeño."""
        btn_frame = tk.Frame(parent, bg=color)
        btn = tk.Label(
            btn_frame,
            text=texto,
            font=('Helvetica', 9),
            bg=color,
            fg='white',
            cursor='hand2',
            padx=15,
            pady=5
        )
        btn.pack()
        btn.bind('<Button-1>', lambda e: comando())
        btn.bind('<Enter>', lambda e: btn.config(bg=hover_color))
        btn.bind('<Leave>', lambda e: btn.config(bg=color))
        return btn_frame

    def crear_widgets(self):
        # Header
        header = tk.Frame(self, bg='#2e7d32', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg='#2e7d32')
        header_content.pack(fill='x', padx=20, pady=10)

        tk.Label(
            header_content,
            text="NutriSmart",
            font=('Helvetica', 18, 'bold'),
            bg='#2e7d32',
            fg='white'
        ).pack(side='left')

        # Botón volver
        volver_btn = self.crear_boton_small(
            header_content, "Volver",
            lambda: self.controller.mostrar_frame('dashboard')
        )
        volver_btn.pack(side='right')

        # Contenido con scroll
        canvas = tk.Canvas(self, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind mousewheel
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

    def actualizar_resultados(self):
        """Actualiza la vista con los resultados calculados."""
        # Limpiar contenido anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not hasattr(self.controller, 'resultados') or not self.controller.resultados:
            return

        resultados = self.controller.resultados
        menu = self.controller.menu

        # Contenedor principal
        main_container = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
        main_container.pack(fill='x', padx=40, pady=30)

        # Título
        tk.Label(
            main_container,
            text="Tu Plan Nutricional",
            font=('Helvetica', 22, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        ).pack(anchor='w', pady=(0, 20))

        # Cards de calorías y macros
        cards_frame = tk.Frame(main_container, bg='#f0f0f0')
        cards_frame.pack(fill='x', pady=(0, 20))

        # Card TMB
        self.crear_card(cards_frame, "TMB", f"{resultados['tmb']}", "kcal/día", '#3498db')

        # Card Calorías objetivo
        self.crear_card(cards_frame, "Calorías Objetivo", f"{resultados['calorias_objetivo']}", "kcal/día", '#2e7d32')

        # Macronutrientes
        tk.Label(
            main_container,
            text="Distribución de Macronutrientes",
            font=('Helvetica', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        ).pack(anchor='w', pady=(20, 15))

        macros_frame = tk.Frame(main_container, bg='#f0f0f0')
        macros_frame.pack(fill='x', pady=(0, 20))

        self.crear_macro_card(macros_frame, "Proteínas", resultados['proteinas_g'], '#e74c3c', '30%')
        self.crear_macro_card(macros_frame, "Carbohidratos", resultados['carbohidratos_g'], '#f39c12', '45%')
        self.crear_macro_card(macros_frame, "Grasas", resultados['grasas_g'], '#9b59b6', '25%')

        # Menú sugerido
        tk.Label(
            main_container,
            text="Menú Sugerido del Día",
            font=('Helvetica', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        ).pack(anchor='w', pady=(20, 15))

        menu_frame = tk.Frame(main_container, bg='#ffffff', padx=25, pady=20)
        menu_frame.pack(fill='x')

        # Desayuno
        self.crear_comida_item(menu_frame, "Desayuno", menu['desayuno'], '#f39c12')

        ttk.Separator(menu_frame, orient='horizontal').pack(fill='x', pady=15)

        # Almuerzo
        self.crear_comida_item(menu_frame, "Almuerzo", menu['almuerzo'], '#e74c3c')

        ttk.Separator(menu_frame, orient='horizontal').pack(fill='x', pady=15)

        # Cena
        self.crear_comida_item(menu_frame, "Cena", menu['cena'], '#3498db')

        ttk.Separator(menu_frame, orient='horizontal').pack(fill='x', pady=15)

        # Totales del menú
        totales_frame = tk.Frame(menu_frame, bg='#f8f9fa', padx=15, pady=10)
        totales_frame.pack(fill='x')

        tk.Label(
            totales_frame,
            text="TOTALES DEL DÍA",
            font=('Helvetica', 11, 'bold'),
            bg='#f8f9fa',
            fg='#333333'
        ).pack(anchor='w')

        totales_info = tk.Frame(totales_frame, bg='#f8f9fa')
        totales_info.pack(fill='x', pady=(5, 0))

        totales = menu['totales']
        diferencia = menu['diferencia']
        color_dif = '#27ae60' if abs(diferencia) <= 100 else '#e74c3c'

        info_text = f"Calorías: {totales['calorias']} kcal  |  "
        info_text += f"Proteínas: {totales['proteinas']}g  |  "
        info_text += f"Carbs: {totales['carbs']}g  |  "
        info_text += f"Grasas: {totales['grasas']}g"

        tk.Label(
            totales_info,
            text=info_text,
            font=('Helvetica', 10),
            bg='#f8f9fa',
            fg='#666666'
        ).pack(side='left')

        dif_text = f"({'+' if diferencia > 0 else ''}{diferencia} kcal vs objetivo)"
        tk.Label(
            totales_info,
            text=dif_text,
            font=('Helvetica', 10),
            bg='#f8f9fa',
            fg=color_dif
        ).pack(side='left', padx=(10, 0))

        # Botón generar nuevo menú
        nuevo_menu_btn = self.crear_boton(main_container, "Generar Nuevo Menú", self.regenerar_menu)
        nuevo_menu_btn.pack(pady=(20, 30))

    def crear_card(self, parent, titulo, valor, unidad, color):
        card = tk.Frame(parent, bg='#ffffff', padx=25, pady=20)
        card.pack(side='left', padx=(0, 15))

        tk.Label(
            card,
            text=titulo,
            font=('Helvetica', 11),
            bg='#ffffff',
            fg='#666666'
        ).pack()

        tk.Label(
            card,
            text=valor,
            font=('Helvetica', 28, 'bold'),
            bg='#ffffff',
            fg=color
        ).pack()

        tk.Label(
            card,
            text=unidad,
            font=('Helvetica', 10),
            bg='#ffffff',
            fg='#999999'
        ).pack()

    def crear_macro_card(self, parent, nombre, gramos, color, porcentaje):
        card = tk.Frame(parent, bg='#ffffff', padx=20, pady=15)
        card.pack(side='left', padx=(0, 15))

        # Barra de color
        color_bar = tk.Frame(card, bg=color, height=4)
        color_bar.pack(fill='x', pady=(0, 10))

        tk.Label(
            card,
            text=nombre,
            font=('Helvetica', 10),
            bg='#ffffff',
            fg='#666666'
        ).pack()

        tk.Label(
            card,
            text=f"{gramos}g",
            font=('Helvetica', 20, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).pack()

        tk.Label(
            card,
            text=porcentaje,
            font=('Helvetica', 9),
            bg='#ffffff',
            fg=color
        ).pack()

    def crear_comida_item(self, parent, tipo, comida, color):
        item_frame = tk.Frame(parent, bg='#ffffff')
        item_frame.pack(fill='x')

        # Indicador de color
        color_indicator = tk.Frame(item_frame, bg=color, width=4)
        color_indicator.pack(side='left', fill='y', padx=(0, 15))

        content_frame = tk.Frame(item_frame, bg='#ffffff')
        content_frame.pack(side='left', fill='x', expand=True)

        tk.Label(
            content_frame,
            text=tipo.upper(),
            font=('Helvetica', 9, 'bold'),
            bg='#ffffff',
            fg=color
        ).pack(anchor='w')

        tk.Label(
            content_frame,
            text=comida['nombre'],
            font=('Helvetica', 13),
            bg='#ffffff',
            fg='#333333'
        ).pack(anchor='w')

        info_frame = tk.Frame(content_frame, bg='#ffffff')
        info_frame.pack(anchor='w', pady=(5, 0))

        info_text = f"{comida['calorias']} kcal  |  P: {comida['proteinas']}g  |  C: {comida['carbs']}g  |  G: {comida['grasas']}g"
        tk.Label(
            info_frame,
            text=info_text,
            font=('Helvetica', 9),
            bg='#ffffff',
            fg='#888888'
        ).pack()

    def regenerar_menu(self):
        """Genera un nuevo menú aleatorio."""
        if hasattr(self.controller, 'resultados') and self.controller.resultados:
            self.controller.menu = generar_menu_diario(self.controller.resultados['calorias_objetivo'])
            self.actualizar_resultados()
