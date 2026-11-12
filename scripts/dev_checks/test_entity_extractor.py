from generators.ai.entity_extractor import AIEntityExtractor

extractor = AIEntityExtractor()

requirements = """
Build an AI Hospital Management System.

Patients can book appointments.

Doctors can manage schedules.

Admin can manage medicines.

Billing should support payments.

Inventory should track medicine stock.
"""

entities = extractor.extract(requirements)

print(entities)