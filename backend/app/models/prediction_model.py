from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PredictionRequest(BaseModel):
    branch_name: str
    periods: int = 30
    frequency: str = "D"

class Prediction(BaseModel):
    date: str
    predicted_value: float
    lower_bound: float
    upper_bound: float

class ModelPerformance(BaseModel):
    mae: float
    mape: float
    accuracy: float

class Metrics(BaseModel):
    total_sales: float
    average_daily_sales: float
    trend_percentage: float

class PredictionResponse(BaseModel):
    predictions: List[Prediction]
    metrics: Metrics
    model_performance: ModelPerformance