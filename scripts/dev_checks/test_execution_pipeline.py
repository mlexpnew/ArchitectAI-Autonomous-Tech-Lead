from planner.task import Task

from executor.execution_engine import ExecutionEngine


tasks = [

    Task(
        step=1,
        title="Generate Models",
        description="",
    ),

    Task(
        step=2,
        title="Generate Schemas",
        description="",
    ),

    Task(
        step=3,
        title="Generate Repository",
        description="",
    ),

    Task(
        step=4,
        title="Generate Service",
        description="",
    ),

    Task(
        step=5,
        title="Generate API",
        description="",
    ),

]

engine = ExecutionEngine(
    "outputs/Hospital_Management_System",
)

engine.execute(

    tasks,

    "Patient",

    [

        "id : integer",

        "name : string",

        "age : integer",

        "gender : string",

        "phone : string",

    ],

)