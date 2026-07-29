```python
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from typing import Optional

class Payment(BaseModel):
    id: int
    patient_id: int
    amount: Decimal
    payment_method: str
    date: date

class PatientCreate(Payment):
    pass

class PatientUpdate(Payment):
    pass

class PatientResponse(Payment):
    pass
```

However, the above code does not utilize the full potential of Pydantic V2. Here's an improved version with additional features:

```python
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from typing import Optional

class Payment(BaseModel):
    id: int = Field(..., title="Unique identifier for the payment")
    patient_id: int = Field(..., title="Identifier of the patient")
    amount: Decimal = Field(..., title="Amount paid", description="The amount paid in the currency")
    payment_method: str = Field(..., title="Method of payment", description="The method of payment used")
    date: date = Field(..., title="Date of payment", description="The date the payment was made")

    class Config:
        from_attributes = True

class PatientCreate(Payment):
    pass

class PatientUpdate(Payment):
    pass

class PatientResponse(Payment):
    pass
```

In this improved version, we've added the following features:

- Added `title` and `description` parameters to the `Field` constructor to provide additional metadata for the fields.
- Added a `Config` class to the `Payment` model to enable the `from_attributes` feature.
- Utilized the `...` syntax to indicate that the fields are required.