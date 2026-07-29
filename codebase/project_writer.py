"""
Project Writer
"""

from codebase.file_manager import FileManager


class ProjectWriter:

    def __init__(self):

        self.files = FileManager()

    def publish(

        self,

        project,

        artifact,

    ):

        return self.files.write(

            project=project,

            relative_path=f"{artifact.category}/{artifact.name}",

            content=artifact.content,

        )