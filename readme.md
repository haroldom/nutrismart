🧠 NutriSmart AI — MVP (versión alcanzable)
🎯 Objetivo del MVP

Crear una app de escritorio que:

✅ calcule calorías diarias
✅ calcule macronutrientes
✅ genere un menú básico peruano
✅ guarde usuarios en una base de datos
✅ tenga interfaz en Tkinter
✅ se pueda exportar a .exe

NO necesitas IA real todavía.
Puedes usar reglas y fórmulas (tu profe seguro espera eso).

🏗️ Estructura del proyecto

Te propongo algo limpio y profesional:

nutrismart/
│
├── main.py              # Punto de entrada
├── ui/
│   ├── login.py
│   ├── registro.py
│   ├── dashboard.py
│   └── resultados.py
│
├── services/
│   ├── calculadora.py   # calorías y macros
│   └── menu_generator.py
│
├── database/
│   ├── db.py            # conexión sqlite
│   └── models.py
│
├── assets/
│   └── icon.ico
│
└── requirements.txt

💡 Esto le encanta a los profes porque se ve ordenado.

🔥 Funcionalidades del MVP
1️⃣ Autenticación básica

Pantallas:

Registro

Login

Datos a guardar:

nombre

edad

peso

altura

sexo

objetivo (bajar peso / mantener / subir)

📌 Base de datos: SQLite (perfecta para el curso).

2️⃣ Calculadora nutricional

Aquí usas fórmula Mifflin-St Jeor (simple y profesional).

🔹 Calorías basales

Hombres:

TMB = 10*peso + 6.25*altura - 5*edad + 5

Mujeres:

TMB = 10*peso + 6.25*altura - 5*edad - 161

Luego ajustas por objetivo:

bajar peso → -500 kcal

mantener → normal

subir → +300 kcal

3️⃣ Distribución de macronutrientes

Algo simple pero realista:

Proteínas: 30%

Carbohidratos: 45%

Grasas: 25%

Convertido a gramos:

proteína = calorías * 0.30 / 4

carbs = calorías * 0.45 / 4

grasas = calorías * 0.25 / 9

💡 Esto ya se siente “inteligente”.

4️⃣ Generador de menú peruano (simple)

Aquí NO necesitas IA.

Haz una base de datos de comidas peruanas:

Tabla comidas
id	nombre	tipo	calorias
1	avena con leche	desayuno	250
2	arroz con pollo	almuerzo	600
3	ensalada de pollo	cena	350
Lógica simple

El programa:

busca comidas por tipo

arma un menú diario

intenta aproximarse a las calorías objetivo

💡 Esto cumple perfectamente como MVP.

🖥️ Flujo de pantallas

Te lo dejo clarito:

Login
  ↓
Registro (si no tiene cuenta)
  ↓
Dashboard (formulario de datos)
  ↓
Resultados nutricionales
  ↓
Menú sugerido
👥 Roles del sistema

Para el MVP, solo necesitas:

👤 Usuario

Puede:

registrarse

iniciar sesión

ingresar datos físicos

ver calorías

ver macros

ver menú

🔒 (Opcional si quieres subir nota) Admin

Podría:

agregar comidas

editar comidas

👉 Esto es bonus, no obligatorio.

🗄️ Base de datos (SQLite)
Tabla usuarios
usuarios
--------
id
nombre
edad
peso
altura
sexo
objetivo
email
password
Tabla comidas
comidas
-------
id
nombre
tipo
calorias
proteinas
carbs
grasas
🧩 Tecnologías (las correctas para tu curso)

✅ Python
✅ Tkinter
✅ SQLite
✅ PyInstaller (para .exe)

📦 Cómo generar el ejecutable

Cuando todo funcione:

pip install pyinstaller
pyinstaller --onefile --windowed main.py

Te genera:

dist/main.exe

Y listo para cualquier PC 💪

🚀 Qué te puede hacer destacar (sin complicarte)

Si quieres que tu profe diga "epa este chico sabe":

✨ validaciones de inputs
✨ barra de progreso
✨ mensajes bonitos
✨ icono personalizado
✨ diseño limpio en Tkinter

🧠 Alcance realista del MVP

✅ Login funcional
✅ Cálculo correcto
✅ Menú básico
✅ Guardado en DB
✅ Ejecutable

❌ IA real
❌ machine learning
❌ nutrición clínica avanzada
❌ API externas

🔥 Si quieres, te ayudo a nivel GOD

Puedo en el siguiente mensaje darte:

🧩 diagrama de clases

🪟 wireframe de las ventanas

🗄️ script SQL listo

🧮 código base de la calculadora

🎨 plantilla Tkinter bonita

Solo dime:

"vamos con el starter kit"

y lo armamos brutal 😏