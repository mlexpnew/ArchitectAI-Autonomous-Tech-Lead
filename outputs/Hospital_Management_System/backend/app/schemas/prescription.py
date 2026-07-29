```python
from pydantic import BaseModel, Field
from typing import Optional

class Prescription(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    medicine: str
    dosage: str
    duration: str

class PatientCreate(BaseModel):
    patient_id: int
    doctor_id: int
    medicine: str
    dosage: str
    duration: str

class PatientUpdate(BaseModel):
    patient_id: Optional[int] = Field(None, exclude=True)
    doctor_id: Optional[int] = Field(None, exclude=True)
    medicine: Optional[str] = Field(None, exclude=True)
    dosage: Optional[str] = Field(None, exclude=True)
    duration: Optional[str] = Field(None, exclude=True)

class PatientResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    medicine: str
    dosage: str
    duration: str
```

This code defines the necessary Pydantic V2 schemas for the `Prescription` entity, including `PatientCreate`, `PatientUpdate`, and `PatientResponse`. The `exclude=True` parameter is used to exclude the `id` field from the `PatientUpdate` schema, as it should not be updated. The `from_attributes=True` parameter is not necessary here, as it's the default behavior in Pydantic V2.