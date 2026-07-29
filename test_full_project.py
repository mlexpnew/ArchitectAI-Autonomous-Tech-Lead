from generators.ai.project_ai_generator import AIProjectGenerator

requirements = """
Build an AI Hospital Management System.

Patients can book appointments.

Doctors manage schedules.

Admin manages inventory.

Billing system.

Medicine management.
"""

generator = AIProjectGenerator(
    "outputs/Hospital_Management_System",
)

generator.generate(requirements)