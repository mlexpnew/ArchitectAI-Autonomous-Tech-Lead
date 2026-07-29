"""
AI Project Builder

Coordinates the complete project generation pipeline.
"""

from generators.ai.entity_extractor import AIEntityExtractor
from generators.ai.module_ai_generator import AIModuleGenerator


class AIProjectBuilder:

    def __init__(
        self,
        output_dir: str,
    ):

        self.output_dir = output_dir

        self.extractor = AIEntityExtractor()

        self.generator = AIModuleGenerator(
            output_dir,
        )

    def build(
        self,
        requirements: str,
    ):

        print("\n" + "=" * 70)
        print("🚀 ArchitectAI Project Builder")
        print("=" * 70)

        entities = self.extractor.extract(
            requirements,
        )

        for entity in entities:

            print(f"\n📦 Building {entity['entity']} Module")

            self.generator.generate(
                entity["entity"],
                entity["fields"],
            )

        print("\n🎉 Project Generation Complete")