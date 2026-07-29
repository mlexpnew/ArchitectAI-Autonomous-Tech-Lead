"""
Schema Generator

Generates production-ready Pydantic schemas dynamically.
"""

from pathlib import Path

from generators.writer import FileWriter


class SchemaGenerator:

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)

    def generate_schema(
        self,
        entity,
    ):
        """
        Generate Create, Update and Response schemas
        dynamically for an entity.
        """

        name = entity.name
        lower = name.lower()

        python_types = {
            "integer": "int",
            "string": "str",
            "float": "float",
            "boolean": "bool",
            "date": "DateType",
            "time": "TimeType",
        }

        # --------------------------------------------------
        # Detect datetime requirements
        # --------------------------------------------------

        needs_date = any(
            field.type.lower() == "date"
            for field in entity.fields
        )

        needs_time = any(
            field.type.lower() == "time"
            for field in entity.fields
        )

        datetime_imports = []

        if needs_date:
            datetime_imports.append(
                "date as DateType"
            )

        if needs_time:
            datetime_imports.append(
                "time as TimeType"
            )

        datetime_import = ""

        if datetime_imports:
            datetime_import = (
                "from datetime import "
                + ", ".join(datetime_imports)
                + "\n\n"
            )

        # --------------------------------------------------
        # Generate fields
        # --------------------------------------------------

        base_fields = []
        update_fields = []

        for field in entity.fields:

            # ID is database generated
            if field.name.lower() == "id":
                continue

            datatype = python_types.get(
                field.type.lower(),
                "str",
            )

            base_fields.append(
                f"    {field.name}: {datatype}"
            )

            update_fields.append(
                f"    {field.name}: {datatype} | None = None"
            )

        base_body = (
            "\n".join(base_fields)
            if base_fields
            else "    pass"
        )

        update_body = (
            "\n".join(update_fields)
            if update_fields
            else "    pass"
        )

        # --------------------------------------------------
        # Generate schema file
        # --------------------------------------------------

        schema = f'''"""
{name} Schemas
"""

{datetime_import}from pydantic import BaseModel
from pydantic import ConfigDict


class {name}Base(BaseModel):
{base_body}


class {name}Create({name}Base):
    pass


class {name}Update(BaseModel):
{update_body}


class {name}Response({name}Base):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "schemas"
            / f"{lower}.py",
            schema,
        )

        print(
            f"✅ Generated {name} Schema"
        )

    def generate(self):
        """
        Legacy pipeline compatibility.
        """

        print(
            "ℹ️ Schemas are generated dynamically "
            "using generate_schema(entity)"
        )