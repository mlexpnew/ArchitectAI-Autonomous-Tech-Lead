from quality.quality_gate import QualityGate


code = """
print("hello")
"""

report = QualityGate().check(code)

print()

print(report.passed)

print(report.score)

print(report.issues)