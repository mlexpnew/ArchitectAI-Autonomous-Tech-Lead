"""
Project Scaffolder

Creates the initial project structure.
"""

from pathlib import Path


class ProjectScaffolder:

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def create(self):

        folders = [
            "backend",
            "backend/app",
            "backend/app/api",
            "backend/app/core",
            "backend/app/models",
            "backend/app/services",
            "backend/app/utils",
            "frontend",
            "frontend/src",
            "frontend/src/components",
            "frontend/src/pages",
            "frontend/src/services",
            "frontend/src/hooks",
            "database",
            "docs",
            "docker",
            "tests",
        ]

        for folder in folders:
            (self.output_dir / folder).mkdir(
                parents=True,
                exist_ok=True,
            )

        starter_files = [
            "README.md",
            ".gitignore",
            ".env.example",
            "docker/Dockerfile",
            "docker/docker-compose.yml",
            "backend/requirements.txt",
            "frontend/package.json",
            "database/schema.sql",
        ]

        for file in starter_files:
            path = self.output_dir / file
            path.parent.mkdir(parents=True, exist_ok=True)

            if not path.exists():
                path.touch()

        return self.output_dir