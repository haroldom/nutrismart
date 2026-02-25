import tkinter as tk
from tkinter import messagebox
from database.models import actualizar_usuario, obtener_usuario_por_id
from services.calculadora import calcular_todo
from services.menu_generator import generar_menu_diario


class DashboardFrame(tk.Frame):
    """Frame principal del dashboard."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        self.crear_widgets()

    def crear_entry(self, parent, width=15):
        """Crea un Entry con estilos consistentes."""
        return tk.Entry(
            parent, width=width, font=('Helvetica', 11),
            bg='white', fg='#333333', insertbackground='#333333',
            relief='flat', highlightthickness=1, highlightbackground='#cccccc',
            highlightcolor='#2e7d32'
        )

    def crear_boton(self, parent, texto, comando, color='#2e7d32', hover_color='#1b5e20'):
        """Crea un botón con Frame para que el color funcione en macOS."""
        btn_frame = tk.Frame(parent, bg=color)
        btn = tk.Label(
            btn_frame,
            text=texto,
            font=('Helvetica', 12, 'bold'),
            bg=color,
            fg='white',
            cursor='hand2',
            padx=30,
            pady=12
        )
        btn.pack(fill='x')
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

        # Botón cerrar sesión
        logout_btn = self.crear_boton_small(header_content, "Cerrar Sesión", self.cerrar_sesion)
        logout_btn.pack(side='right')

        self.bienvenida_label = tk.Label(
            header_content,
            text="Bienvenido",
            font=('Helvetica', 11),
            bg='#2e7d32',
            fg='white'
        )
        self.bienvenida_label.pack(side='right', padx=(0, 20))

        # Contenido principal
        main_content = tk.Frame(self, bg='#f0f0f0')
        main_content.pack(fill='both', expand=True, padx=40, pady=30)

        # Título
        tk.Label(
            main_content,
            text="Actualiza tus datos",
            font=('Helvetica', 20, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        ).pack(anchor='w', pady=(0, 20))

        # Frame del formulario
        form_frame = tk.Frame(main_content, bg='#ffffff', padx=30, pady=25)
        form_frame.pack(fill='x')

        # Grid de campos
        grid_frame = tk.Frame(form_frame, bg='#ffffff')
        grid_frame.pack(fill='x')

        # Fila 1: Edad y Peso
        self.crear_campo_grid(grid_frame, "Edad (años)", 0, 0)
        self.edad_entry = self.crear_entry(grid_frame)
        self.edad_entry.grid(row=0, column=1, padx=(0, 40), pady=10, ipady=8, ipadx=10)

        self.crear_campo_grid(grid_frame, "Peso (kg)", 0, 2)
        self.peso_entry = self.crear_entry(grid_frame)
        self.peso_entry.grid(row=0, column=3, pady=10, ipady=8, ipadx=10)

        # Fila 2: Altura y Sexo
        self.crear_campo_grid(grid_frame, "Altura (cm)", 1, 0)
        self.altura_entry = self.crear_entry(grid_frame)
        self.altura_entry.grid(row=1, column=1, padx=(0, 40), pady=10, ipady=8, ipadx=10)

        self.crear_campo_grid(grid_frame, "Sexo", 1, 2)
        self.sexo_var = tk.StringVar(value='masculino')
        sexo_frame = tk.Frame(grid_frame, bg='#ffffff')
        sexo_frame.grid(row=1, column=3, sticky='w', pady=10)
        tk.Radiobutton(sexo_frame, text='M', variable=self.sexo_var, value='masculino',
                       bg='#ffffff', fg='#333333', activebackground='#ffffff',
                       selectcolor='#ffffff', font=('Helvetica', 10)).pack(side='left')
        tk.Radiobutton(sexo_frame, text='F', variable=self.sexo_var, value='femenino',
                       bg='#ffffff', fg='#333333', activebackground='#ffffff',
                       selectcolor='#ffffff', font=('Helvetica', 10)).pack(side='left', padx=(10, 0))

        # Fila 3: Objetivo
        tk.Label(
            form_frame,
            text="Objetivo",
            font=('Helvetica', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).pack(anchor='w', pady=(20, 10))

        self.objetivo_var = tk.StringVar(value='mantener')
        objetivo_frame = tk.Frame(form_frame, bg='#ffffff')
        objetivo_frame.pack(anchor='w')

        objetivos = [
            ('Bajar de peso', 'bajar'),
            ('Mantener peso', 'mantener'),
            ('Subir de peso', 'subir')
        ]

        for texto, valor in objetivos:
            tk.Radiobutton(objetivo_frame, text=texto, variable=self.objetivo_var, value=valor,
                           bg='#ffffff', fg='#333333', activebackground='#ffffff',
                           selectcolor='#ffffff', font=('Helvetica', 10)).pack(side='left', padx=(0, 30))

        # Botón calcular
        calcular_btn = self.crear_boton(form_frame, "Calcular Mi Plan Nutricional", self.calcular)
        calcular_btn.pack(pady=(30, 10))

    def crear_campo_grid(self, parent, texto, row, col):
        tk.Label(
            parent,
            text=texto,
            font=('Helvetica', 10),
            bg='#ffffff',
            fg='#333333'
        ).grid(row=row, column=col, sticky='e', padx=(0, 10), pady=10)

    def actualizar_datos_usuario(self):
        """Actualiza los campos con los datos del usuario actual."""
        if self.controller.usuario_actual:
            usuario = self.controller.usuario_actual
            self.bienvenida_label.config(text=f"Hola, {usuario['nombre']}")

            self.edad_entry.delete(0, tk.END)
            self.edad_entry.insert(0, str(usuario['edad']))

            self.peso_entry.delete(0, tk.END)
            self.peso_entry.insert(0, str(usuario['peso']))

            self.altura_entry.delete(0, tk.END)
            self.altura_entry.insert(0, str(usuario['altura']))

            self.sexo_var.set(usuario['sexo'])
            self.objetivo_var.set(usuario['objetivo'])

    def calcular(self):
        try:
            edad = int(self.edad_entry.get())
            peso = float(self.peso_entry.get())
            altura = float(self.altura_entry.get())
            sexo = self.sexo_var.get()
            objetivo = self.objetivo_var.get()

            # Validaciones
            if edad < 10 or edad > 120:
                messagebox.showwarning("Edad inválida", "La edad debe estar entre 10 y 120 años.")
                return

            if peso < 20 or peso > 300:
                messagebox.showwarning("Peso inválido", "El peso debe estar entre 20 y 300 kg.")
                return

            if altura < 100 or altura > 250:
                messagebox.showwarning("Altura inválida", "La altura debe estar entre 100 y 250 cm.")
                return

            # Actualizar usuario en BD
            if self.controller.usuario_actual:
                actualizar_usuario(
                    self.controller.usuario_actual['id'],
                    self.controller.usuario_actual['nombre'],
                    edad, peso, altura, sexo, objetivo
                )
                # Actualizar datos locales
                self.controller.usuario_actual['edad'] = edad
                self.controller.usuario_actual['peso'] = peso
                self.controller.usuario_actual['altura'] = altura
                self.controller.usuario_actual['sexo'] = sexo
                self.controller.usuario_actual['objetivo'] = objetivo

            # Calcular resultados
            resultados = calcular_todo(peso, altura, edad, sexo, objetivo)
            menu = generar_menu_diario(resultados['calorias_objetivo'])

            # Pasar a resultados
            self.controller.resultados = resultados
            self.controller.menu = menu
            self.controller.mostrar_frame('resultados')

        except ValueError:
            messagebox.showwarning("Datos inválidos", "Por favor ingresa valores numéricos válidos.")

    def cerrar_sesion(self):
        self.controller.usuario_actual = None
        self.controller.mostrar_frame('login')
