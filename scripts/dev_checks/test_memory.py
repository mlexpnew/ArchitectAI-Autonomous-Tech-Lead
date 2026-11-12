from memory.memory_manager import MemoryManager

memory = MemoryManager(
    "outputs/Hospital_Management_System",
)

memory.add_entity(

    "Patient",

    [

        "id",

        "name",

        "age",

        "phone",

    ],

)

memory.plugin_completed("model")

memory.plugin_completed("schema")

memory.file_generated(

    "backend/app/models/patient.py",

)

print(memory.memory)