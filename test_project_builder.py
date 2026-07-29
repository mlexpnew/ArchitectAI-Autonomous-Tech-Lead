from builder.project_builder import AIProjectBuilder

requirements = """
Build an AI Hospital Management System.

Patients

Doctors

Appointments

Billing

Inventory

Payments

Authentication

Admin Dashboard
"""

builder = AIProjectBuilder(
    "outputs/Hospital_Management_System",
)

builder.build(requirements)