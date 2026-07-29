from generators.ai.code_generator import AICodeGenerator

generator = AICodeGenerator()

prompt = """
Generate a SQLAlchemy model for a Hospital Patient.

Fields:

id
name
age
phone
gender
"""

print(generator.generate(prompt))