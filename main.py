import sys

from crews.engineering_crew import EngineeringCrew
from utils.project_scaffolder import ProjectScaffolder
from generators.backend_generator import BackendGenerator
from generators.model_generator import ModelGenerator
from generators.schema_generator import SchemaGenerator
from generators.repository_generator import RepositoryGenerator
from generators.service_generator import ServiceGenerator
from generators.api_generator import APIGenerator
from generators.master_generator import MasterGenerator
from orchestrator import ArchitectAI
from builder.project_builder import AIProjectBuilder
from autonomous.tech_lead import AutonomousTechLead

def main():

    project_name = "Hospital_Management_System"

    project_idea = """
Build an AI-powered Hospital Management System.

The system should allow patients to book appointments,
consult doctors online, manage prescriptions,
make payments, and allow hospital staff to manage
patients, doctors, billing, reports and inventory.
"""

    if len(sys.argv) != 2:
        print("\nUsage:")
        print("python3 main.py requirement")
        print("python3 main.py architecture")
        print("python3 main.py backend")
        print("python3 main.py database")
        print("python3 main.py frontend")
        print("python3 main.py generate-backend")
        print("python3 main.py generate-models")
        print("python3 main.py generate-schemas")
        print("python3 main.py generate-repositories")
        print("python3 main.py generate-services")
        print("python3 main.py generate-api")
        print("python3 main.py generate-project")
        print("python3 main.py ai")
        print("python3 main.py build")
        print("python3 main.py autonomous")
        return

    stage = sys.argv[1].lower()

    # -----------------------------
    # Generate Project Structure
    # -----------------------------
    if stage == "scaffold":

        scaffolder = ProjectScaffolder(
            output_dir=f"outputs/{project_name}"
        )

        scaffolder.create()

        print("\n✅ Project folder structure created successfully.")
        return
    
    elif stage == "generate-models":

        generator = ModelGenerator(
            output_dir=f"outputs/{project_name}",
        )

        generator.generate()

        return
    elif stage == "generate-schemas":

        generator = SchemaGenerator(
            output_dir=f"outputs/{project_name}",
        )

        generator.generate()

        return
    elif stage == "generate-repositories":

        generator = RepositoryGenerator(
            output_dir=f"outputs/{project_name}",
        )

        generator.generate()

        return
    
    elif stage == "generate-services":

        generator = ServiceGenerator(
            output_dir=f"outputs/{project_name}",
        )

        generator.generate()

        return
    elif stage == "generate-api":

        generator = APIGenerator(
            output_dir=f"outputs/{project_name}",
        )

        generator.generate()

        return
    elif stage == "generate-project":

        generator = MasterGenerator(
            output_dir=f"outputs/{project_name}",
            project_name=project_name,
        )

        generator.generate()

        return
    elif stage == "ai":

        ai = ArchitectAI()

        ai.build(project_idea)

        return
    elif stage == "build":

        builder = AIProjectBuilder(
            f"outputs/{project_name}",
        )

        builder.build(project_idea)

        return
    
    elif stage == "autonomous":

        AutonomousTechLead(
            f"outputs/{project_name}",
        ).build(
            project_idea,
        )

        return



    # -----------------------------
    # Run Engineering Agent
    # -----------------------------
    crew = EngineeringCrew(
        project_name=project_name,
        project_idea=project_idea,
    )

    if stage == "generate-backend":

        generator = BackendGenerator(
            output_dir=f"outputs/{project_name}",
            project_name=project_name,
        )

        generator.generate()

        return

    crew.run(stage)


if __name__ == "__main__":
    main()