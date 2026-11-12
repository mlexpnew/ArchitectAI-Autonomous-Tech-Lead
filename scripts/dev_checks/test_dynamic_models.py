from generators.backend.backend_pipeline import BackendPipeline

pipeline = BackendPipeline(
    "generated_projects/Dynamic_Project"
)

pipeline.generate_from_requirements(
    """
Build a Library Management System.

Books

Authors

Members

Loans
"""
)