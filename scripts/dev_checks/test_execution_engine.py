from planner.task_planner import TaskPlanner

from executor.execution_engine import ExecutionEngine


requirements = """
Build an AI Hospital Management System.

Patients

Doctors

Appointments

Billing

Inventory

Payments
"""

planner = TaskPlanner()

tasks = planner.plan(requirements)

engine = ExecutionEngine()

engine.execute(tasks)