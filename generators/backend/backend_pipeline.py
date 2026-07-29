"""
Backend Generation Pipeline

Coordinates AI requirement extraction and generates
a complete FastAPI backend from the resulting blueprint.
"""

from pathlib import Path
import shutil

from generators.model_generator import ModelGenerator
from generators.schema_generator import SchemaGenerator
from generators.repository_generator import RepositoryGenerator
from generators.service_generator import ServiceGenerator
from generators.api_generator import APIGenerator
from generators.database_generator import DatabaseGenerator
from generators.init_generator import InitGenerator
from generators.infrastructure_generator import InfrastructureGenerator
from generators.main_generator import MainGenerator
from generators.router_generator import RouterGenerator
from generators.model_registry_generator import ModelRegistryGenerator
from generators.test_generator import TestGenerator
from generators.requirements_generator import RequirementsGenerator
from generators.config_generator import ConfigGenerator

from generators.ai.entity_extractor import AIEntityExtractor
from generators.ai.relationship_extractor import RelationshipExtractor

from generators.entities.project_blueprint import ProjectBlueprint


class BackendPipeline:
    """
    Generates FastAPI backend projects.

    Supports:
    1. Legacy hardcoded generation
    2. AI-driven dynamic generation from requirements
    """

    def __init__(
        self,
        output_dir: str,
    ):
        # ---------------------------------------------------------
        # Normalise output directory
        # ---------------------------------------------------------

        self.output_dir = Path(output_dir)

        # Most existing generators accept either str or Path.
        # Keep one consistent value for all generators.
        generator_output_dir = str(
            self.output_dir
        )

        # ---------------------------------------------------------
        # AI Extractors
        # ---------------------------------------------------------

        self.extractor = AIEntityExtractor()

        self.relationship_extractor = (
            RelationshipExtractor()
        )

        # ---------------------------------------------------------
        # Code Generators
        # ---------------------------------------------------------

        self.model = ModelGenerator(
            generator_output_dir
        )

        self.schema = SchemaGenerator(
            generator_output_dir
        )

        self.repository = RepositoryGenerator(
            generator_output_dir
        )

        self.service = ServiceGenerator(
            generator_output_dir
        )

        self.api = APIGenerator(
            generator_output_dir
        )

        self.database = DatabaseGenerator(
            generator_output_dir
        )

        self.init = InitGenerator(
            generator_output_dir
        )

        self.infrastructure = InfrastructureGenerator(
            generator_output_dir
        )

        self.main = MainGenerator(
            generator_output_dir
        )

        self.router = RouterGenerator(
            generator_output_dir
        )

        self.model_registry = ModelRegistryGenerator(
            generator_output_dir
        )

        self.test_generator = TestGenerator(
            generator_output_dir
        )

        self.requirements_generator = (
            RequirementsGenerator(
                generator_output_dir
            )
        )

        self.config_generator = ConfigGenerator(
            generator_output_dir
        )

        self.blueprint = None

    # ---------------------------------------------------------
    # Legacy Backend Generator
    # ---------------------------------------------------------

    def generate(self):
        """
        Execute the original hardcoded backend generator.
        """

        self.model.generate()

        self.schema.generate()

        self.repository.generate()

        self.service.generate()

        self.api.generate()

        self.init.generate()

        self.database.generate()

        self.infrastructure.generate()

        self.main.generate()

    # ---------------------------------------------------------
    # Clean Previous Generated Backend
    # ---------------------------------------------------------

    def _prepare_backend_directory(self):
        """
        Remove stale generated backend files before creating
        a new project.

        This prevents old models, APIs and tests from leaking
        into a newly generated application.
        """

        backend_dir = (
            self.output_dir
            / "backend"
        )

        if backend_dir.exists():

            print(
                "\n🧹 Cleaning previous generated backend..."
            )

            shutil.rmtree(
                backend_dir
            )

        backend_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        print(
            "✅ Clean generation workspace ready"
        )

        return backend_dir

    # ---------------------------------------------------------
    # AI-Driven Backend Generator
    # ---------------------------------------------------------

    def generate_from_requirements(
        self,
        requirements: str,
    ):
        """
        Generate a complete backend from natural-language
        requirements.
        """

        if not requirements:
            raise ValueError(
                "Requirements cannot be empty."
            )

        if not requirements.strip():
            raise ValueError(
                "Requirements cannot be empty."
            )

        # ---------------------------------------------------------
        # Step 1: Clean stale generated backend
        # ---------------------------------------------------------

        self._prepare_backend_directory()

        # ---------------------------------------------------------
        # Step 2: Extract entities
        # ---------------------------------------------------------

        print(
            "\n=============================="
        )

        print(
            "Extracting Entities..."
        )

        print(
            "==============================\n"
        )

        entities = self.extractor.extract(
            requirements
        )

        if not entities:
            raise RuntimeError(
                "AI entity extraction returned no entities."
            )

        # ---------------------------------------------------------
        # Step 3: Extract relationships
        # ---------------------------------------------------------

        relationships = (
            self.relationship_extractor.extract(
                requirements
            )
        )

        if relationships is None:
            relationships = []

        # ---------------------------------------------------------
        # Step 4: Build blueprint
        # ---------------------------------------------------------

        blueprint = ProjectBlueprint(
            name="Generated Project",
            entities=entities,
            relationships=relationships,
        )

        self.blueprint = blueprint

        print(
            f"✅ Extracted {len(blueprint.entities)} entities"
        )

        print(
            f"✅ Extracted "
            f"{len(blueprint.relationships)} relationships"
        )

        # ---------------------------------------------------------
        # Step 5: Generate entity-specific backend files
        # ---------------------------------------------------------

        print(
            "\n=============================="
        )

        print(
            "Generating Dynamic Backend..."
        )

        print(
            "==============================\n"
        )

        for entity in blueprint.entities:

            print(
                f"\n{'=' * 60}"
            )

            print(
                f"🚀 Generating Backend for "
                f"{entity.name}"
            )

            print(
                f"{'=' * 60}"
            )

            self.model.generate_model(
                entity,
                blueprint,
            )

            self.schema.generate_schema(
                entity
            )

            self.repository.generate_repository(
                entity
            )

            self.service.generate_service(
                entity
            )

            self.api.generate_api(
                entity
            )

        # ---------------------------------------------------------
        # Step 6: Generate shared project files
        #
        # IMPORTANT:
        # These must run exactly once.
        # ---------------------------------------------------------

        print(
            "\n============================================================"
        )

        print(
            "⚙️ Generating Shared Backend Infrastructure"
        )

        print(
            "============================================================"
        )

        self.database.generate()

        self.init.generate()

        self.infrastructure.generate()

        self.model_registry.generate(
            blueprint.entities
        )

        self.router.generate(
            blueprint.entities
        )

        # ---------------------------------------------------------
        # Step 7: Generate tests
        # ---------------------------------------------------------

        self.test_generator.generate(
            blueprint.entities
        )

        # ---------------------------------------------------------
        # Step 8: Generate requirements/config
        # ---------------------------------------------------------

        self.requirements_generator.generate()

        self.config_generator.generate()

        # ---------------------------------------------------------
        # Complete
        # ---------------------------------------------------------

        print(
            "\n✅ Dynamic Backend Generation Completed\n"
        )

        return blueprint