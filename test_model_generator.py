from generators.ai.model_ai_generator import AIModelGenerator

generator = AIModelGenerator(
    "outputs/Hospital_Management_System",
)

generator.generate(
    entity_name="Patient",
    fields=[
        "id : integer primary key",
        "name : string",
        "age : integer",
        "gender : string",
        "phone : string",
    ],
)