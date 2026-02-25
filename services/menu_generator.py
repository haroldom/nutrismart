"""
Generador de menú diario con comidas peruanas.
"""
import random
from database.models import obtener_comidas_por_tipo


def generar_menu_diario(calorias_objetivo):
    """
    Genera un menú diario que se aproxime a las calorías objetivo.

    Distribución aproximada:
        - Desayuno: 25% de calorías
        - Almuerzo: 45% de calorías
        - Cena: 30% de calorías

    Args:
        calorias_objetivo: Calorías totales del día

    Returns:
        Diccionario con el menú y totales nutricionales
    """
    desayunos = obtener_comidas_por_tipo('desayuno')
    almuerzos = obtener_comidas_por_tipo('almuerzo')
    cenas = obtener_comidas_por_tipo('cena')

    # Calorías objetivo por comida
    cal_desayuno = calorias_objetivo * 0.25
    cal_almuerzo = calorias_objetivo * 0.45
    cal_cena = calorias_objetivo * 0.30

    # Seleccionar comida más cercana a cada objetivo
    desayuno = seleccionar_comida_cercana(desayunos, cal_desayuno)
    almuerzo = seleccionar_comida_cercana(almuerzos, cal_almuerzo)
    cena = seleccionar_comida_cercana(cenas, cal_cena)

    # Calcular totales
    total_calorias = desayuno['calorias'] + almuerzo['calorias'] + cena['calorias']
    total_proteinas = desayuno['proteinas'] + almuerzo['proteinas'] + cena['proteinas']
    total_carbs = desayuno['carbs'] + almuerzo['carbs'] + cena['carbs']
    total_grasas = desayuno['grasas'] + almuerzo['grasas'] + cena['grasas']

    return {
        'desayuno': desayuno,
        'almuerzo': almuerzo,
        'cena': cena,
        'totales': {
            'calorias': total_calorias,
            'proteinas': round(total_proteinas, 1),
            'carbs': round(total_carbs, 1),
            'grasas': round(total_grasas, 1)
        },
        'calorias_objetivo': calorias_objetivo,
        'diferencia': total_calorias - calorias_objetivo
    }


def seleccionar_comida_cercana(comidas, calorias_objetivo):
    """
    Selecciona la comida más cercana al objetivo de calorías.
    Si hay varias cercanas, elige una al azar entre ellas.
    """
    if not comidas:
        return None

    # Ordenar por diferencia con el objetivo
    comidas_ordenadas = sorted(
        comidas,
        key=lambda c: abs(c['calorias'] - calorias_objetivo)
    )

    # Tomar las 3 más cercanas y elegir una al azar
    mejores = comidas_ordenadas[:min(3, len(comidas_ordenadas))]
    return random.choice(mejores)


def generar_menu_semanal(calorias_objetivo):
    """
    Genera un menú para toda la semana.

    Returns:
        Lista con 7 menús diarios
    """
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    menu_semanal = []

    for dia in dias:
        menu_dia = generar_menu_diario(calorias_objetivo)
        menu_dia['dia'] = dia
        menu_semanal.append(menu_dia)

    return menu_semanal
