```

```python
# services.py
from typing import List
from repository import ReportRepository

class ReportService:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, report: Report):
        return self.repository.create(report)

    def update(self, id: int, report: Report):
        return self.repository.update(id, report)

    def delete(self, id: int):
        return self.repository.delete(id)

SERVICE_START
```

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from database import SessionLocal
from services import ReportService
from schemas import ReportSchema

app = FastAPI()

@app.get("/reports/")
def get_all_reports(service: ReportService = Depends()):
    return service.get_all()

@app.get("/reports/{id}")
def get_report_by_id(id: int, service: ReportService = Depends()):
    return service.get_by_id(id)

@app.post("/reports/")
def create_report(report: ReportSchema, service: ReportService = Depends()):
    return service.create(report)

@app.put("/reports/{id}")
def update_report(id: int, report: ReportSchema, service: ReportService = Depends()):
    return service.update(id, report)

@app.delete("/reports/{id}")
def delete_report(id: int, service: ReportService = Depends()):
    return service.delete(id)

API_START
```