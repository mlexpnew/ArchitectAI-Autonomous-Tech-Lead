"""
Master Generator

Runs all generators in sequence.
"""

from generators.backend_generator import BackendGenerator
from generators.model_generator import ModelGenerator
from generators.schema_generator import SchemaGenerator
from generators.repository_generator import RepositoryGenerator
from generators.service_generator import ServiceGenerator
from generators.api_generator import APIGenerator


class MasterGenerator:

    def __init__(
        self,
        output_dir: str,
        project_name: str,
    ):

        self.output_dir = output_dir
        self.project_name = project_name

    def generate(self):

        print("\n" + "=" * 70)
        print("🚀 ArchitectAI Code Generation Started")
        print("=" * 70)

        BackendGenerator(
            self.output_dir,
            self.project_name,
        ).generate()

        ModelGenerator(
            self.output_dir,
        ).generate()

        SchemaGenerator(
            self.output_dir,
        ).generate()

        RepositoryGenerator(
            self.output_dir,
        ).generate()

        ServiceGenerator(
            self.output_dir,
        ).generate()

        APIGenerator(
            self.output_dir,
        ).generate()

        print("\n" + "=" * 70)
        print("🎉 Project Generated Successfully")
        print("=" * 70)