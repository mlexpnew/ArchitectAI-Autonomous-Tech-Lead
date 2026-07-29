class VersionManager:

    def __init__(self):

        self.versions = {}

    def next(self, artifact_name):

        version = self.versions.get(artifact_name, 0) + 1

        self.versions[artifact_name] = version

        return version