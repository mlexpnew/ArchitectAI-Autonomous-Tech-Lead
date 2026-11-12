from graph.change_detector import ChangeDetector

detector = ChangeDetector(
    "outputs/Hospital_Management_System",
)

detector.register(

    "PatientModel",

    "outputs/Hospital_Management_System/backend/app/models/patient.py",

)

print(

    detector.changed(
        "PatientModel",
    )

)

print(

    detector.affected_nodes(
        "PatientModel",
    )

)