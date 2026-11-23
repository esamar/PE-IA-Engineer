import logging
from fastapi import FastAPI
from app.schemas import SolicitudIn, ClassificacionOut
from app.service import clasificar_solicitud

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app=FastAPI(title="AI Service Desk", description="este es un ejemplo", version="1.0.0")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/classificar", response_model=ClassificacionOut)
def classificar(solicitud: SolicitudIn) -> ClassificacionOut:
    logger.info(f"clasificando solicitud de {solicitud.cliente}")
    return clasificar_solicitud(solicitud)