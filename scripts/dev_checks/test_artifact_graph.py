from graph.artifact_graph import ArtifactGraph
from graph.dependency_node import DependencyNode


graph = ArtifactGraph(
    "outputs/Hospital_Management_System",
)

graph.add_node(

    DependencyNode(

        "PatientModel",

        "model",

        "backend/app/models/patient.py",

    )

)

graph.add_node(

    DependencyNode(

        "PatientSchema",

        "schema",

        "backend/app/schemas/patient.py",

    )

)

graph.add_node(

    DependencyNode(

        "PatientRepository",

        "repository",

        "backend/app/repositories/patient_repository.py",

    )

)

graph.add_dependency(

    "PatientModel",

    "PatientSchema",

)

graph.add_dependency(

    "PatientSchema",

    "PatientRepository",

)

print()

print(graph.affected("PatientModel"))