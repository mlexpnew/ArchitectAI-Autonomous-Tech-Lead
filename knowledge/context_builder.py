"""
Context Builder
"""

from knowledge.project_index import ProjectIndex


class ContextBuilder:

    def __init__(self):

        self.index = ProjectIndex()

    def build(
        self,
        project_dir: str,
        keyword: str,
    ):

        self.index.index_project(
            project_dir,
        )

        docs = self.index.search(
            keyword,
        )

        context = []

        for doc in docs:

            context.append(

                f"""
FILE:
{doc.path}

{doc.content[:2000]}
"""

            )

        return "\n".join(context)