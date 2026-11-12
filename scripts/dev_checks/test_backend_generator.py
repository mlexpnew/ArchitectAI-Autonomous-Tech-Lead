from generators.backend.backend_generator import BackendGenerator


generator = BackendGenerator()

code = generator.generate_service("Patient")

print(code)