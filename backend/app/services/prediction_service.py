from prophet import Prophet
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ..models.prediction_model import PredictionRequest, Prediction, ModelPerformance, Metrics, PredictionResponse

class PredictionService:
    def __init__(self):
        self.models = {}
        self.data = {}

    def configure_model(self, branch_name: str) -> Prophet:
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=True,
            interval_width=0.95
        )
        
        model.add_country_holidays(country_name='CH')
        
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
                weekly_pattern[date.weekday()] * 
                (1 + i * 0.001) +  
                np.random.normal(0, 50)
            )
            sales.append(max(0, daily_sales))
        
        return pd.DataFrame({
            'ds': dates,
            'y': sales
        })

    async def train_model(self, branch_name: str) -> None:
        data = self.get_historical_data(branch_name)
        model = self.configure_model(branch_name)
        model.fit(data)
        
        self.models[branch_name] = model
        self.data[branch_name] = data

    async def get_predictions(self, request: PredictionRequest) -> PredictionResponse:
        if request.branch_name not in self.models:
            await self.train_model(request.branch_name)
        
        model = self.models[request.branch_name]
        historical_data = self.data[request.branch_name]
        
        future = model.make_future_dataframe(periods=request.periods)
        forecast = model.predict(future)
        
        total_sales = historical_data['y'].sum()
        average_daily_sales = historical_data['y'].mean()
        trend = ((forecast['yhat'].iloc[-1] - forecast['yhat'].iloc[0]) / 
                forecast['yhat'].iloc[0] * 100)
        
        historical_forecast = model.predict(model.history)
        mae = np.mean(np.abs(historical_data['y'] - historical_forecast['yhat']))
        mape = np.mean(np.abs((historical_data['y'] - historical_forecast['yhat']) / 
                              historical_data['y'])) * 100
        
        predictions = [
            Prediction(
                date=row['ds'].strftime('%Y-%m-%d'),
                predicted_value=round(row['yhat'], 2),
                lower_bound=round(row['yhat_lower'], 2),
                upper_bound=round(row['yhat_upper'], 2)
            )
            for _, row in forecast.tail(request.periods).iterrows()
        ]
        
        return PredictionResponse(
            predictions=predictions,
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