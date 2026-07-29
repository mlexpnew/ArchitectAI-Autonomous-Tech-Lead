```python
from pydantic import BaseModel, Field
from typing import Optional

class Staff(BaseModel):
    id: int
    name: str
    role: str
    email: str
    phone: str
    address: str

class PatientCreate(BaseModel):
    name: str
    role: str
    email: str
    phone: str
    address: str
    from_attributes: bool = Field(default=True)

class PatientUpdate(BaseModel):
    name: Optional[str]
    role: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]

class PatientResponse(BaseModel):
    id: int
    name: str
    role: str
    email: str
    phone: str
    address: str
```

This code defines the Staff entity as a Pydantic model, and then defines the PatientCreate, PatientUpdate, and PatientResponse models according to the provided requirements. The `from_attributes=True` parameter is set for the PatientCreate model to enable the use of the `from_attributes` method.