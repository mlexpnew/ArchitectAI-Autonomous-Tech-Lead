```python
from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional

class Schedule(BaseModel):
    id: int
    doctor_id: int
    date: date
    time: time
    status: str

class PatientCreate(BaseModel):
    id: int = Field(..., description="Patient ID")
    doctor_id: int = Field(..., description="Doctor ID")
    date: date = Field(..., description="Schedule date")
    time: time = Field(..., description="Schedule time")
    status: str = Field(..., description="Schedule status")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "doctor_id": 1,
                "date": "2024-03-16",
                "time": "10:00:00",
                "status": "pending"
            }
        }

class PatientUpdate(BaseModel):
    id: Optional[int] = Field(None, description="Patient ID")
    doctor_id: Optional[int] = Field(None, description="Doctor ID")
    date: Optional[date] = Field(None, description="Schedule date")
    time: Optional[time] = Field(None, description="Schedule time")
    status: Optional[str] = Field(None, description="Schedule status")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "doctor_id": 1,
                "date": "2024-03-16",
                "time": "10:00:00",
                "status": "confirmed"
            }
        }

class PatientResponse(BaseModel):
    id: int
    doctor_id: int
    date: date
    time: time
    status: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "doctor_id": 1,
                "date": "2024-03-16",
                "time": "10:00:00",
                "status": "pending"
            }
        }
```

This code defines the required Pydantic V2 schemas for the Schedule entity. It includes the `Schedule`, `PatientCreate`, `PatientUpdate`, and `PatientResponse` models, each with the specified fields and type hints. The `Config` class is used to add additional metadata to each model, including example values for the `schema_extra` attribute.