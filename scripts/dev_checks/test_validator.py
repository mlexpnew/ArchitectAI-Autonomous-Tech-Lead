from validation.python_validator import PythonValidator

good_code = """
def hello():
    print("Hello")
"""

bad_code = """
def hello(
"""

print(PythonValidator.validate(good_code))

print(PythonValidator.validate(bad_code))