import subprocess
import json
import time

DOMAINS = [
    ("Hospital Management System", "hospital_requirements.txt", "Hospital_System"),
    ("E-Commerce Management System", "ecommerce_requirements.txt", "ECommerce_System"),
    ("Banking Management System", "banking_requirements.txt", "Banking_System"),
    ("Library Management System", "library_requirements.txt", "Library_System"),
    ("School Management System", "school_requirements.txt", "School_System"),
    ("Inventory Management System", "inventory_requirements.txt", "Inventory_System"),
    ("CRM Management System", "crm_requirements.txt", "CRM_System"),
    ("Hotel Management System", "hotel_requirements.txt", "Hotel_System"),
]

results = []

for name, req, output in DOMAINS:

    print("=" * 80)
    print(name)
    print("=" * 80)

    start = time.time()

    process = subprocess.run(
        [
            "python3",
            "architectai.py",
            "generate",
            "--name",
            name,
            "--requirements",
            f"examples/{req}",
            "--output",
            f"generated_projects/{output}",
        ]
    )

    elapsed = round(time.time() - start, 2)

    results.append(
        {
            "project": name,
            "success": process.returncode == 0,
            "time_seconds": elapsed,
        }
    )

with open(
    "benchmark/acceptance_report.json",
    "w",
) as f:
    json.dump(results, f, indent=4)

print("\nAcceptance testing completed.")