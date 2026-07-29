"""
File Manager
"""

from pathlib import Path


class FileManager:

    def __init__(self, root="generated_projects"):

        self.root = Path(root)

        self.root.mkdir(exist_ok=True)

    def write(

        self,

        project,

        relative_path,

        content,

    ):

        file_path = self.root / project / relative_path

        file_path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        file_path.write_text(

            content,

            encoding="utf-8",

        )

        return file_path

    def read(

        self,

        project,

        relative_path,

    ):

        file_path = self.root / project / relative_path

        return file_path.read_text(

            encoding="utf-8",

        )

    def exists(

        self,

        project,

        relative_path,

    ):

        return (

            self.root / project / relative_path

        ).exists()