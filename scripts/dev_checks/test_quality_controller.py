from quality.quality_controller import QualityController

code = """
def add(a,b):
 return a+b
"""

result = QualityController().improve(code)

print()

print(result)