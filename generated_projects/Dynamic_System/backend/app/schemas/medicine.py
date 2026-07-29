"""
Medicine Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class MedicineBase(BaseModel):
    name: str
    description: str
    price: float


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None


class MedicineResponse(MedicineBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
