"""
AI Project Generator
"""

from generators.ai.entity_extractor import AIEntityExtractor

from generators.ai.model_ai_generator import AIModelGenerator
from generators.ai.schema_ai_generator import AISchemaGenerator
from generators.ai.repository_ai_generator import AIRepositoryGenerator
from generators.ai.service_ai_generator import AIServiceGenerator
from generators.ai.api_ai_generator import AIAPIGenerator


class AIProjectGenerator:

    def __init__(self, output_dir):

        self.output_dir = output_dir

    def generate(self, requirements: str):

        extractor = AIEntityExtractor()

        entities = extractor.extract(requirements)

        for entity in entities:

            name = entity["entity"]

            fields = entity["fields"]

            AIModelGenerator(self.output_dir).generate(
                name,
                fields,
            )

            AISchemaGenerator(self.output_dir).generate(
                name,
                fields,
            )

            AIRepositoryGenerator(self.output_dir).generate(
                name,
            )

            AIServiceGenerator(self.output_dir).generate(
                name,
            )

            AIAPIGenerator(self.output_dir).generate(
                name,
            )

            print(f"✅ {name} completed")

        print("\n🎉 Entire Backend Generated")