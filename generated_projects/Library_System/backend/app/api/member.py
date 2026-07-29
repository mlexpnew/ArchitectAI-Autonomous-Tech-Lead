"""
Member API
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.member import (
    MemberCreate,
    MemberUpdate,
    MemberResponse,
)

from app.services.member_service import (
    MemberService,
)


router = APIRouter(
    prefix="/members",
    tags=["Member"],
)

service = MemberService()


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: MemberCreate,
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
    response_model=list[MemberResponse],
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
    response_model=MemberResponse,
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
            detail="Member not found",
        )

    return obj


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{obj_id}",
    response_model=MemberResponse,
)
def update(
    obj_id: int,
    data: MemberUpdate,
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
            detail="Member not found",
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
            detail="Member not found",
        )

    return {
        "message": "Member deleted successfully"
    }
