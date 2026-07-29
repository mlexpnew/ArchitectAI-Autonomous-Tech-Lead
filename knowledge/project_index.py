"""
Project Index
"""

from pathlib import Path

from knowledge.document import ProjectDocument


class ProjectIndex:

    def __init__(self):

        self.documents = []

    def index_project(
        self,
        root: str,
    ):

        root = Path(root)

        for file in root.rglob("*.py"):

            try:

                self.documents.append(

                    ProjectDocument(

                        path=str(file),

                        content=file.read_text(
                            encoding="utf-8"
                        ),

                    )

                )

            except Exception:

                pass

    def search(
        self,
        keyword: str,
    ):

        keyword = keyword.lower()

        results = []

        for doc in self.documents:

            if keyword in doc.content.lower():

                results.append(doc)

        return results