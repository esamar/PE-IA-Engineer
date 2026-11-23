import pytest

from app.schemas import SolicitudIn
from app.service import clasificadorreglas, normalizar

@pytest.mark.parametrize("mensaje", [
    "Mi ssitema està CaÌdo",
    "El servicio està caido",
    "No puedo facturar",
    "Estamos SIN SERVICIO",
    "Es urgente resolverlo"]
)

def test_mensaje_urgentes(mensaje:str)->None:
    solicitud = SolicitudIn(cliente="Empresa ABC", mensaje=mensaje, canal="web")
    resultado = clasificadorreglas().clasificar(solicitud)
    assert resultado.prioridad == "alta"
    assert resultado.categoria == "incidente"

def test_consulta_normal() -> None:
    solicitud = SolicitudIn(cliente="Empresa ABC", mensaje="Necesito consultar mi estado", canal="correo")
    resultado = clasificadorreglas().clasificar(solicitud)
    assert resultado.prioridad == "normal"
    assert resultado.requiere_atencion == False

def test_normalizador_acentos()->None:
    assert normalizar("CAÌDO") == "caido"