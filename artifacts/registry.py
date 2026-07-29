class ArtifactRegistry:

    def __init__(self):

        self.artifacts = {}

    def register(self, artifact):

        self.artifacts[artifact.name] = artifact

    def get(self, name):

        return self.artifacts.get(name)

    def all(self):

        return list(self.artifacts.values())

    def exists(self, name):

        return name in self.artifacts