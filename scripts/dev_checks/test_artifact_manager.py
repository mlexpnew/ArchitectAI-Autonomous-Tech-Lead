from core.artifact_manager import ArtifactManager

artifact = ArtifactManager(
    "outputs/Hospital_Management_System",
)

artifact.save(
    "backend/app/demo.py",
    "print('ArchitectAI Working')",
)

print(
    artifact.read(
        "backend/app/demo.py",
    )
)