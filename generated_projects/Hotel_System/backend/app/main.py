"""
Generated FastAPI Application
"""

from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.guest import Guest
from app.models.room import Room
from app.models.reservation import Reservation
from app.models.payment import Payment
from app.models.staff import Staff

from app.api import guest
from app.api import room
from app.api import reservation
from app.api import payment
from app.api import staff

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

app.include_router(guest.router)
app.include_router(room.router)
app.include_router(reservation.router)
app.include_router(payment.router)
app.include_router(staff.router)

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "API Generated Successfully"
    }
