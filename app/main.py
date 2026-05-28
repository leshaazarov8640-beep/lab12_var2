from fastapi import FastAPI
from app.database import engine, Base
from app.routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="REST API for managing a library's book catalog",
    version="1.0.0",
)

app.include_router(books.router, prefix="/api/v1", tags=["books"])
