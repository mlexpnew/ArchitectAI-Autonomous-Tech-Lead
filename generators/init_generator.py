"""
Init Generator
"""

from pathlib import Path

from generators.writer import FileWriter


class InitGenerator:

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)

    def generate(self):

        folders = [
            "backend/app",
            "backend/app/models",
            "backend/app/schemas",
            "backend/app/repositories",
            "backend/app/services",
            "backend/app/api",
        ]

        for folder in folders:

            FileWriter.write(
                self.output_dir
                / folder
                / "__init__.py",
                "",
            )

        print("✅ Generated __init__.py files")
        