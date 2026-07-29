"""
Generated FastAPI Application
"""

from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.customer import Customer
from app.models.branch import Branch
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.card import Card
from app.models.loan import Loan

from app.api import customer
from app.api import branch
from app.api import account
from app.api import transaction
from app.api import card
from app.api import loan

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
app.include_router(branch.router)
app.include_router(account.router)
app.include_router(transaction.router)
app.include_router(card.router)
app.include_router(loan.router)

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "API Generated Successfully"
    }
