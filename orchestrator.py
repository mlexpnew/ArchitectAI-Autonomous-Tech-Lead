"""
ArchitectAI Orchestrator

Runs the complete AI pipeline.
"""

from generators.ai.project_ai_generator import AIProjectGenerator


class ArchitectAI:

    def __init__(self):

        self.generator = AIProjectGenerator(
            "outputs/Hospital_Management_System",
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