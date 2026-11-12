"""
ArchitectAI End-to-End Pipeline Test
"""

from orchestration.architect_pipeline import ArchitectPipeline


requirements = """
Build a library management backend.

The system should manage:

Member:
- id integer
- name string
- email string

Book:
- id integer
- title string
- author string
- available boolean

Borrow:
- id integer
- member_id integer
- book_id integer
- borrowed_date date
- returned boolean

A member can have many borrows.
A book can have many borrow records.
"""


pipeline = ArchitectPipeline(
    output_dir="generated_projects/Library_System",
)


result = pipeline.generate(
    requirements=requirements,
    project_name="Library Management System",
)


print("\nGenerated Entities:")

for entity in result["blueprint"].entities:
    print(f" - {entity.name}")


print("\nPublished Artifacts:")

for artifact in result["artifacts"]:
    print(
        f" - {artifact.name} "
        f"[{artifact.category}] "
        f"by {artifact.author}"
    )


print("\n🎉 END-TO-END ARCHITECTAI TEST SUCCESSFUL")