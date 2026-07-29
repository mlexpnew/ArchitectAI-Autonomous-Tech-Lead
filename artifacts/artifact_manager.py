from artifacts.registry import ArtifactRegistry
from artifacts.version import VersionManager
from artifacts.artifact import Artifact


class ArtifactManager:

    def __init__(self):

        self.registry = ArtifactRegistry()

        self.version_manager = VersionManager()

    def save(

        self,

        name,

        category,

        author,

        content,

    ):

        artifact = Artifact(

            name=name,

            category=category,

            author=author,

            content=content,

            version=self.version_manager.next(name),

        )

        self.registry.register(artifact)

        return artifact

    def load(

        self,

        name,

    ):

        return self.registry.get(name)

    def list(self):

        return self.registry.all()