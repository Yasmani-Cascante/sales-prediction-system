from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.prediction_routes import prediction_router

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

# Incluir rutas
app.include_router(prediction_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Sistema de Predicción de Ventas API"}