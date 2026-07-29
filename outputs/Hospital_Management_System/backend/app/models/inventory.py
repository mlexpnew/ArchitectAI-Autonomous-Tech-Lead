```

```python
# schemas.py
from pydantic import BaseModel
from datetime import date

class InventorySchema(BaseModel):
    id: int
    item_name: str
    quantity: int
    expiration_date: date

    class Config:
        orm_mode = True

SCHEMA_START
```

```python
# repositories.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Inventory

class InventoryRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_all(self):
        session = self.Session()
        return session.query(Inventory).all()

    def get_by_id(self, id):
        session = self.Session()
        return session.query(Inventory).filter(Inventory.id == id).first()

    def create(self, item):
        session = self.Session()
        session.add(item)
        session.commit()
        return item

    def update(self, id, item):
        session = self.Session()
        inventory = session.query(Inventory).filter(Inventory.id == id).first()
        if inventory:
            inventory.item_name = item.item_name
            inventory.quantity = item.quantity
            inventory.expiration_date = item.expiration_date
            session.commit()
            return inventory
        return None

    def delete(self, id):
        session = self.Session()
        inventory = session.query(Inventory).filter(Inventory.id == id).first()
        if inventory:
            session.delete(inventory)
            session.commit()
            return True
        return False

REPOSITORY_START
```

```python
# services.py
from repositories import InventoryRepository

class InventoryService:
    def __init__(self, db_url):
        self.repository = InventoryRepository(db_url)

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, item):
        return self.repository.create(item)

    def update(self, id, item):
        return self.repository.update(id, item)

    def delete(self, id):
        return self.repository.delete(id)

SERVICE_START
```

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from models import Inventory
from repositories import InventoryRepository
from services import InventoryService

app = FastAPI()

class InventorySchema(BaseModel):
    id: int
    item_name: str
    quantity: int
    expiration_date: str

@app.get("/inventory/")
def read_inventory():
    service = InventoryService("sqlite:///inventory.db")
    return service.get_all()

@app.get("/inventory/{id}")
def read_inventory_by_id(id: int):
    service = InventoryService("sqlite:///inventory.db")
    return service.get_by_id(id)

@app.post("/inventory/")
def create_inventory(item: InventorySchema):
    service = InventoryService("sqlite:///inventory.db")
    return service.create(Inventory(item_name=item.item_name, quantity=item.quantity, expiration_date=item.expiration_date))

@app.put("/inventory/{id}")
def update_inventory(id: int, item: InventorySchema):
    service = InventoryService("sqlite:///inventory.db")
    return service.update(id, Inventory(id=id, item_name=item.item_name, quantity=item.quantity, expiration_date=item.expiration_date))

@app.delete("/inventory/{id}")
def delete_inventory(id: int):
    service = InventoryService("sqlite:///inventory.db")
    return service.delete(id)

API_START
```