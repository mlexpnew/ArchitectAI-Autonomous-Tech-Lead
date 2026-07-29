```python
from pydantic import BaseModel, Field
from typing import Optional

class PatientCreate(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the patient")
    name: str = Field(..., description="Patient's name")
    age: int = Field(..., description="Patient's age")
    phone: str = Field(..., description="Patient's phone number")

    class Config:
        from_attributes = True


class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Patient's name")
    age: Optional[int] = Field(None, description="Patient's age")
    phone: Optional[str] = Field(None, description="Patient's phone number")

    class Config:
        from_attributes = True


class PatientResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for the patient")
    name: str = Field(..., description="Patient's name")
    age: int = Field(..., description="Patient's age")
    phone: str = Field(..., description="Patient's phone number")

    class Config:
        from_attributes = True
```

This code defines three Pydantic V2 schemas:

- `PatientCreate`: for creating a new patient, with all fields required.
- `PatientUpdate`: for updating an existing patient, with fields optional.
- `PatientResponse`: for returning a patient's details, with all fields required.

The `from_attributes=True` configuration is used to automatically generate the `__init__` method from the model's attributes, making the models more Pythonic and easier to use.