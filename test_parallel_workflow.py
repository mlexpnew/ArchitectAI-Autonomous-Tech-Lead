from workflow.dag import WorkflowDAG
from workflow.node import WorkflowNode

from workflow.parallel_executor import ParallelWorkflowExecutor


dag = WorkflowDAG()

dag.add_node(
    WorkflowNode(
        "Model",
        "model",
    )
)

dag.add_node(
    WorkflowNode(
        "Schema",
        "schema",
        ["Model"],
    )
)

dag.add_node(
    WorkflowNode(
        "Repository",
        "repository",
        ["Schema"],
    )
)

dag.add_node(
    WorkflowNode(
        "Service",
        "service",
        ["Repository"],
    )
)

dag.add_node(
    WorkflowNode(
        "API",
        "api",
        ["Service"],
    )
)

ParallelWorkflowExecutor(
    "outputs/Hospital_Management_System",
).execute(

    dag,

    "Patient",

    [

        "id : integer",

        "name : string",

        "age : integer",

        "phone : string",

    ],

)