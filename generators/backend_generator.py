"""
Backend Generator

Generates a production-ready FastAPI backend skeleton.
"""

from pathlib import Path


from generators.writer import FileWriter

from generators.templates import (
    main_template,
    requirements_template,
    config_template,
    database_template,
    env_template,
    health_api_template,
    patients_api_template,
    doctors_api_template,
    appointments_api_template,
)


from generators.auth_templates import (
    password_template,
    jwt_template,
)

class BackendGenerator:

    def __init__(
        self,
        output_dir: str,
        project_name: str,
    ):
        self.output_dir = Path(output_dir)
        self.project_name = project_name

    def generate(self):

        backend = self.output_dir / "backend"

        print("\n🚀 Generating Backend Project...\n")

        # =====================================================
        # Core Files
        # =====================================================

        FileWriter.write(
            backend / "app" / "main.py",
            main_template(self.project_name),
        )

        FileWriter.write(
            backend / "app" / "config.py",
            config_template(),
        )

        FileWriter.write(
            backend / "app" / "database.py",
            database_template(),
        )

        FileWriter.write(
            backend / ".env.example",
            env_template(),
        )

        FileWriter.write(
            backend / "requirements.txt",
            requirements_template(),
        )
        
        FileWriter.write(
            backend / "app" / "auth" / "password.py",
            password_template(),
        )

        FileWriter.write(
            backend / "app" / "auth" / "jwt_handler.py",
            jwt_template(),
        )

        FileWriter.write(
            backend / "app" / "auth" / "__init__.py",
         "",
        )
        
        # Patient Module

    

        # =====================================================
        # Python Packages
        # =====================================================

        packages: list[str] = [
            "api",
            "models",
            "schemas",
            "services",
            "utils",
            "repositories",
            "auth",
        ]

        for package in packages:

            FileWriter.write(
                backend / "app" / package / "__init__.py",
                "",
            )

        # =====================================================
        # API Routes
        # =====================================================

        FileWriter.write(
            backend / "app" / "api" / "health.py",
            health_api_template(),
        )

        FileWriter.write(
            backend / "app" / "api" / "patients.py",
            patients_api_template(),
        )

        FileWriter.write(
            backend / "app" / "api" / "doctors.py",
            doctors_api_template(),
        )

        FileWriter.write(
            backend / "app" / "api" / "appointments.py",
            appointments_api_template(),
        )

    

        print("\n" + "=" * 60)
        print("✅ Backend Generated Successfully")
        print("=" * 60)

        print(f"\nProject Location: {backend}")

        print("\nGenerated Files:")

        generated_files = [
            "app/main.py",
            "app/config.py",
            "app/database.py",
            "app/api/health.py",
            "app/api/patients.py",
            "app/api/doctors.py",
            "app/api/appointments.py",
            "requirements.txt",
            ".env.example",
        ]

        for file in generated_files:
            print(f"   ✔ {file}")

        print()