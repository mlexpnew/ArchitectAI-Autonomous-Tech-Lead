"""
Shared Workspace V2
"""

from sys import path

from artifacts.artifact_manager import ArtifactManager
from codebase.project_writer import ProjectWriter
from collaboration import artifact


class SharedWorkspace:

    def __init__(self):

        path = self.writer.publish(

            "Hospital_Management_System",

            artifact,

        )

        print(f"Saved -> {path}")

        return artifact

    def publish(

        self,

        name,

        category,

        author,

        content,

    ):

        artifact = self.artifacts.save(

            name=name,

            category=category,

            author=author,

            content=content,

        )

        print()

        print("📦 Published Artifact")

        print("Name :", artifact.name)

        print("Version :", artifact.version)

        print()

        return artifact

    def get(self, name):

        return self.artifacts.load(name)

    def list(self):

        return self.artifacts.list()