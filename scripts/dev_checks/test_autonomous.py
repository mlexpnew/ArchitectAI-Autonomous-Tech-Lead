from autonomous.tech_lead import AutonomousTechLead


requirements = """
Build an AI Hospital Management System.

Entities

Patient
Doctor
Appointment
Prescription
Payment
Inventory

Authentication

Admin Dashboard

Email Notifications

Reports
"""


AutonomousTechLead(
    "outputs/Hospital_Management_System",
).build(
    requirements,
)