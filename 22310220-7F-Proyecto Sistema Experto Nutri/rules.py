from database import ALIMENTOS

def recomendar_alimentos(sintoma):
    # reglas simples de inferencia
    reglas = {
        "Diarrea": ["blanda"],
        "Vomito": ["blanda"],
        "Gripe": ["ligera"],
        "Fatiga": ["alta energia"],
        "Bajar de peso": ["ligera"],
        "Subir masa muscular": ["rica en proteina"],
    }

    if sintoma not in reglas:
        return []

    categorias_recomendadas = reglas[sintoma]

    # Inferencia: filtrar alimentos que pertenezcan a esas categorías
    recomendaciones = [
        alimento for alimento in ALIMENTOS 
        if alimento["tipo"] in categorias_recomendadas
    ]

    return recomendaciones
