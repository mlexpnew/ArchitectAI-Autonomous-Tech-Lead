from generators.ai.relationship_extractor import RelationshipExtractor

extractor = RelationshipExtractor()

relationships = extractor.extract(
    """
Hospital Management System

Patients

Doctors

Appointments

Medicines

Invoices
"""
)

for relationship in relationships:
    print(relationship)