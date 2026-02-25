import sqlite3
import os
import sys
from datetime import datetime, date


def _get_db_path():
    """Devuelve la ruta de la base de datos.
    Cuando la app está empaquetada usa la misma carpeta del ejecutable.
    En desarrollo usa el directorio del módulo.
    """
    if getattr(sys, 'frozen', False):
        data_dir = os.path.dirname(sys.executable)
    else:
        data_dir = os.path.dirname(__file__)
    return os.path.join(data_dir, 'nutrismart.db')


DB_PATH = _get_db_path()


def get_connection():
    """Obtiene conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa las tablas de la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla usuarios (con nivel de actividad)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            peso REAL NOT NULL,
            altura REAL NOT NULL,
            sexo TEXT NOT NULL,
            objetivo TEXT NOT NULL,
            nivel_actividad TEXT DEFAULT 'sedentario',
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fecha_registro TEXT DEFAULT CURRENT_DATE,
            racha_actual INTEGER DEFAULT 0,
            racha_maxima INTEGER DEFAULT 0
        )
    ''')

    # Tabla comidas/recetas (con ingredientes y preparación)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            calorias INTEGER NOT NULL,
            proteinas REAL NOT NULL,
            carbs REAL NOT NULL,
            grasas REAL NOT NULL,
            ingredientes TEXT,
            preparacion TEXT,
            tiempo_preparacion INTEGER DEFAULT 30,
            dificultad TEXT DEFAULT 'media',
            imagen TEXT,
            creado_por INTEGER,
            es_personalizada INTEGER DEFAULT 0,
            FOREIGN KEY (creado_por) REFERENCES usuarios(id)
        )
    ''')

    # Tabla registro diario de comidas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            comida_id INTEGER,
            nombre_comida TEXT,
            tipo_comida TEXT NOT NULL,
            calorias INTEGER NOT NULL,
            proteinas REAL NOT NULL,
            carbs REAL NOT NULL,
            grasas REAL NOT NULL,
            hora TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (comida_id) REFERENCES comidas(id)
        )
    ''')

    # Tabla de metas diarias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas_diarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            calorias_meta INTEGER NOT NULL,
            calorias_consumidas INTEGER DEFAULT 0,
            proteinas_meta REAL,
            proteinas_consumidas REAL DEFAULT 0,
            carbs_meta REAL,
            carbs_consumidas REAL DEFAULT 0,
            grasas_meta REAL,
            grasas_consumidas REAL DEFAULT 0,
            meta_cumplida INTEGER DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            UNIQUE(usuario_id, fecha)
        )
    ''')

    # Tabla de logros/achievements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            icono TEXT,
            condicion TEXT,
            puntos INTEGER DEFAULT 10
        )
    ''')

    # Tabla de logros desbloqueados por usuario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario_logros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            logro_id INTEGER NOT NULL,
            fecha_obtenido TEXT DEFAULT CURRENT_DATE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (logro_id) REFERENCES logros(id),
            UNIQUE(usuario_id, logro_id)
        )
    ''')

    # Migraciones: agregar columnas faltantes si la tabla ya existía sin ellas
    cursor.execute("PRAGMA table_info(usuarios)")
    columnas_usuarios = {row[1] for row in cursor.fetchall()}
    if 'nivel_actividad' not in columnas_usuarios:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN nivel_actividad TEXT DEFAULT 'sedentario'")
    if 'racha_actual' not in columnas_usuarios:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN racha_actual INTEGER DEFAULT 0")
    if 'racha_maxima' not in columnas_usuarios:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN racha_maxima INTEGER DEFAULT 0")

    cursor.execute("PRAGMA table_info(comidas)")
    columnas_comidas = {row[1] for row in cursor.fetchall()}
    if 'ingredientes' not in columnas_comidas:
        cursor.execute('ALTER TABLE comidas ADD COLUMN ingredientes TEXT')
    if 'preparacion' not in columnas_comidas:
        cursor.execute('ALTER TABLE comidas ADD COLUMN preparacion TEXT')
    if 'tiempo_preparacion' not in columnas_comidas:
        cursor.execute('ALTER TABLE comidas ADD COLUMN tiempo_preparacion INTEGER DEFAULT 30')
    if 'dificultad' not in columnas_comidas:
        cursor.execute("ALTER TABLE comidas ADD COLUMN dificultad TEXT DEFAULT 'media'")
    if 'creado_por' not in columnas_comidas:
        cursor.execute('ALTER TABLE comidas ADD COLUMN creado_por INTEGER')
    if 'es_personalizada' not in columnas_comidas:
        cursor.execute('ALTER TABLE comidas ADD COLUMN es_personalizada INTEGER DEFAULT 0')

    conn.commit()
    conn.close()


def poblar_comidas():
    """Pobla la tabla de comidas con platos peruanos si está vacía."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM comidas')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    comidas_peruanas = [
        # Desayunos
        {
            'nombre': 'Avena con leche',
            'tipo': 'desayuno',
            'calorias': 250,
            'proteinas': 8,
            'carbs': 40,
            'grasas': 6,
            'ingredientes': '1 taza de avena|2 tazas de leche|1 cda de miel|1/2 cdta de canela|Frutas al gusto',
            'preparacion': 'Hervir la leche en una olla|Agregar la avena y revolver constantemente|Cocinar por 5-7 minutos a fuego medio|Agregar canela y miel|Servir caliente con frutas picadas',
            'tiempo': 15,
            'dificultad': 'facil'
        },
        {
            'nombre': 'Pan con palta',
            'tipo': 'desayuno',
            'calorias': 280,
            'proteinas': 6,
            'carbs': 30,
            'grasas': 15,
            'ingredientes': '2 rebanadas de pan integral|1 palta madura|Sal y pimienta al gusto|Jugo de 1/2 limón|Tomate cherry (opcional)',
            'preparacion': 'Tostar el pan hasta que esté dorado|Cortar la palta y retirar la semilla|Machacar la palta con un tenedor|Agregar limón, sal y pimienta|Untar sobre el pan tostado|Decorar con tomate si desea',
            'tiempo': 10,
            'dificultad': 'facil'
        },
        {
            'nombre': 'Quinua con manzana',
            'tipo': 'desayuno',
            'calorias': 220,
            'proteinas': 7,
            'carbs': 38,
            'grasas': 4,
            'ingredientes': '1/2 taza de quinua|1 taza de agua|1 manzana|1 cda de miel|Canela al gusto|Pasas (opcional)',
            'preparacion': 'Lavar bien la quinua|Cocinar con agua por 15 minutos|Picar la manzana en cubos|Mezclar la quinua con la manzana|Agregar miel y canela|Servir tibio o frío',
            'tiempo': 20,
            'dificultad': 'facil'
        },
        {
            'nombre': 'Huevos revueltos con pan',
            'tipo': 'desayuno',
            'calorias': 320,
            'proteinas': 15,
            'carbs': 25,
            'grasas': 18,
            'ingredientes': '2 huevos|1 cda de mantequilla|2 rebanadas de pan|Sal y pimienta|Cebollita china picada',
            'preparacion': 'Batir los huevos con sal y pimienta|Derretir mantequilla en sartén|Verter los huevos y revolver suavemente|Cocinar hasta que cuajen|Tostar el pan|Servir con cebollita china',
            'tiempo': 10,
            'dificultad': 'facil'
        },

        # Almuerzos
        {
            'nombre': 'Arroz con pollo',
            'tipo': 'almuerzo',
            'calorias': 600,
            'proteinas': 35,
            'carbs': 65,
            'grasas': 20,
            'ingredientes': '1 presa de pollo|1 taza de arroz|1/2 taza de alverjitas|1/2 taza de zanahoria|1/4 taza de culantro licuado|1/2 cerveza negra|Ajo, cebolla, ají amarillo',
            'preparacion': 'Dorar el pollo sazonado en aceite|Preparar aderezo con ajo, cebolla y ají|Agregar el culantro licuado y cerveza|Añadir el arroz y el agua necesaria|Incorporar alverjitas y zanahoria|Cocinar tapado por 20 minutos|Servir con salsa criolla',
            'tiempo': 45,
            'dificultad': 'media'
        },
        {
            'nombre': 'Lomo saltado',
            'tipo': 'almuerzo',
            'calorias': 550,
            'proteinas': 40,
            'carbs': 45,
            'grasas': 22,
            'ingredientes': '200g de lomo fino|2 tomates|1 cebolla roja|Ají amarillo|Sillao|Vinagre|Papas fritas|Arroz blanco',
            'preparacion': 'Cortar el lomo en tiras y sazonar|Cortar tomate y cebolla en juliana|Saltear la carne a fuego alto|Agregar cebolla y tomate|Añadir sillao y vinagre|Mezclar con papas fritas|Servir con arroz blanco',
            'tiempo': 30,
            'dificultad': 'media'
        },
        {
            'nombre': 'Ceviche de pescado',
            'tipo': 'almuerzo',
            'calorias': 350,
            'proteinas': 38,
            'carbs': 20,
            'grasas': 12,
            'ingredientes': '500g de pescado fresco|10 limones|1 cebolla roja|Ají limo|Culantro|Sal|Camote|Choclo|Lechuga',
            'preparacion': 'Cortar el pescado en cubos|Exprimir los limones|Cortar cebolla en juliana y lavar|Mezclar pescado con limón y sal|Agregar ají limo y culantro|Dejar reposar 5 minutos|Añadir la cebolla|Servir con camote y choclo',
            'tiempo': 20,
            'dificultad': 'media'
        },
        {
            'nombre': 'Ají de gallina',
            'tipo': 'almuerzo',
            'calorias': 580,
            'proteinas': 32,
            'carbs': 50,
            'grasas': 28,
            'ingredientes': '1/2 kg de pechuga de pollo|4 ajíes amarillos|1/2 taza de nueces|3 rebanadas de pan|1 taza de leche|Arroz blanco|Papas|Aceitunas|Huevo duro',
            'preparacion': 'Sancochar y deshilachar el pollo|Licuar ají con leche y pan remojado|Hacer aderezo con ajo y cebolla|Agregar la crema de ají|Incorporar el pollo deshilachado|Cocinar 10 minutos|Servir sobre papas con arroz|Decorar con aceituna y huevo',
            'tiempo': 50,
            'dificultad': 'media'
        },
        {
            'nombre': 'Seco de res con frejoles',
            'tipo': 'almuerzo',
            'calorias': 650,
            'proteinas': 42,
            'carbs': 55,
            'grasas': 25,
            'ingredientes': '1/2 kg de carne de res|1 taza de culantro|1/2 taza de chicha de jora|Ajo, cebolla, ají|Frejoles canario cocidos|Arroz blanco|Yuca sancochada',
            'preparacion': 'Sellar la carne en trozos|Preparar aderezo con ajo, cebolla y ají|Licuar culantro con chicha de jora|Agregar a la carne y cocinar tapado|Cocinar hasta que la carne esté suave|Preparar frejoles aparte|Servir con arroz y yuca',
            'tiempo': 90,
            'dificultad': 'dificil'
        },
        {
            'nombre': 'Pollo a la brasa con papas',
            'tipo': 'almuerzo',
            'calorias': 700,
            'proteinas': 45,
            'carbs': 50,
            'grasas': 35,
            'ingredientes': '1/4 de pollo|Papas fritas|Ensalada fresca|Ají de huacatay|Sillao|Comino|Ajo|Vinagre|Cerveza negra',
            'preparacion': 'Marinar pollo con sillao, ajo, comino y cerveza|Dejar reposar mínimo 4 horas|Hornear a 180°C por 45 minutos|Voltear a mitad de cocción|Freír las papas|Preparar ensalada|Servir con ají de huacatay',
            'tiempo': 60,
            'dificultad': 'media'
        },

        # Cenas
        {
            'nombre': 'Ensalada de pollo',
            'tipo': 'cena',
            'calorias': 350,
            'proteinas': 30,
            'carbs': 15,
            'grasas': 18,
            'ingredientes': '150g pechuga de pollo|Lechuga|Tomate|Pepino|Palta|Aceite de oliva|Limón|Sal y pimienta',
            'preparacion': 'Cocinar y desmenuzar el pollo|Lavar y cortar las verduras|Cortar la palta en cubos|Mezclar todo en un bowl|Preparar vinagreta con aceite y limón|Aliñar la ensalada|Servir fresca',
            'tiempo': 20,
            'dificultad': 'facil'
        },
        {
            'nombre': 'Sopa de pollo',
            'tipo': 'cena',
            'calorias': 280,
            'proteinas': 22,
            'carbs': 25,
            'grasas': 10,
            'ingredientes': '1 presa de pollo|2 papas|1 zanahoria|Fideos cabello de ángel|Apio|Culantro|Sal',
            'preparacion': 'Hervir el pollo con sal|Agregar verduras picadas|Cocinar 20 minutos|Añadir fideos|Cocinar 5 minutos más|Agregar culantro picado|Servir caliente',
            'tiempo': 35,
            'dificultad': 'facil'
        },
        {
            'nombre': 'Pescado a la plancha con ensalada',
            'tipo': 'cena',
            'calorias': 320,
            'proteinas': 35,
            'carbs': 12,
            'grasas': 14,
            'ingredientes': '200g filete de pescado|Aceite de oliva|Ajo|Limón|Ensalada verde|Tomate|Sal y pimienta',
            'preparacion': 'Sazonar el pescado con sal, pimienta y ajo|Calentar plancha con aceite|Cocinar 4 minutos por lado|Preparar ensalada fresca|Rociar con limón|Servir inmediatamente',
            'tiempo': 15,
            'dificultad': 'facil'
        },
        {
            'nombre': 'Tortilla de verduras',
            'tipo': 'cena',
            'calorias': 250,
            'proteinas': 14,
            'carbs': 18,
            'grasas': 14,
            'ingredientes': '3 huevos|1 papa pequeña|1/4 cebolla|1/4 pimiento|Espinaca|Sal y pimienta|Aceite',
            'preparacion': 'Cortar verduras en cubitos pequeños|Saltear las verduras|Batir huevos con sal y pimienta|Verter sobre las verduras|Cocinar a fuego bajo tapado|Voltear para dorar|Servir caliente',
            'tiempo': 25,
            'dificultad': 'facil'
        },
        {
            'nombre': 'Sopa criolla',
            'tipo': 'cena',
            'calorias': 380,
            'proteinas': 20,
            'carbs': 35,
            'grasas': 16,
            'ingredientes': '150g carne molida|Fideos cabello de ángel|2 huevos|Leche evaporada|Ají panca|Ajo|Cebolla|Orégano',
            'preparacion': 'Preparar aderezo con ajo, cebolla y ají|Agregar carne molida y dorar|Añadir agua y hervir|Incorporar fideos|Agregar leche evaporada|Cascar huevos encima|Servir con orégano',
            'tiempo': 30,
            'dificultad': 'media'
        },
    ]

    for comida in comidas_peruanas:
        cursor.execute('''
            INSERT INTO comidas (nombre, tipo, calorias, proteinas, carbs, grasas,
                                ingredientes, preparacion, tiempo_preparacion, dificultad, es_personalizada)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        ''', (
            comida['nombre'], comida['tipo'], comida['calorias'],
            comida['proteinas'], comida['carbs'], comida['grasas'],
            comida['ingredientes'], comida['preparacion'],
            comida['tiempo'], comida['dificultad']
        ))

    conn.commit()
    conn.close()


def actualizar_comidas_default():
    """Actualiza ingredientes y preparación de las comidas por defecto que los tengan vacíos."""
    conn = get_connection()
    cursor = conn.cursor()

    actualizaciones = [
        ('Avena con leche',
         '1 taza de avena|2 tazas de leche|1 cda de miel|1/2 cdta de canela|Frutas al gusto',
         'Hervir la leche en una olla|Agregar la avena y revolver constantemente|Cocinar por 5-7 minutos a fuego medio|Agregar canela y miel|Servir caliente con frutas picadas',
         15, 'facil'),
        ('Pan con palta',
         '2 rebanadas de pan integral|1 palta madura|Sal y pimienta al gusto|Jugo de 1/2 limón|Tomate cherry (opcional)',
         'Tostar el pan hasta que esté dorado|Cortar la palta y retirar la semilla|Machacar la palta con un tenedor|Agregar limón, sal y pimienta|Untar sobre el pan tostado|Decorar con tomate si desea',
         10, 'facil'),
        ('Quinua con manzana',
         '1/2 taza de quinua|1 taza de agua|1 manzana|1 cda de miel|Canela al gusto|Pasas (opcional)',
         'Lavar bien la quinua|Cocinar con agua por 15 minutos|Picar la manzana en cubos|Mezclar la quinua con la manzana|Agregar miel y canela|Servir tibio o frío',
         20, 'facil'),
        ('Huevos revueltos con pan',
         '2 huevos|1 cda de mantequilla|2 rebanadas de pan|Sal y pimienta|Cebollita china picada',
         'Batir los huevos con sal y pimienta|Derretir mantequilla en sartén|Verter los huevos y revolver suavemente|Cocinar hasta que cuajen|Tostar el pan|Servir con cebollita china',
         10, 'facil'),
        ('Arroz con pollo',
         '1 presa de pollo|1 taza de arroz|1/2 taza de alverjitas|1/2 taza de zanahoria|1/4 taza de culantro licuado|1/2 cerveza negra|Ajo, cebolla, ají amarillo',
         'Dorar el pollo sazonado en aceite|Preparar aderezo con ajo, cebolla y ají|Agregar el culantro licuado y cerveza|Añadir el arroz y el agua necesaria|Incorporar alverjitas y zanahoria|Cocinar tapado por 20 minutos|Servir con salsa criolla',
         45, 'media'),
        ('Lomo saltado',
         '200g de lomo fino|2 tomates|1 cebolla roja|Ají amarillo|Sillao|Vinagre|Papas fritas|Arroz blanco',
         'Cortar el lomo en tiras y sazonar|Cortar tomate y cebolla en juliana|Saltear la carne a fuego alto|Agregar cebolla y tomate|Añadir sillao y vinagre|Mezclar con papas fritas|Servir con arroz blanco',
         30, 'media'),
        ('Ceviche de pescado',
         '500g de pescado fresco|10 limones|1 cebolla roja|Ají limo|Culantro|Sal|Camote|Choclo|Lechuga',
         'Cortar el pescado en cubos|Exprimir los limones|Cortar cebolla en juliana y lavar|Mezclar pescado con limón y sal|Agregar ají limo y culantro|Dejar reposar 5 minutos|Añadir la cebolla|Servir con camote y choclo',
         20, 'media'),
        ('Ají de gallina',
         '1/2 kg de pechuga de pollo|4 ajíes amarillos|1/2 taza de nueces|3 rebanadas de pan|1 taza de leche|Arroz blanco|Papas|Aceitunas|Huevo duro',
         'Sancochar y deshilachar el pollo|Licuar ají con leche y pan remojado|Hacer aderezo con ajo y cebolla|Agregar la crema de ají|Incorporar el pollo deshilachado|Cocinar 10 minutos|Servir sobre papas con arroz|Decorar con aceituna y huevo',
         50, 'media'),
        ('Seco de res con frejoles',
         '1/2 kg de carne de res|1 taza de culantro|1/2 taza de chicha de jora|Ajo, cebolla, ají|Frejoles canario cocidos|Arroz blanco|Yuca sancochada',
         'Sellar la carne en trozos|Preparar aderezo con ajo, cebolla y ají|Licuar culantro con chicha de jora|Agregar a la carne y cocinar tapado|Cocinar hasta que la carne esté suave|Preparar frejoles aparte|Servir con arroz y yuca',
         90, 'dificil'),
        ('Pollo a la brasa con papas',
         '1/4 de pollo|Papas fritas|Ensalada fresca|Ají de huacatay|Sillao|Comino|Ajo|Vinagre|Cerveza negra',
         'Marinar pollo con sillao, ajo, comino y cerveza|Dejar reposar mínimo 4 horas|Hornear a 180°C por 45 minutos|Voltear a mitad de cocción|Freír las papas|Preparar ensalada|Servir con ají de huacatay',
         60, 'media'),
        ('Ensalada de pollo',
         '150g pechuga de pollo|Lechuga|Tomate|Pepino|Palta|Aceite de oliva|Limón|Sal y pimienta',
         'Cocinar y desmenuzar el pollo|Lavar y cortar las verduras|Cortar la palta en cubos|Mezclar todo en un bowl|Preparar vinagreta con aceite y limón|Aliñar la ensalada|Servir fresca',
         20, 'facil'),
        ('Sopa de pollo',
         '1 presa de pollo|2 papas|1 zanahoria|Fideos cabello de ángel|Apio|Culantro|Sal',
         'Hervir el pollo con sal|Agregar verduras picadas|Cocinar 20 minutos|Añadir fideos|Cocinar 5 minutos más|Agregar culantro picado|Servir caliente',
         35, 'facil'),
        ('Pescado a la plancha con ensalada',
         '200g filete de pescado|Aceite de oliva|Ajo|Limón|Ensalada verde|Tomate|Sal y pimienta',
         'Sazonar el pescado con sal, pimienta y ajo|Calentar plancha con aceite|Cocinar 4 minutos por lado|Preparar ensalada fresca|Rociar con limón|Servir inmediatamente',
         15, 'facil'),
        ('Tortilla de verduras',
         '3 huevos|1 papa pequeña|1/4 cebolla|1/4 pimiento|Espinaca|Sal y pimienta|Aceite',
         'Cortar verduras en cubitos pequeños|Saltear las verduras|Batir huevos con sal y pimienta|Verter sobre las verduras|Cocinar a fuego bajo tapado|Voltear para dorar|Servir caliente',
         25, 'facil'),
        ('Sopa criolla',
         '150g carne molida|Fideos cabello de ángel|2 huevos|Leche evaporada|Ají panca|Ajo|Cebolla|Orégano',
         'Preparar aderezo con ajo, cebolla y ají|Agregar carne molida y dorar|Añadir agua y hervir|Incorporar fideos|Agregar leche evaporada|Cascar huevos encima|Servir con orégano',
         30, 'media'),
    ]

    for nombre, ingredientes, preparacion, tiempo, dificultad in actualizaciones:
        cursor.execute('''
            UPDATE comidas
            SET ingredientes = ?, preparacion = ?, tiempo_preparacion = ?, dificultad = ?
            WHERE nombre = ? AND (ingredientes IS NULL OR ingredientes = '')
        ''', (ingredientes, preparacion, tiempo, dificultad, nombre))

    conn.commit()
    conn.close()


def poblar_logros():
    """Pobla la tabla de logros si está vacía."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM logros')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    logros = [
        ('Primera comida', 'Registraste tu primera comida', 'star', 'registro_1', 10),
        ('Semana saludable', '7 días cumpliendo tu meta', 'fire', 'racha_7', 50),
        ('Dos semanas', '14 días de racha', 'trophy', 'racha_14', 100),
        ('Mes completo', '30 días cumpliendo metas', 'medal', 'racha_30', 200),
        ('Chef novato', 'Creaste tu primera receta', 'chef', 'receta_1', 25),
        ('Chef experto', 'Creaste 5 recetas', 'chef_star', 'receta_5', 75),
        ('Explorador', 'Probaste 10 recetas diferentes', 'explore', 'probar_10', 50),
        ('Constancia', '3 comidas registradas en un día', 'check', 'dia_completo', 30),
    ]

    cursor.executemany('''
        INSERT INTO logros (nombre, descripcion, icono, condicion, puntos)
        VALUES (?, ?, ?, ?, ?)
    ''', logros)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    poblar_comidas()
    poblar_logros()
    print("Base de datos inicializada correctamente.")
