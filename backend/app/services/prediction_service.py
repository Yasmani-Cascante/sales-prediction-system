from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ..models.prediction_model import PredictionRequest, Prediction, ModelPerformance, Metrics, PredictionResponse

class PredictionService:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.data = {}

    def prepare_features(self, dates):
        """Prepara características para el modelo."""
        features = pd.DataFrame({
            'year': dates.dt.year,
            'month': dates.dt.month,
            'day': dates.dt.day,
            'day_of_week': dates.dt.dayofweek,
            'day_of_year': dates.dt.dayofyear,
            'is_weekend': dates.dt.dayofweek.isin([5, 6]).astype(int),
            'is_month_start': dates.dt.is_month_start.astype(int),
            'is_month_end': dates.dt.is_month_end.astype(int)
        })
        
        # Agregar características cíclicas para capturar estacionalidad
        features['month_sin'] = np.sin(2 * np.pi * features['month']/12)
        features['month_cos'] = np.cos(2 * np.pi * features['month']/12)
        features['day_sin'] = np.sin(2 * np.pi * features['day_of_year']/365)
        features['day_cos'] = np.cos(2 * np.pi * features['day_of_year']/365)
        
        return features

    def get_historical_data(self, branch_name: str) -> pd.DataFrame:
        """Genera datos históricos simulados."""
        dates = pd.date_range(
            start='2024-01-01',
            end='2024-12-31',
            freq='D'
        )
        
        base_sales = 1000
        weekly_pattern = [1.2, 0.8, 0.8, 0.9, 1.0, 1.5, 1.3]
        
        sales = []
        for i, date in enumerate(dates):
            daily_sales = (
                base_sales * 
                weekly_pattern[date.dayofweek] * 
                (1 + i * 0.001) +  # Tendencia ligera al alza
                np.random.normal(0, 50)  # Ruido aleatorio
            )
            sales.append(max(0, daily_sales))
        
        return pd.DataFrame({
            'ds': dates,
            'y': sales
        })

    async def train_model(self, branch_name: str) -> None:
        """Entrena el modelo para una sucursal específica."""
        try:
            # Obtener datos históricos
            data = self.get_historical_data(branch_name)
            self.data[branch_name] = data
            
            # Preparar características
            X = self.prepare_features(data['ds'])
            y = data['y']
            
            # Escalar características
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers[branch_name] = scaler
            
            # Entrenar modelo
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            model.fit(X_scaled, y)
            
            self.models[branch_name] = model
            
        except Exception as e:
            print(f"Error during training: {str(e)}")
            raise

    async def get_predictions(self, request: PredictionRequest) -> PredictionResponse:
        """Genera predicciones para una sucursal específica."""
        try:
            if request.branch_name not in self.models:
                await self.train_model(request.branch_name)
            
            model = self.models[request.branch_name]
            scaler = self.scalers[request.branch_name]
            historical_data = self.data[request.branch_name]
            
            # Generar fechas futuras
            last_date = historical_data['ds'].iloc[-1]
            future_dates = pd.date_range(
                start=last_date + timedelta(days=1),
                periods=request.periods,
                freq='D'
            )
            
            # Preparar características futuras
            future_features = self.prepare_features(pd.Series(future_dates))
            future_features_scaled = scaler.transform(future_features)
            
            # Generar predicciones
            predictions = model.predict(future_features_scaled)
            
            # Calcular intervalos de confianza
            # Usar los árboles individuales para estimar la incertidumbre
            predictions_trees = np.array([tree.predict(future_features_scaled) 
                                       for tree in model.estimators_])
            lower_bound = np.percentile(predictions_trees, 2.5, axis=0)
            upper_bound = np.percentile(predictions_trees, 97.5, axis=0)
            
            # Calcular métricas
            total_sales = historical_data['y'].sum()
            average_daily_sales = historical_data['y'].mean()
            trend = ((predictions[-1] - predictions[0]) / predictions[0] * 100)
            
            # Calcular métricas de rendimiento del modelo
            historical_features = self.prepare_features(historical_data['ds'])
            historical_features_scaled = scaler.transform(historical_features)
            historical_predictions = model.predict(historical_features_scaled)
            
            mae = np.mean(np.abs(historical_data['y'] - historical_predictions))
            mape = np.mean(np.abs((historical_data['y'] - historical_predictions) / 
                                 historical_data['y'])) * 100
            
            # Preparar predicciones en el formato requerido
            predictions_list = [
                Prediction(
                    date=date.strftime('%Y-%m-%d'),
                    predicted_value=round(pred, 2),
                    lower_bound=round(lb, 2),
                    upper_bound=round(ub, 2)
                )
                for date, pred, lb, ub in zip(future_dates, predictions, lower_bound, upper_bound)
            ]
            
            return PredictionResponse(
                predictions=predictions_list,
                metrics=Metrics(
                    total_sales=round(total_sales, 2),
                    average_daily_sales=round(average_daily_sales, 2),
                    trend_percentage=round(trend, 2)
                ),
                model_performance=ModelPerformance(
                    mae=round(mae, 2),
                    mape=round(mape, 2),
                    accuracy=round(100 - mape, 2)
                )
            )
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            raise