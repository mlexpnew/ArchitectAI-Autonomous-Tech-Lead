"""
Autonomous Tech Lead

Top-level orchestrator for ArchitectAI.
"""

from workflow.ai_workflow_planner import AIWorkflowPlanner
from workflow.parallel_executor import ParallelWorkflowExecutor

from generators.ai.entity_extractor import AIEntityExtractor


class AutonomousTechLead:

    def __init__(
        self,
        output_dir: str,
    ):

        self.output_dir = output_dir

        self.entities = AIEntityExtractor()

        self.workflow = AIWorkflowPlanner(
            output_dir,
        )

        self.executor = ParallelWorkflowExecutor(
            output_dir,
        )

    def build(
        self,
        requirements: str,
    ):

        print()

        print("=" * 70)

        print("🚀 ArchitectAI Autonomous Tech Lead")

        print("=" * 70)

        dag = self.workflow.build(
            requirements,
        )

        entities = self.entities.extract(
            requirements,
        )

        for entity in entities:

            print()

            print("=" * 70)

            print(
                f"Building {entity['entity']}"
            )

            print("=" * 70)

            self.executor.execute(

                dag,

                entity["entity"],

                entity["fields"],

            )

        print()

        print("=" * 70)

        print("🎉 Project Generated Successfully")

        print("=" * 70)