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