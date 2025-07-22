"""
Utilidades para mapear entre el formato de períodos de la base de datos
y el formato esperado por el frontend.

BD usa: "2025-1", "2025-2", "2025-3"
Frontend espera: "parcial1", "parcial2", "parcial3"
"""

def bd_periodo_to_frontend(bd_periodo: str) -> str:
    """
    Convierte período de BD ("2025-1") a formato frontend ("parcial1")
    """
    mapping = {
        "2025-1": "parcial1",
        "2025-2": "parcial2", 
        "2025-3": "parcial3"
    }
    return mapping.get(bd_periodo, bd_periodo)

def frontend_periodo_to_bd(frontend_periodo: str, year: int = 2025) -> str:
    """
    Convierte período de frontend ("parcial1") a formato BD ("2025-1")
    """
    mapping = {
        "parcial1": f"{year}-1",
        "parcial2": f"{year}-2",
        "parcial3": f"{year}-3"
    }
    return mapping.get(frontend_periodo, frontend_periodo)

def get_periodo_number_from_frontend(frontend_periodo: str) -> int:
    """
    Extrae el número del período del formato frontend
    """
    mapping = {
        "parcial1": 1,
        "parcial2": 2,
        "parcial3": 3
    }
    return mapping.get(frontend_periodo, 1)

def calcular_promedio(notas: list) -> float:
    """
    Calcula el promedio de una lista de notas, ignorando valores None
    """
    notas_validas = [nota for nota in notas if nota is not None]
    if not notas_validas:
        return 0.0
    return round(sum(notas_validas) / len(notas_validas), 2)
