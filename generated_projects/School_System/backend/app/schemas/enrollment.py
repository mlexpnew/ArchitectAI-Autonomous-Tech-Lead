"""
Enrollment Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class EnrollmentBase(BaseModel):
    enrollment_date: DateType
    grade: str


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    enrollment_date: DateType | None = None
    grade: str | None = None


class EnrollmentResponse(EnrollmentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
