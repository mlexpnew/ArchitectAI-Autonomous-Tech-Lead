
"""
Repository Generator

Generates SQLAlchemy repository classes.
"""

from pathlib import Path

from generators.writer import FileWriter


class RepositoryGenerator:

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)

    def generate_repository(
        self,
        entity,
    ):
        """
        Generate repository dynamically.
        """

        class_name = entity.name
        lower = class_name.lower()

        code = f'''"""
{class_name} Repository
"""

from sqlalchemy.orm import Session

from app.models.{lower} import {class_name}


class {class_name}Repository:

    @staticmethod
    def create(
        db: Session,
        obj: {class_name},
    ):
        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return (
            db.query({class_name})
            .filter({class_name}.id == obj_id)
            .first()
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return (
            db.query({class_name})
            .offset(skip)
            .limit(limit)
            .all()
        )


    @staticmethod
    def update(
        db: Session,
        obj_id: int,
        data: dict,
    ):
        obj = (
            db.query({class_name})
            .filter({class_name}.id == obj_id)
            .first()
        )

        if obj is None:
            return None

        for key, value in data.items():

            if key == "id":
                continue

            if hasattr(obj, key):
                setattr(obj, key, value)

        db.commit()
        db.refresh(obj)

        return obj


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        obj = (
            db.query({class_name})
            .filter({class_name}.id == obj_id)
            .first()
        )

        if obj is None:
            return None

        db.delete(obj)
        db.commit()

        return obj


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return (
            db.query({class_name}.id)
            .filter({class_name}.id == obj_id)
            .first()
            is not None
        )
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "repositories"
            / f"{lower}_repository.py",
            code,
        )

        print(
            f"✅ Generated {class_name} Repository"
        )

    def generate(self):
        """
        Compatibility method for the legacy pipeline.
        """

        print(
            "ℹ️ Repositories are generated dynamically "
            "using generate_repository(entity)"
        )