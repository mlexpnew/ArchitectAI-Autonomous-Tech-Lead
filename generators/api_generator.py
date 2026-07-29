"""
API Generator

Generates production-ready FastAPI CRUD endpoints.
"""

from pathlib import Path

from generators.writer import FileWriter


class APIGenerator:

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)

    def generate_api(
        self,
        entity,
    ):
        """
        Generate CRUD API endpoints dynamically.
        """

        name = entity.name
        lower = name.lower()

        code = f'''"""
{name} API
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.{lower} import (
    {name}Create,
    {name}Update,
    {name}Response,
)

from app.services.{lower}_service import (
    {name}Service,
)


router = APIRouter(
    prefix="/{lower}s",
    tags=["{name}"],
)

service = {name}Service()


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model={name}Response,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: {name}Create,
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
    response_model=list[{name}Response],
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
    "/{{obj_id}}",
    response_model={name}Response,
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
            detail="{name} not found",
        )

    return obj


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{{obj_id}}",
    response_model={name}Response,
)
def update(
    obj_id: int,
    data: {name}Update,
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
            detail="{name} not found",
        )

    return obj


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{{obj_id}}",
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
            detail="{name} not found",
        )

    return {{
        "message": "{name} deleted successfully"
    }}
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "api"
            / f"{lower}.py",
            code,
        )

        print(
            f"✅ Generated {name} API"
        )