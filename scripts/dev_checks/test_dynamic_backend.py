from generators.backend.backend_pipeline import BackendPipeline

pipeline = BackendPipeline(
    "generated_projects/Dynamic_System"
)

pipeline.generate_from_requirements(
    """
Build a Hospital Management System.

Patients

Doctors

Appointments

Medicines

Invoices
"""
)