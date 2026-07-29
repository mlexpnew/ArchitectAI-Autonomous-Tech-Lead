"""
File Writer Utility

Handles writing generated files safely.
"""

from pathlib import Path


class FileWriter:

    @staticmethod
    def write(path: str, content: str):

        file_path = Path(path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        print(f"✅ Created {file_path}")