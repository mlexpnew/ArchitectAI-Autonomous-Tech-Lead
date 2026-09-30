"""
ArchitectAI Orchestrator

Runs the complete AI pipeline.
"""

from generators.ai.project_ai_generator import AIProjectGenerator


class ArchitectAI:

    def __init__(self, output_dir: str = "outputs/Hospital_Management_System"):

        self.output_dir = output_dir
        self.generator = AIProjectGenerator(
            self.output_dir,
        )

    def build(
        self,
        project_idea: str,
    ):

        print("\n" + "=" * 70)
        print("ArchitectAI Started")
        print("=" * 70)

        self.generator.generate(project_idea)

        print("\n" + "=" * 70)
        print("🎉 Project Generation Completed")
        print("=" * 70)