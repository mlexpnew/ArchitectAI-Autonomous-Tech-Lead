from pathlib import Path

from generators.writer import FileWriter


class ModelRegistryGenerator:

    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)

    def generate(self, entities):

        imports = []
        all_models = []

        for entity in entities:
            name = entity.name
            module = entity.name.lower()

            imports.append(
                f"from .{module} import {name}"
            )

            all_models.append(name)

        code = "\n".join(imports)

        code += "\n\n"

        code += "__all__ = [\n"

        for model in all_models:
            code += f'    "{model}",\n'

        code += "]\n"

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "models"
            / "__init__.py",
            code,
        )

        print("✅ Generated Model Registry")