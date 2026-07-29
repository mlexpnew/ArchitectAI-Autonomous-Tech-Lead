"""
BorrowRecord Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class BorrowRecordBase(BaseModel):
    borrow_date: DateType
    due_date: DateType
    return_date: DateType


class BorrowRecordCreate(BorrowRecordBase):
    pass


class BorrowRecordUpdate(BaseModel):
    borrow_date: DateType | None = None
    due_date: DateType | None = None
    return_date: DateType | None = None


class BorrowRecordResponse(BorrowRecordBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
