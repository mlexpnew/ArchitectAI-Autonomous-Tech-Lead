"""
Generated FastAPI Application
"""

from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.book import Book
from app.models.author import Author
from app.models.publisher import Publisher
from app.models.member import Member
from app.models.borrowrecord import BorrowRecord

from app.api import book
from app.api import author
from app.api import publisher
from app.api import member
from app.api import borrowrecord

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

app.include_router(book.router)
app.include_router(author.router)
app.include_router(publisher.router)
app.include_router(member.router)
app.include_router(borrowrecord.router)

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "API Generated Successfully"
    }
