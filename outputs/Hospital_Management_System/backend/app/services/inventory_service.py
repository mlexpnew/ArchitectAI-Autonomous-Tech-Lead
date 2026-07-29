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