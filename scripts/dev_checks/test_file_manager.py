from codebase.file_manager import FileManager


manager = FileManager()

manager.write(

    project="Hospital_Management_System",

    relative_path="services/patient_service.py",

    content="print('Hello')",

)

print(

    manager.read(

        "Hospital_Management_System",

        "services/patient_service.py",

    )

)