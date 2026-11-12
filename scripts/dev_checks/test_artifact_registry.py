from artifacts.artifact_manager import ArtifactManager


manager = ArtifactManager()

manager.save(

    name="patient_service.py",

    category="services",

    author="backend",

    content="FastAPI CRUD Service",

)

manager.save(

    name="patient_repository.py",

    category="repository",

    author="backend",

    content="SQLAlchemy Repository",

)

for artifact in manager.list():

    print()

    print("Name :", artifact.name)

    print("Version :", artifact.version)

    print("Author :", artifact.author)

    print("Category :", artifact.category)

    print("Content :", artifact.content)