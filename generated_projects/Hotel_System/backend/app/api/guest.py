"""
Guest API
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.guest import (
    GuestCreate,
    GuestUpdate,
    GuestResponse,
)

from app.services.guest_service import (
    GuestService,
)


router = APIRouter(
    prefix="/guests",
    tags=["Guest"],
)

service = GuestService()


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=GuestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: GuestCreate,
    db: Session = Depends(get_db),
):

    return service.create(
        db,
        data,
    )


# ==========================================================
# GET ALL
# ==========================================================

@router.get(
    "/",
    response_model=list[GuestResponse],
)
def get_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):

    return service.get_all(
        db,
        skip=skip,
        limit=limit,
    )


# ==========================================================
# GET BY ID
# ==========================================================

@router.get(
    "/{obj_id}",
    response_model=GuestResponse,
)
def get_by_id(
    obj_id: int,
    db: Session = Depends(get_db),
):

    obj = service.get_by_id(
        db,
        obj_id,
    )

    if obj is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )

    return obj


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{obj_id}",
    response_model=GuestResponse,
)
def update(
    obj_id: int,
    data: GuestUpdate,
    db: Session = Depends(get_db),
):

    obj = service.update(
        db,
        obj_id,
        data,
    )

    if obj is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )

    return obj


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{obj_id}",
    status_code=status.HTTP_200_OK,
)
def delete(
    obj_id: int,
    db: Session = Depends(get_db),
):

    obj = service.delete(
        db,
        obj_id,
    )

    if obj is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )

    return {
        "message": "Guest deleted successfully"
    }
