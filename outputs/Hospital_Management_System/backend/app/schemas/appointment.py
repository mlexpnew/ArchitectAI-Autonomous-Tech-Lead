```python
from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional

class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: date
    time: time
    status: str

class PatientCreate(Appointment):
    pass

class PatientUpdate(Appointment):
    status: Optional[str] = Field(None, exclude=True)

class PatientResponse(Appointment):
    patient_id: int
    doctor_id: int
    date: date
    time: time
    status: str

    class Config:
        from_attributes = True
```

Note: `exclude=True` is used to exclude the `status` field from the `PatientUpdate` schema. The `from_attributes=True` is set in the `PatientResponse` schema's config to indicate that the model should be generated from the attributes of the model.