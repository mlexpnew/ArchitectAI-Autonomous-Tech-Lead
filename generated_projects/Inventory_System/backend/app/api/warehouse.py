"""
Warehouse API
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseResponse,
)

from app.services.warehouse_service import (
    WarehouseService,
)


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouse"],
)

service = WarehouseService()


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=WarehouseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: WarehouseCreate,
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
    response_model=list[WarehouseResponse],
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
    response_model=WarehouseResponse,
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
            detail="Warehouse not found",
        )

    return obj


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{obj_id}",
    response_model=WarehouseResponse,
)
def update(
    obj_id: int,
    data: WarehouseUpdate,
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
            detail="Warehouse not found",
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
            detail="Warehouse not found",
        )

    return {
        "message": "Warehouse deleted successfully"
    }
