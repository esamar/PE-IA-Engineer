from app.schemas import SolicitudIn, ClassificacionOut
from typing import Protocol
import unicodedata

PALABRAS_URGENTES = ["urgente", "caido", "caído", "no puedo", "sin servicio", "no funciona"]

def normalizar(texto:str)->str:
    """Minusculas y sin marcas de acentos para comparar expresiones"""

    texto=unicodedata.normalize("NFKD", texto.casefold())
    return "".join(caracter for caracter in texto if not unicodedata.combining(caracter))

class Clasificador(Protocol):
    def clasificar(self, solicitud: SolicitudIn) ->ClassificacionOut:...

class clasificadorreglas:
    def clasificar(self, solicitud: SolicitudIn) -> ClassificacionOut:
        mensaje = normalizar(solicitud.mensaje)
        es_urgente = any(palabra in mensaje for palabra in PALABRAS_URGENTES)

        return ClassificacionOut(
            cliente=solicitud.cliente,
            categoria="incidente" if es_urgente else "consulta",
            prioridad="alta" if es_urgente else "normal",
            requiere_atencion=es_urgente,
            metodo="reglas_deterministas",
        )

def obtener_clasificado() -> Clasificador:
    """Punto de entension para un clasificador LLM en proximos cursos."""
    return clasificadorreglas()

def clasificar_solicitud(solicitud: SolicitudIn) -> ClassificacionOut:
    cliente = solicitud.cliente
    mensaje = solicitud.mensaje.lower()
    es_urgente = any(palabra in mensaje for palabra in PALABRAS_URGENTES)
    return ClassificacionOut(
        cliente=cliente,
        categoria="incidente" if es_urgente else "consulta", 
        prioridad="alta" if es_urgente else "normal",
        requiere_atencion=es_urgente,
        metodo="reglas_deterministas"
    )