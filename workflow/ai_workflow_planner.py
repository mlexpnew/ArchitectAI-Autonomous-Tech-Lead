"""
AI Workflow Planner
"""

import json

from generators.ai.code_generator import AICodeGenerator

from workflow.dag import WorkflowDAG
from workflow.node import WorkflowNode
from workflow.workflow_cache import WorkflowCache


class AIWorkflowPlanner:

    def __init__(
        self,
        output_dir: str,
    ):

        self.ai = AICodeGenerator()

        self.cache = WorkflowCache(
            output_dir,
        )

    def build(
        self,
        requirements: str,
    ):

        if self.cache.exists():

            print("📦 Loading cached workflow...")

            return self.cache.load()

        prompt = f"""
You are a Principal Software Architect.

Create the execution workflow.

Requirements:

{requirements}

Available Plugins

- model
- schema
- repository
- service
- api

Return ONLY JSON.

Example

[
    {{
        "name":"Model",
        "plugin":"model",
        "dependencies":[]
    }},
    {{
        "name":"Schema",
        "plugin":"schema",
        "dependencies":["Model"]
    }}
]
"""

        response = self.ai.generate(prompt)

        response = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(response)

        dag = WorkflowDAG()

        for node in data:

            dag.add_node(

                WorkflowNode(

                    name=node["name"],

                    plugin=node["plugin"],

                    dependencies=node["dependencies"],

                )

            )

        self.cache.save(dag)

        return dag