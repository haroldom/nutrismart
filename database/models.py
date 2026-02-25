from database.db import get_connection
from datetime import datetime, date, timedelta
import hashlib


def hash_password(password):
    """Genera hash SHA-256 de la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()


# ============ USUARIOS ============

def crear_usuario(nombre, edad, peso, altura, sexo, objetivo, nivel_actividad, email, password):
    """Crea un nuevo usuario en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre, edad, peso, altura, sexo, objetivo, nivel_actividad, email, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, edad, peso, altura, sexo, objetivo, nivel_actividad, email, hash_password(password)))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def verificar_login(email, password):
    """Verifica credenciales y retorna el usuario si es válido."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usuarios WHERE email = ? AND password = ?
    ''', (email, hash_password(password)))
    usuario = cursor.fetchone()
    conn.close()
    return dict(usuario) if usuario else None


def verificar_credenciales(email, password):
    """Alias de verificar_login para compatibilidad con PyQt6."""
    return verificar_login(email, password)


def obtener_usuario_por_id(user_id):
    """Obtiene un usuario por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
    usuario = cursor.fetchone()
    conn.close()
    return dict(usuario) if usuario else None


def actualizar_usuario(user_id, nombre=None, edad=None, peso=None, altura=None, sexo=None, objetivo=None, nivel_actividad=None):
    """Actualiza los datos de un usuario. Parámetros opcionales."""
    conn = get_connection()
    cursor = conn.cursor()

    # Construir query dinámicamente con solo los campos proporcionados
    updates = []
    valores = []

    if nombre is not None:
        updates.append("nombre = ?")
        valores.append(nombre)
    if edad is not None:
        updates.append("edad = ?")
        valores.append(edad)
    if peso is not None:
        updates.append("peso = ?")
        valores.append(peso)
    if altura is not None:
        updates.append("altura = ?")
        valores.append(altura)
    if sexo is not None:
        updates.append("sexo = ?")
        valores.append(sexo)
    if objetivo is not None:
        updates.append("objetivo = ?")
        valores.append(objetivo)
    if nivel_actividad is not None:
        updates.append("nivel_actividad = ?")
        valores.append(nivel_actividad)

    if updates:
        valores.append(user_id)
        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, valores)
        conn.commit()

    conn.close()


def actualizar_racha(user_id, racha_actual, racha_maxima):
    """Actualiza las rachas del usuario."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE usuarios SET racha_actual = ?, racha_maxima = ? WHERE id = ?
    ''', (racha_actual, racha_maxima, user_id))
    conn.commit()
    conn.close()


def email_existe(email):
    """Verifica si un email ya está registrado."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe


# ============ COMIDAS/RECETAS ============

def obtener_comidas_por_tipo(tipo):
    """Obtiene todas las comidas del sistema de un tipo específico."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comidas WHERE tipo = ? AND (es_personalizada = 0 OR es_personalizada IS NULL)', (tipo,))
    comidas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comidas


def obtener_todas_comidas():
    """Obtiene todas las comidas del sistema (no personalizadas)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comidas WHERE es_personalizada = 0 OR es_personalizada IS NULL ORDER BY tipo, nombre')
    comidas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comidas


def obtener_comidas():
    """Alias de obtener_todas_comidas para compatibilidad."""
    return obtener_todas_comidas()


def obtener_comida_por_id(comida_id):
    """Obtiene una comida por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comidas WHERE id = ?', (comida_id,))
    comida = cursor.fetchone()
    conn.close()
    return dict(comida) if comida else None


def buscar_comidas(termino):
    """Busca comidas por nombre."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comidas WHERE nombre LIKE ?', (f'%{termino}%',))
    comidas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comidas


def crear_comida(nombre, tipo, calorias, proteinas, carbs, grasas,
                 ingredientes='', preparacion='', tiempo=30, dificultad='media', creado_por=None):
    """Crea una nueva comida/receta."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comidas (nombre, tipo, calorias, proteinas, carbs, grasas,
                            ingredientes, preparacion, tiempo_preparacion, dificultad,
                            creado_por, es_personalizada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    ''', (nombre, tipo, calorias, proteinas, carbs, grasas,
          ingredientes, preparacion, tiempo, dificultad, creado_por))
    conn.commit()
    comida_id = cursor.lastrowid
    conn.close()
    return comida_id


def obtener_recetas_usuario(user_id):
    """Obtiene las recetas creadas por un usuario."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comidas WHERE creado_por = ? AND es_personalizada = 1', (user_id,))
    comidas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comidas


def eliminar_comida(comida_id, user_id):
    """Elimina una comida (solo si es del usuario)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comidas WHERE id = ? AND creado_por = ?', (comida_id, user_id))
    conn.commit()
    conn.close()


# ============ REGISTRO DIARIO ============

def registrar_comida_diaria(usuario_id, comida_id=None, nombre_comida='', tipo_comida='',
                            calorias=0, proteinas=0, carbs=0, grasas=0):
    """Registra una comida en el diario del usuario."""
    conn = get_connection()
    cursor = conn.cursor()
    fecha = date.today().isoformat()
    hora = datetime.now().strftime('%H:%M')

    cursor.execute('''
        INSERT INTO registro_diario (usuario_id, fecha, comida_id, nombre_comida,
                                    tipo_comida, calorias, proteinas, carbs, grasas, hora)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (usuario_id, fecha, comida_id, nombre_comida, tipo_comida,
          calorias, proteinas, carbs, grasas, hora))
    conn.commit()
    registro_id = cursor.lastrowid
    conn.close()

    # Actualizar metas diarias y verificar racha
    actualizar_consumo_diario(usuario_id, fecha, calorias, proteinas, carbs, grasas)
    verificar_meta_cumplida(usuario_id, fecha)
    actualizar_rachas_usuario(usuario_id)

    return registro_id


def obtener_registro_diario(usuario_id, fecha=None):
    """Obtiene el registro de comidas de un día."""
    if fecha is None:
        fecha = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM registro_diario
        WHERE usuario_id = ? AND fecha = ?
        ORDER BY hora
    ''', (usuario_id, fecha))
    registros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return registros


def eliminar_registro(registro_id, usuario_id):
    """Elimina un registro del diario."""
    conn = get_connection()
    cursor = conn.cursor()

    # Obtener datos del registro para restar del consumo
    cursor.execute('SELECT * FROM registro_diario WHERE id = ? AND usuario_id = ?',
                   (registro_id, usuario_id))
    registro = cursor.fetchone()

    if registro:
        registro = dict(registro)
        cursor.execute('DELETE FROM registro_diario WHERE id = ?', (registro_id,))
        conn.commit()

        # Restar del consumo diario
        actualizar_consumo_diario(
            usuario_id, registro['fecha'],
            -registro['calorias'], -registro['proteinas'],
            -registro['carbs'], -registro['grasas']
        )

        # Re-evaluar si la meta sigue cumplida y actualizar racha
        verificar_meta_cumplida(usuario_id, registro['fecha'])
        actualizar_rachas_usuario(usuario_id)

    conn.close()


def obtener_totales_dia(usuario_id, fecha=None):
    """Obtiene los totales nutricionales de un día."""
    if fecha is None:
        fecha = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            COALESCE(SUM(calorias), 0) as total_calorias,
            COALESCE(SUM(proteinas), 0) as total_proteinas,
            COALESCE(SUM(carbs), 0) as total_carbs,
            COALESCE(SUM(grasas), 0) as total_grasas,
            COUNT(*) as num_comidas
        FROM registro_diario
        WHERE usuario_id = ? AND fecha = ?
    ''', (usuario_id, fecha))
    resultado = cursor.fetchone()
    conn.close()
    return dict(resultado) if resultado else None


# ============ METAS DIARIAS ============

def crear_meta_diaria(usuario_id, calorias_meta, proteinas_meta, carbs_meta, grasas_meta, fecha=None):
    """Crea o actualiza la meta diaria del usuario."""
    if fecha is None:
        fecha = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO metas_diarias
        (usuario_id, fecha, calorias_meta, proteinas_meta, carbs_meta, grasas_meta,
         calorias_consumidas, proteinas_consumidas, carbs_consumidas, grasas_consumidas)
        VALUES (?, ?, ?, ?, ?, ?,
                COALESCE((SELECT calorias_consumidas FROM metas_diarias WHERE usuario_id = ? AND fecha = ?), 0),
                COALESCE((SELECT proteinas_consumidas FROM metas_diarias WHERE usuario_id = ? AND fecha = ?), 0),
                COALESCE((SELECT carbs_consumidas FROM metas_diarias WHERE usuario_id = ? AND fecha = ?), 0),
                COALESCE((SELECT grasas_consumidas FROM metas_diarias WHERE usuario_id = ? AND fecha = ?), 0))
    ''', (usuario_id, fecha, calorias_meta, proteinas_meta, carbs_meta, grasas_meta,
          usuario_id, fecha, usuario_id, fecha, usuario_id, fecha, usuario_id, fecha))
    conn.commit()
    conn.close()


def actualizar_consumo_diario(usuario_id, fecha, calorias, proteinas, carbs, grasas):
    """Actualiza el consumo en la meta diaria."""
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si existe la meta
    cursor.execute('SELECT * FROM metas_diarias WHERE usuario_id = ? AND fecha = ?',
                   (usuario_id, fecha))
    meta = cursor.fetchone()

    if meta:
        cursor.execute('''
            UPDATE metas_diarias SET
                calorias_consumidas = calorias_consumidas + ?,
                proteinas_consumidas = proteinas_consumidas + ?,
                carbs_consumidas = carbs_consumidas + ?,
                grasas_consumidas = grasas_consumidas + ?
            WHERE usuario_id = ? AND fecha = ?
        ''', (calorias, proteinas, carbs, grasas, usuario_id, fecha))
    conn.commit()
    conn.close()


def obtener_meta_diaria(usuario_id, fecha=None):
    """Obtiene la meta diaria del usuario."""
    if fecha is None:
        fecha = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM metas_diarias WHERE usuario_id = ? AND fecha = ?',
                   (usuario_id, fecha))
    meta = cursor.fetchone()
    conn.close()
    return dict(meta) if meta else None


def verificar_meta_cumplida(usuario_id, fecha=None):
    """Verifica si el usuario cumplió su meta del día."""
    if fecha is None:
        fecha = date.today().isoformat()

    meta = obtener_meta_diaria(usuario_id, fecha)
    if not meta:
        return False

    # Meta cumplida si está entre 90% y 110% de las calorías objetivo
    porcentaje = meta['calorias_consumidas'] / meta['calorias_meta'] if meta['calorias_meta'] > 0 else 0
    cumplida = 0.9 <= porcentaje <= 1.1

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE metas_diarias SET meta_cumplida = ? WHERE usuario_id = ? AND fecha = ?',
                   (1 if cumplida else 0, usuario_id, fecha))
    conn.commit()
    conn.close()

    return cumplida


# ============ RACHAS ============

def calcular_racha(usuario_id):
    """Calcula la racha actual del usuario."""
    conn = get_connection()
    cursor = conn.cursor()

    # Obtener días con meta cumplida ordenados
    cursor.execute('''
        SELECT fecha FROM metas_diarias
        WHERE usuario_id = ? AND meta_cumplida = 1
        ORDER BY fecha DESC
    ''', (usuario_id,))

    fechas = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not fechas:
        return 0

    racha = 0
    fecha_actual = date.today()

    for fecha_str in fechas:
        fecha = date.fromisoformat(fecha_str)
        dias_diferencia = (fecha_actual - fecha).days

        if dias_diferencia == racha:
            racha += 1
        else:
            break

    return racha


def actualizar_rachas_usuario(usuario_id):
    """Actualiza las rachas del usuario."""
    racha_actual = calcular_racha(usuario_id)
    usuario = obtener_usuario_por_id(usuario_id)

    racha_maxima = max(racha_actual, usuario.get('racha_maxima', 0))
    actualizar_racha(usuario_id, racha_actual, racha_maxima)

    return racha_actual, racha_maxima


# ============ LOGROS ============

def obtener_todos_logros():
    """Obtiene todos los logros disponibles."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logros ORDER BY puntos')
    logros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return logros


def obtener_logros_usuario(usuario_id):
    """Obtiene los logros desbloqueados por un usuario."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT l.*, ul.fecha_obtenido
        FROM logros l
        INNER JOIN usuario_logros ul ON l.id = ul.logro_id
        WHERE ul.usuario_id = ?
        ORDER BY ul.fecha_obtenido DESC
    ''', (usuario_id,))
    logros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return logros


def desbloquear_logro(usuario_id, logro_id):
    """Desbloquea un logro para el usuario."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO usuario_logros (usuario_id, logro_id)
            VALUES (?, ?)
        ''', (usuario_id, logro_id))
        conn.commit()
        return cursor.rowcount > 0
    except:
        return False
    finally:
        conn.close()


def verificar_logros(usuario_id):
    """Verifica y desbloquea logros según las condiciones."""
    conn = get_connection()
    cursor = conn.cursor()
    logros_nuevos = []

    # Contar registros de comidas
    cursor.execute('SELECT COUNT(*) FROM registro_diario WHERE usuario_id = ?', (usuario_id,))
    num_registros = cursor.fetchone()[0]

    # Contar recetas creadas
    cursor.execute('SELECT COUNT(*) FROM comidas WHERE creado_por = ? AND es_personalizada = 1', (usuario_id,))
    num_recetas = cursor.fetchone()[0]

    # Obtener racha
    usuario = obtener_usuario_por_id(usuario_id)
    racha = usuario.get('racha_actual', 0)

    # Comidas en el día actual
    fecha_hoy = date.today().isoformat()
    cursor.execute('SELECT COUNT(*) FROM registro_diario WHERE usuario_id = ? AND fecha = ?',
                   (usuario_id, fecha_hoy))
    comidas_hoy = cursor.fetchone()[0]

    conn.close()

    # Verificar cada condición
    condiciones = {
        'registro_1': num_registros >= 1,
        'racha_7': racha >= 7,
        'racha_14': racha >= 14,
        'racha_30': racha >= 30,
        'receta_1': num_recetas >= 1,
        'receta_5': num_recetas >= 5,
        'dia_completo': comidas_hoy >= 3,
    }

    for condicion, cumplida in condiciones.items():
        if cumplida:
            # Buscar logro con esta condición
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre FROM logros WHERE condicion = ?', (condicion,))
            logro = cursor.fetchone()
            conn.close()

            if logro:
                if desbloquear_logro(usuario_id, logro[0]):
                    logros_nuevos.append(logro[1])

    return logros_nuevos


# ============ ESTADÍSTICAS ============

def obtener_estadisticas_semana(usuario_id):
    """Obtiene resumen de estadísticas de la última semana."""
    conn = get_connection()
    cursor = conn.cursor()

    fecha_inicio = (date.today() - timedelta(days=7)).isoformat()

    # Obtener resumen agregado
    cursor.execute('''
        SELECT
            COUNT(DISTINCT fecha) as dias_activos,
            COUNT(*) as comidas_totales,
            COALESCE(AVG(calorias), 0) as promedio_calorias
        FROM registro_diario
        WHERE usuario_id = ? AND fecha >= ?
    ''', (usuario_id, fecha_inicio))

    resultado = cursor.fetchone()
    conn.close()

    return dict(resultado) if resultado else {
        'dias_activos': 0,
        'comidas_totales': 0,
        'promedio_calorias': 0
    }


def obtener_comidas_mas_consumidas(usuario_id, limite=5):
    """Obtiene las comidas más consumidas por el usuario."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nombre_comida, COUNT(*) as veces, AVG(calorias) as calorias_promedio
        FROM registro_diario
        WHERE usuario_id = ? AND nombre_comida != ''
        GROUP BY nombre_comida
        ORDER BY veces DESC
        LIMIT ?
    ''', (usuario_id, limite))
    comidas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comidas


def obtener_registro_hoy(usuario_id):
    """Obtiene el registro completo del día de hoy con totales y lista de comidas."""
    fecha = date.today().isoformat()

    # Obtener totales
    totales = obtener_totales_dia(usuario_id, fecha)

    # Obtener lista de comidas
    comidas = obtener_registro_diario(usuario_id, fecha)

    if totales and totales['num_comidas'] > 0:
        return {
            'total_calorias': totales['total_calorias'],
            'total_proteinas': totales['total_proteinas'],
            'total_carbs': totales['total_carbs'],
            'total_grasas': totales['total_grasas'],
            'num_comidas': totales['num_comidas'],
            'comidas': comidas
        }

    return None
