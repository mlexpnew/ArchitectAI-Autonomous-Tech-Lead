"""
Service Generator

Generates Business Logic Layer.
"""

from pathlib import Path

from generators.writer import FileWriter


class ServiceGenerator:

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)

    # ==========================================================
    # Dynamic Service Generator Entry Point
    # ==========================================================

    def generate_service(
        self,
        entity,
    ):
        """
        Generate service for an entity.
        """

        return self.generate_service_full(entity)

    # ==========================================================
    # Full Service Generator
    # ==========================================================

    def generate_service_full(
        self,
        entity,
    ):
        """
        Generate production CRUD service.
        """

        class_name = entity.name
        lower = class_name.lower()

        code = f'''"""
{class_name} Service
"""

from sqlalchemy.orm import Session

from app.models.{lower} import {class_name}

from app.repositories.{lower}_repository import (
    {class_name}Repository,
)


class {class_name}Service:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = {class_name}(
            **data.model_dump()
        )

        return {class_name}Repository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return {class_name}Repository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return {class_name}Repository.get_all(
            db,
            skip=skip,
            limit=limit,
        )


    @staticmethod
    def update(
        db: Session,
        obj_id: int,
        data,
    ):
        update_data = data.model_dump(
            exclude_unset=True
        )

        return {class_name}Repository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return {class_name}Repository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return {class_name}Repository.exists(
            db,
            obj_id,
        )
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "services"
            / f"{lower}_service.py",
            code,
        )

        print(
            f"✅ Generated {class_name} Service"
        )

    # ==========================================================
    # Legacy Pipeline Compatibility
    # ==========================================================

    def generate(self):
        """
        Compatibility method for legacy pipeline.
        """

        print(
            "ℹ️ Services are generated dynamically "
            "using generate_service(entity)"
        )