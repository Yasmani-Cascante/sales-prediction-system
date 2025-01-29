from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.prediction_model import PredictionRequest, PredictionResponse
from .services.prediction_service import PredictionService

app = FastAPI(
    title="Sistema de Predicción de Ventas",
    description="API para predicción de ventas usando Prophet",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar el servicio de predicción
prediction_service = PredictionService()

@app.get("/")
async def read_root():
    return {"message": "Sistema de Predicción de Ventas API"}

@app.post("/api/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Genera predicciones de ventas para una sucursal específica.
    
    - **branch_name**: Nombre de la sucursal
    - **periods**: Número de períodos a predecir (default: 30)
    - **frequency**: Frecuencia de predicción (default: "D" para diario)
    """
    return await prediction_service.get_predictions(request)