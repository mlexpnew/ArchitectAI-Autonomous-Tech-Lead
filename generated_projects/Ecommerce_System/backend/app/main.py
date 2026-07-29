"""
Generated FastAPI Application
"""

from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.customer import Customer
from app.models.category import Category
from app.models.product import Product
from app.models.cart import Cart
from app.models.cartitem import CartItem
from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.payment import Payment
from app.models.address import Address

from app.api import customer
from app.api import category
from app.api import product
from app.api import cart
from app.api import cartitem
from app.api import order
from app.api import orderitem
from app.api import payment
from app.api import address

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

app.include_router(customer.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(cartitem.router)
app.include_router(order.router)
app.include_router(orderitem.router)
app.include_router(payment.router)
app.include_router(address.router)

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "API Generated Successfully"
    }
