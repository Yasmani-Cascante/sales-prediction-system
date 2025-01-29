from prophet import Prophet
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

class PredictionService:
    def __init__(self):
        self.models = {}  # Cache para modelos por sucursal
        self.data = {}    # Cache para datos históricos

    def configure_model(self, branch_name: str) -> Prophet:
        """Configura un modelo Prophet específico para una sucursal"""
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=True,
            interval_width=0.95
        )
        
        # Añadir festivos suizos
        model.add_country_holidays(country_name='CH')
        
        # Añadir estacionalidades personalizadas para restaurantes
        model.add_seasonality(
            name='lunch_rush',
            period=0.5,
            fourier_order=3
        )
        
        model.add_seasonality(
            name='dinner_rush',
            period=0.5,
            fourier_order=3
        )
        
        return model

    def get_historical_data(self, branch_name: str) -> pd.DataFrame:
        """Obtiene datos históricos para una sucursal específica"""
        # TODO: Implementar conexión con base de datos real
        # Por ahora, generamos datos sintéticos
        dates = pd.date_range(
            start='2024-01-01',
            end='2024-12-31',
            freq='D'
        )
        
        # Simulamos patrones realistas para un restaurante
        base_sales = 1000  # Ventas base
        weekly_pattern = [1.2, 0.8, 0.8, 0.9, 1.0, 1.5, 1.3]  # Patrón semanal
        
        sales = []
        for i, date in enumerate(dates):
            # Base + patrón semanal + tendencia + ruido aleatorio
            daily_sales = (
                base_sales * 
                weekly_pattern[date.weekday()] * 
                (1 + i * 0.001) +  # Tendencia positiva
                np.random.normal(0, 50)  # Ruido aleatorio
            )
            sales.append(max(0, daily_sales))  # Aseguramos valores no negativos
        
        return pd.DataFrame({
            'ds': dates,
            'y': sales
        })

    def train_model(self, branch_name: str) -> None:
        """Entrena el modelo para una sucursal específica"""
        data = self.get_historical_data(branch_name)
        model = self.configure_model(branch_name)
        model.fit(data)
        
        self.models[branch_name] = model
        self.data[branch_name] = data

    def predict(self, branch_name: str, periods: int = 30) -> Dict[str, Any]:
        """Genera predicciones para una sucursal"""
        if branch_name not in self.models:
            self.train_model(branch_name)
        
        model = self.models[branch_name]
        
        # Generar predicciones
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        # Calcular métricas adicionales
        historical_data = self.data[branch_name]
        total_sales = historical_data['y'].sum()
        average_daily_sales = historical_data['y'].mean()
        trend = ((forecast['yhat'].iloc[-1] - forecast['yhat'].iloc[0]) / 
                forecast['yhat'].iloc[0] * 100)
        
        # Formatear predicciones
        predictions = []
        for _, row in forecast.tail(periods).iterrows():
            predictions.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted_value': round(row['yhat'], 2),
                'lower_bound': round(row['yhat_lower'], 2),
                'upper_bound': round(row['yhat_upper'], 2)
            })
        
        return {
            'predictions': predictions,
            'metrics': {
                'total_sales': round(total_sales, 2),
                'average_daily_sales': round(average_daily_sales, 2),
                'trend_percentage': round(trend, 2),
            }
        }

    def get_model_performance(self, branch_name: str) -> Dict[str, float]:
        """Calcula métricas de rendimiento del modelo"""
        if branch_name not in self.models:
            self.train_model(branch_name)
            
        model = self.models[branch_name]
        data = self.data[branch_name]
        
        # Calcular predicciones para datos históricos
        historical_forecast = model.predict(model.history)
        
        # Calcular métricas de error
        mae = np.mean(np.abs(data['y'] - historical_forecast['yhat']))
        mape = np.mean(np.abs((data['y'] - historical_forecast['yhat']) / data['y'])) * 100
        
        return {
            'mae': round(mae, 2),
            'mape': round(mape, 2),
            'accuracy': round(100 - mape, 2)
        }