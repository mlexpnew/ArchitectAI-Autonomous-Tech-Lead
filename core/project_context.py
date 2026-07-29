"""
Project Context Builder

Provides context for AI generation.
"""

from pathlib import Path


class ProjectContext:

    def __init__(
        self,
        project_root: str,
    ):

        self.project_root = Path(project_root)

    def build(self):

        """
        Returns the entire project context.
        (Useful for debugging only.)
        """

        context = []

        backend = self.project_root / "backend"

        if not backend.exists():
            return ""

        for file in backend.rglob("*.py"):

            try:

                context.append(
                    f"\n### {file.relative_to(self.project_root)}\n"
                )

                context.append(
                    file.read_text(
                        encoding="utf-8"
                    )[:1000]
                )

            except Exception:
                pass

        return "\n".join(context)

    def build_for_entity(
        self,
        entity_name: str,
    ):

        """
        Returns ONLY files related to one entity.

        This keeps AI prompts small and avoids
        Groq token-limit errors.
        """

        entity = entity_name.lower()

        context = []

        files = [

            self.project_root
            / "backend"
            / "app"
            / "models"
            / f"{entity}.py",

            self.project_root
            / "backend"
            / "app"
            / "schemas"
            / f"{entity}.py",

            self.project_root
            / "backend"
            / "app"
            / "repositories"
            / f"{entity}_repository.py",

            self.project_root
            / "backend"
            / "app"
            / "services"
            / f"{entity}_service.py",

            self.project_root
            / "backend"
            / "app"
            / "api"
            / f"{entity}s.py",
        ]

        for file in files:

            if file.exists():

                try:

                    context.append(
                        f"\n### {file.name}\n"
                    )

                    # Limit each file to avoid huge prompts
                    context.append(
                        file.read_text(
                            encoding="utf-8"
                        )[:1000]
                    )

                except Exception:
                    pass

        return "\n".join(context)