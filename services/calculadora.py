"""
Calculadora nutricional usando la fórmula Mifflin-St Jeor.
Con factores de actividad física para deportistas.
"""

# Factores de actividad física
FACTORES_ACTIVIDAD = {
    'sedentario': {
        'factor': 1.2,
        'nombre': 'Sedentario',
        'descripcion': 'Poco o ningún ejercicio, trabajo de escritorio'
    },
    'ligero': {
        'factor': 1.375,
        'nombre': 'Ligeramente activo',
        'descripcion': 'Ejercicio ligero 1-3 días/semana'
    },
    'moderado': {
        'factor': 1.55,
        'nombre': 'Moderadamente activo',
        'descripcion': 'Ejercicio moderado 3-5 días/semana'
    },
    'activo': {
        'factor': 1.725,
        'nombre': 'Muy activo',
        'descripcion': 'Ejercicio intenso 6-7 días/semana'
    },
    'muy_activo': {
        'factor': 1.9,
        'nombre': 'Extra activo',
        'descripcion': 'Atleta profesional, ejercicio muy intenso diario'
    }
}


def obtener_factores_actividad():
    """Retorna la lista de factores de actividad disponibles."""
    return FACTORES_ACTIVIDAD


def calcular_tmb(peso, altura, edad, sexo):
    """
    Calcula la Tasa Metabólica Basal (TMB) usando Mifflin-St Jeor.

    Args:
        peso: Peso en kg
        altura: Altura en cm
        edad: Edad en años
        sexo: 'masculino' o 'femenino'

    Returns:
        TMB en kcal/día
    """
    if sexo.lower() == 'masculino':
        tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * edad - 161
    return tmb


def calcular_calorias_mantenimiento(tmb, nivel_actividad='sedentario'):
    """
    Calcula las calorías de mantenimiento según nivel de actividad.

    Args:
        tmb: Tasa Metabólica Basal
        nivel_actividad: Clave del nivel de actividad

    Returns:
        Calorías de mantenimiento por día
    """
    factor = FACTORES_ACTIVIDAD.get(nivel_actividad, FACTORES_ACTIVIDAD['sedentario'])['factor']
    return round(tmb * factor)


def calcular_calorias_objetivo(calorias_mantenimiento, objetivo):
    """
    Calcula las calorías objetivo según el objetivo del usuario.

    Args:
        calorias_mantenimiento: Calorías de mantenimiento
        objetivo: 'bajar', 'mantener', o 'subir'

    Returns:
        Calorías objetivo por día
    """
    ajustes = {
        'bajar': -500,      # Déficit para perder ~0.5kg/semana
        'mantener': 0,
        'subir': 300        # Superávit para ganar masa muscular
    }

    ajuste = ajustes.get(objetivo.lower(), 0)
    return round(calorias_mantenimiento + ajuste)


def calcular_macros(calorias, objetivo='mantener'):
    """
    Calcula la distribución de macronutrientes.

    La distribución varía según el objetivo:
    - Bajar peso: más proteína para preservar músculo
    - Mantener: distribución balanceada
    - Subir peso: más carbohidratos para energía

    Args:
        calorias: Calorías totales objetivo
        objetivo: 'bajar', 'mantener', o 'subir'

    Returns:
        Diccionario con gramos de cada macronutriente
    """
    distribuciones = {
        'bajar': {'proteinas': 0.35, 'carbs': 0.40, 'grasas': 0.25},
        'mantener': {'proteinas': 0.30, 'carbs': 0.45, 'grasas': 0.25},
        'subir': {'proteinas': 0.25, 'carbs': 0.50, 'grasas': 0.25}
    }

    dist = distribuciones.get(objetivo.lower(), distribuciones['mantener'])

    return {
        'proteinas': round(calorias * dist['proteinas'] / 4),
        'carbohidratos': round(calorias * dist['carbs'] / 4),
        'grasas': round(calorias * dist['grasas'] / 9),
        'distribucion': {
            'proteinas_pct': int(dist['proteinas'] * 100),
            'carbs_pct': int(dist['carbs'] * 100),
            'grasas_pct': int(dist['grasas'] * 100)
        }
    }


def calcular_agua_recomendada(peso, nivel_actividad='sedentario'):
    """
    Calcula la cantidad de agua recomendada por día.

    Args:
        peso: Peso en kg
        nivel_actividad: Nivel de actividad física

    Returns:
        Litros de agua recomendados
    """
    # Base: 35ml por kg de peso
    agua_base = peso * 0.035

    # Ajuste por actividad
    ajustes_agua = {
        'sedentario': 0,
        'ligero': 0.3,
        'moderado': 0.5,
        'activo': 0.7,
        'muy_activo': 1.0
    }

    ajuste = ajustes_agua.get(nivel_actividad, 0)
    return round(agua_base + ajuste, 1)


def calcular_todo(peso, altura, edad, sexo, objetivo, nivel_actividad='sedentario'):
    """
    Función principal que calcula TMB, calorías y macros.

    Returns:
        Diccionario con todos los resultados
    """
    tmb = calcular_tmb(peso, altura, edad, sexo)
    calorias_mantenimiento = calcular_calorias_mantenimiento(tmb, nivel_actividad)
    calorias_objetivo = calcular_calorias_objetivo(calorias_mantenimiento, objetivo)
    macros = calcular_macros(calorias_objetivo, objetivo)
    agua = calcular_agua_recomendada(peso, nivel_actividad)

    return {
        'tmb': round(tmb),
        'calorias_mantenimiento': calorias_mantenimiento,
        'calorias_objetivo': calorias_objetivo,
        'proteinas_g': macros['proteinas'],
        'carbohidratos_g': macros['carbohidratos'],
        'grasas_g': macros['grasas'],
        'distribucion': macros['distribucion'],
        'agua_litros': agua,
        'nivel_actividad': FACTORES_ACTIVIDAD.get(nivel_actividad, FACTORES_ACTIVIDAD['sedentario'])['nombre']
    }


def calcular_imc(peso, altura_cm):
    """
    Calcula el Índice de Masa Corporal.

    Args:
        peso: Peso en kg
        altura_cm: Altura en centímetros

    Returns:
        Diccionario con IMC y clasificación
    """
    altura_m = altura_cm / 100
    imc = peso / (altura_m ** 2)

    if imc < 18.5:
        clasificacion = 'Bajo peso'
        color = '#3498db'
    elif imc < 25:
        clasificacion = 'Normal'
        color = '#27ae60'
    elif imc < 30:
        clasificacion = 'Sobrepeso'
        color = '#f39c12'
    else:
        clasificacion = 'Obesidad'
        color = '#e74c3c'

    return {
        'imc': round(imc, 1),
        'clasificacion': clasificacion,
        'color': color
    }
