"""
Generated FastAPI Application
"""

from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.lead import Lead
from app.models.customer import Customer
from app.models.employee import Employee
from app.models.opportunity import Opportunity
from app.models.task import Task

from app.api import lead
from app.api import customer
from app.api import employee
from app.api import opportunity
from app.api import task

app = FastAPI(
    title="Generated API",
    version="1.0.0",
)

# ----------------------------------------
# Create database tables automatically
# ----------------------------------------

Base.metadata.create_all(bind=engine)

# ----------------------------------------
# Register Routers
# ----------------------------------------

app.include_router(lead.router)
app.include_router(customer.router)
app.include_router(employee.router)
app.include_router(opportunity.router)
app.include_router(task.router)

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "API Generated Successfully"
    }
