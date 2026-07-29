"""
Generated FastAPI Application
"""

from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.student import Student
from app.models.teacher import Teacher
from app.models.department import Department
from app.models.course import Course
from app.models.enrollment import Enrollment

from app.api import student
from app.api import teacher
from app.api import department
from app.api import course
from app.api import enrollment

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

app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(department.router)
app.include_router(course.router)
app.include_router(enrollment.router)

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "API Generated Successfully"
    }
