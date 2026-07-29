"""
Model Generator

Generates SQLAlchemy models dynamically.

Design rules:
- All models use the shared Base from app.database.
- Foreign keys are generated only when they can be validated.
- ORM relationships are generated only when backed by a real FK.
- Unsafe many-to-many relationships are skipped until association-table
  generation is available.
"""

from pathlib import Path

from generators.writer import FileWriter


class ModelGenerator:

    SQL_TYPES = {
        "integer": "Integer",
        "string": "String",
        "float": "Float",
        "boolean": "Boolean",
        "date": "Date",
        "time": "Time",
    }

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _table_name(entity_name: str) -> str:
        return f"{entity_name.lower()}s"

    @staticmethod
    def _field_names(entity) -> set[str]:
        return {
            field.name
            for field in entity.fields
        }

    @staticmethod
    def _find_entity(
        blueprint,
        entity_name: str,
    ):
        for entity in blueprint.entities:

            if entity.name == entity_name:
                return entity

        return None

    def _resolve_foreign_key(
        self,
        entity,
        field,
        blueprint,
    ):
        """
        Resolve FK target for a field.

        The safest convention is:

            patient_id -> Patient.id
            doctor_id  -> Doctor.id

        Relationship metadata is used only when it agrees
        with an actual field on the current entity.
        """

        field_name = field.name

        if not field_name.endswith("_id"):
            return None

        # ------------------------------------------------------
        # First use deterministic <entity>_id convention.
        # ------------------------------------------------------

        candidate_name = (
            field_name[:-3]
            .replace("_", " ")
            .title()
            .replace(" ", "")
        )

        candidate_entity = self._find_entity(
            blueprint,
            candidate_name,
        )

        if candidate_entity is not None:
            return candidate_entity.name

        # ------------------------------------------------------
        # Fallback to AI relationship metadata.
        # Only accept it when this entity really owns the field.
        # ------------------------------------------------------

        for relation in blueprint.relationships:

            if relation.foreign_key != field_name:
                continue

            if relation.relationship_type == "many_to_many":
                continue

            if relation.source == entity.name:

                target = self._find_entity(
                    blueprint,
                    relation.target,
                )

                if target is not None:
                    return target.name

            if relation.target == entity.name:

                source = self._find_entity(
                    blueprint,
                    relation.source,
                )

                if source is not None:
                    return source.name

        return None

    def _collect_foreign_keys(
        self,
        entity,
        blueprint,
    ):
        """
        Return:

        {
            "patient_id": "Patient",
            "doctor_id": "Doctor"
        }
        """

        foreign_keys = {}

        for field in entity.fields:

            target = self._resolve_foreign_key(
                entity,
                field,
                blueprint,
            )

            if target:
                foreign_keys[field.name] = target

        return foreign_keys

    # ==========================================================
    # Dynamic model generation
    # ==========================================================

    def generate_model(
        self,
        entity,
        blueprint,
    ):
        """
        Generate one SQLAlchemy model.
        """

        name = entity.name
        table_name = self._table_name(name)

        foreign_keys = self._collect_foreign_keys(
            entity,
            blueprint,
        )

        columns = []
        relationships_code = []

        # ------------------------------------------------------
        # Columns
        # ------------------------------------------------------

        for field in entity.fields:

            field_name = field.name

            datatype = self.SQL_TYPES.get(
                field.type.lower(),
                "String",
            )

            if field_name.lower() == "id":

                columns.append(
                    f'''    {field_name} = Column(
        {datatype},
        primary_key=True,
        index=True,
    )'''
                )

                continue

            foreign_model = foreign_keys.get(
                field_name
            )

            if foreign_model:

                target_table = self._table_name(
                    foreign_model
                )

                columns.append(
                    f'''    {field_name} = Column(
        {datatype},
        ForeignKey("{target_table}.id"),
    )'''
                )

            else:

                columns.append(
                    f'''    {field_name} = Column(
        {datatype},
    )'''
                )

        # ------------------------------------------------------
        # Relationships owned by this model
        #
        # Example:
        # Appointment.patient_id -> Patient
        #
        # generates:
        #
        # patient = relationship("Patient")
        #
        # We intentionally do NOT generate arbitrary
        # Doctor.invoice relationships.
        # ------------------------------------------------------

        used_relationship_names = set()

        for field_name, target_model in foreign_keys.items():

            relationship_name = field_name

            if relationship_name.endswith("_id"):
                relationship_name = relationship_name[:-3]

            if relationship_name in used_relationship_names:
                continue

            used_relationship_names.add(
                relationship_name
            )

            relationships_code.append(
                f'''    {relationship_name} = relationship(
        "{target_model}",
        foreign_keys=[{field_name}],
    )'''
            )

        # ------------------------------------------------------
        # Class body
        # ------------------------------------------------------

        class_parts = (
            columns
            + relationships_code
        )

        if class_parts:
            class_body = "\n\n".join(
                class_parts
            )
        else:
            class_body = "    pass"

        # ------------------------------------------------------
        # Generated model
        # ------------------------------------------------------

        model = f'''"""
{name} Model
"""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time

from sqlalchemy.orm import relationship

from app.database import Base


class {name}(Base):

    __tablename__ = "{table_name}"

{class_body}
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "models"
            / f"{name.lower()}.py",
            model,
        )

        print(
            f"✅ Generated {name} Model"
        )

    def generate(self):
        """
        Legacy pipeline compatibility.
        """

        print(
            "ℹ️ Models are generated dynamically "
            "using generate_model(entity, blueprint)"
        )