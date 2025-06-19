from datetime import date
from typing import List, Optional
from pydantic import BaseModel, field_validator

class CostQueryParams(BaseModel):
    start_date: date
    end_date: date

    @field_validator('end_date')
    def end_date_must_be_after_start_date(cls, v: date, info):
        start_date = info.data.get('start_date')
        if start_date and v < start_date:
            raise ValueError('end_date must be after start_date')
        return v

class ServiceCost(BaseModel):
    service_name: str
    amount: float
    currency: str

class CostResponse(BaseModel):
    start_date: date
    end_date: date
    total_cost: float
    currency: str
    costs_by_service: List[ServiceCost]
    time_period_start: Optional[str]
    time_period_end: Optional[str]
