"""
Generated FastAPI Application
"""

from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.supplier import Supplier
from app.models.inventory import Inventory
from app.models.purchaseorder import PurchaseOrder

from app.api import product
from app.api import warehouse
from app.api import supplier
from app.api import inventory
from app.api import purchaseorder

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

app.include_router(product.router)
app.include_router(warehouse.router)
app.include_router(supplier.router)
app.include_router(inventory.router)
app.include_router(purchaseorder.router)

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "API Generated Successfully"
    }
