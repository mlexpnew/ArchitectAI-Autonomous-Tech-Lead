from generators.ai.project_ai_generator import AIProjectGenerator

generator = AIProjectGenerator(
    "outputs/Hospital_Management_System",
)

generator.generate_entity(
    "Patient",
    [
        "id : integer",
        "name : string",
        "age : integer",
        "gender : string",
        "phone : string",
    ],
)