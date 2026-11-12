from generators.ai.schema_ai_generator import AISchemaGenerator

generator = AISchemaGenerator(
    "outputs/Hospital_Management_System",
)

generator.generate(
    entity_name="Patient",
    fields=[
        "id : integer",
        "name : string",
        "age : integer",
        "gender : string",
        "phone : string",
    ],
)