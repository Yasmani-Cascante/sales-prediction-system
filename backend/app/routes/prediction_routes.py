from fastapi import APIRouter, HTTPException
from ..models.prediction_model import PredictionRequest, PredictionResponse
from ..services.prediction_service import PredictionService

prediction_router = APIRouter()
prediction_service = PredictionService()

@prediction_router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Genera predicciones de ventas para una sucursal específica.
    
    - **branch_name**: Nombre de la sucursal
    - **periods**: Número de períodos a predecir (default: 30)
    - **frequency**: Frecuencia de predicción (default: "D" para diario)
    """
    try:
        return await prediction_service.get_predictions(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))