"""
Artifact Manager

Responsible for saving AI generated files.
"""

from pathlib import Path


class ArtifactManager:

    def __init__(self, project_root: str):

        self.project_root = Path(project_root)

    def save(
        self,
        relative_path: str,
        content: str,
    ):

        file_path = self.project_root / relative_path

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        print(f"✅ {relative_path}")

    def read(
        self,
        relative_path: str,
    ):

        file_path = self.project_root / relative_path

        if not file_path.exists():
            return ""

        return file_path.read_text(
            encoding="utf-8",
        )