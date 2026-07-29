```python
from pydantic import BaseModel, EmailStr, Field

class Admin(BaseModel):
    id: int = Field(..., title="Admin ID")
    name: str = Field(..., title="Admin Name")
    email: EmailStr = Field(..., title="Admin Email")
    password: str = Field(..., title="Admin Password")

class PatientCreate(BaseModel):
    name: str = Field(..., title="Patient Name")
    email: EmailStr = Field(..., title="Patient Email")
    password: str = Field(..., title="Patient Password")

class PatientUpdate(BaseModel):
    name: str | None = Field(None, title="Patient Name")
    email: EmailStr | None = Field(None, title="Patient Email")
    password: str | None = Field(None, title="Patient Password")

class PatientResponse(BaseModel):
    id: int = Field(..., title="Patient ID")
    name: str = Field(..., title="Patient Name")
    email: EmailStr = Field(..., title="Patient Email")
```

This code defines the required Pydantic V2 schemas for the Admin entity and the Patient entity. The `Admin` model is used as is, while the `PatientCreate` model is used for creating new patients, the `PatientUpdate` model is used for updating existing patients, and the `PatientResponse` model is used for returning patient data in responses.