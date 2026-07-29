"""
File Manager

Creates a workspace for every project and stores all AI-generated
artifacts in an organized directory structure.
"""

from pathlib import Path
import re


class FileManager:

    def __init__(self, base_output="outputs"):

        self.base_output = Path(base_output)
        self.base_output.mkdir(exist_ok=True)

    def _clean_project_name(self, project_name: str):

        project_name = project_name.strip()

        project_name = re.sub(r"\s+", "_", project_name)

        project_name = re.sub(
            r"[^a-zA-Z0-9_-]",
            "",
            project_name,
        )

        return project_name

    def create_project_workspace(self, project_name: str):

        project_name = self._clean_project_name(project_name)

        project_dir = self.base_output / project_name

        project_dir.mkdir(parents=True, exist_ok=True)

        (project_dir / "diagrams").mkdir(exist_ok=True)

        return project_dir

    def save_document(
        self,
        project_name: str,
        filename: str,
        content: str,
    ):

        project_dir = self.create_project_workspace(project_name)

        filepath = project_dir / filename

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        return filepath

    def read_document(
        self,
        project_name: str,
        filename: str,
    ):

        project_dir = self.create_project_workspace(project_name)

        filepath = project_dir / filename

        if not filepath.exists():
            return ""

        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()