```python
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal

class PatientCreate(BaseModel):
    patient_id: int
    amount: Decimal
    payment_status: str
    date: date

    class Config:
        from_attributes = True

class PatientUpdate(BaseModel):
    patient_id: int | None
    amount: Decimal | None
    payment_status: str | None
    date: date | None

    class Config:
        from_attributes = True

class PatientResponse(BaseModel):
    id: int
    patient_id: int
    amount: Decimal
    payment_status: str
    date: date

    class Config:
        from_attributes = True
```

This code defines three Pydantic V2 schemas for Patient: `PatientCreate`, `PatientUpdate`, and `PatientResponse`. Each schema includes the required fields with type hints and uses the `from_attributes=True` configuration to enable attribute-based initialization. The `PatientResponse` schema includes the `id` field, which is not present in the `PatientCreate` schema.