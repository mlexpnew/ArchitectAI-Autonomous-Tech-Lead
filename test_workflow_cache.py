from workflow.ai_workflow_planner import AIWorkflowPlanner

planner = AIWorkflowPlanner(
    "outputs/Hospital_Management_System",
)

dag = planner.build(

    """
Hospital Management System

Patients

Doctors

Appointments

Billing

Inventory
"""

)

print()

print("=" * 60)

print("Workflow Nodes")

print("=" * 60)

for node in dag.nodes.values():

    print(node.name)