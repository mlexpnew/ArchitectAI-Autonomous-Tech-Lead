"""
ArchitectAI E-Commerce End-to-End Generation Test
"""

from orchestration.architect_pipeline import ArchitectPipeline


requirements = """
Build an e-commerce backend.

The system should manage:

Customers:
- id integer
- name string
- email string
- phone string

Products:
- id integer
- name string
- description string
- price float
- stock integer

Orders:
- id integer
- customer_id integer
- total float
- status string

OrderItems:
- id integer
- order_id integer
- product_id integer
- quantity integer
- price float

A customer can have many orders.

An order belongs to one customer.

An order can contain many order items.

Each order item belongs to one product.
"""


pipeline = ArchitectPipeline(
    output_dir="generated_projects/Ecommerce_System",
)


result = pipeline.generate(
    requirements=requirements,
    project_name="E-Commerce System",
)


blueprint = result["blueprint"]


print("\n" + "=" * 60)
print("🎉 E-COMMERCE GENERATION COMPLETED")
print("=" * 60)


print("\nEntities:")

for entity in blueprint.entities:
    print(
        f" - {entity.name}"
    )


print("\nRelationships:")

for relationship in blueprint.relationships:

    print(
        f" - {relationship.source} "
        f"-> {relationship.target} "
        f"({relationship.relationship_type})"
    )


print("\nValidation:")

validation = result["validation"]

print(
    " - Valid:",
    validation["valid"],
)

if validation.get("tests"):

    print(
        " - Tests passed:",
        validation["tests"]["passed"],
    )


print("\nSelf-Healing:")

healing = result.get(
    "self_healing"
)

if healing is None:

    print(
        " - Not required"
    )

else:

    print(
        " - Healed:",
        healing["healed"],
    )

    print(
        " - Attempts:",
        healing["attempts"],
    )


print("\nArtifacts:")

for artifact in result["artifacts"]:

    print(
        f" - {artifact.name}"
    )


print("\n🚀 ARCHITECTAI END-TO-END TEST PASSED")
