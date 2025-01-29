
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class PredictionRequest:
    branch_name: str
    start_date: datetime
    periods: int = 30
    frequency: str = 'D'

@dataclass
class PredictionResult:
    date: datetime
    predicted_value: float
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None