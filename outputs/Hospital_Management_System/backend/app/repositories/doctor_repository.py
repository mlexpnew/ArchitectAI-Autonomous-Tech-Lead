```

```python
# services.py
from repository import DoctorRepository

class DoctorService:
    def __init__(self, db_url):
        self.repository = DoctorRepository(db_url)

    def get_all_doctors(self):
        return self.repository.get_all_doctors()

    def get_doctor_by_id(self, id):
        return self.repository.get_doctor_by_id(id)

    def create_doctor(self, doctor):
        return self.repository.create_doctor(doctor)

    def update_doctor(self, id, doctor):
        return self.repository.update_doctor(id, doctor)

    def delete_doctor(self, id):
        self.repository.delete_doctor(id)

SERVICE_START
```

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from services import DoctorService
from schemas import DoctorSchema

app = FastAPI()

@app.get("/doctors/")
def read_doctors():
    service = DoctorService("sqlite:///doctors.db")
    return service.get_all_doctors()

@app.get("/doctors/{id}")
def read_doctor(id: int):
    service = DoctorService("sqlite:///doctors.db")
    return service.get_doctor_by_id(id)

@app.post("/doctors/")
def create_doctor(doctor: DoctorSchema):
    service = DoctorService("sqlite:///doctors.db")
    return service.create_doctor(doctor)

@app.put("/doctors/{id}")
def update_doctor(id: int, doctor: DoctorSchema):
    service = DoctorService("sqlite:///doctors.db")
    return service.update_doctor(id, doctor)

@app.delete("/doctors/{id}")
def delete_doctor(id: int):
    service = DoctorService("sqlite:///doctors.db")
    service.delete_doctor(id)
    return {"message": "Doctor deleted successfully"}

API_START
```