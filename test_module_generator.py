from generators.ai.module_ai_generator import AIModuleGenerator

print("🚀 Starting Module Generator...")

generator = AIModuleGenerator(
    "outputs/Hospital_Management_System",
)

generator.generate(
    "Patient",
    [
        "id : integer",
        "name : string",
        "age : integer",
        "phone : string",
    ],
)

print("✅ Done")