```python
from pydantic import BaseModel, Field
from typing import Optional

class Billing(BaseModel):
    id: int = Field(..., description="Unique identifier for the billing")
    appointment_id: int = Field(..., description="Foreign key referencing the appointment")
    medicine_id: int = Field(..., description="Foreign key referencing the medicine")
    quantity: int = Field(..., description="Quantity of the medicine")
    total: float = Field(..., description="Total cost of the medicine")

class PatientCreate(BaseModel):
    appointment_id: int = Field(..., description="Foreign key referencing the appointment")
    medicine_id: int = Field(..., description="Foreign key referencing the medicine")
    quantity: int = Field(..., description="Quantity of the medicine")
    total: float = Field(..., description="Total cost of the medicine")

class PatientUpdate(BaseModel):
    appointment_id: Optional[int] = Field(None, description="Foreign key referencing the appointment")
    medicine_id: Optional[int] = Field(None, description="Foreign key referencing the medicine")
    quantity: Optional[int] = Field(None, description="Quantity of the medicine")
    total: Optional[float] = Field(None, description="Total cost of the medicine")

class PatientResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for the billing")
    appointment_id: int = Field(..., description="Foreign key referencing the appointment")
    medicine_id: int = Field(..., description="Foreign key referencing the medicine")
    quantity: int = Field(..., description="Quantity of the medicine")
    total: float = Field(..., description="Total cost of the medicine")
```

Note: The `from_attributes=True` parameter is not needed in Pydantic V2 as it's the default behavior.