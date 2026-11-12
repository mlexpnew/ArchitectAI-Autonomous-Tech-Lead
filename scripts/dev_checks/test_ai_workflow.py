from workflow.ai_workflow_planner import AIWorkflowPlanner

from workflow.parallel_executor import ParallelWorkflowExecutor


requirements = """
Hospital Management System

Patients

Doctors

Appointments

Payments

Inventory
"""

planner = AIWorkflowPlanner()

dag = planner.build(requirements)

ParallelWorkflowExecutor(
    "outputs/Hospital_Management_System"
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