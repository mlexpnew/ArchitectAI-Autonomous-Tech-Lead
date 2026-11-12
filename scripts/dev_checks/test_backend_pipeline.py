from generators.backend.backend_pipeline import BackendPipeline


pipeline = BackendPipeline(
    "generated_projects/Hospital_Management_System"
)

pipeline.generate_from_requirements(
    """
Build a Hospital Management System.

Patients book appointments.

Doctors manage appointments.

Receptionists handle billing.

Admin manages users.
"""
)