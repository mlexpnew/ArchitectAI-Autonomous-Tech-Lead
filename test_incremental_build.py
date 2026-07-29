from graph.change_detector import ChangeDetector

detector = ChangeDetector(
    "outputs/Hospital_Management_System",
)

print()

print("=" * 60)

print("Affected Files")

print("=" * 60)

for node in detector.affected_nodes(
    "PatientModel",
):

    print(node)