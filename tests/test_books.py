import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/books", json={
            "title": "Война и мир",
            "author": "Лев Толстой",
            "isbn": "9783161484100",
            "published_year": 1869,
            "genre": "Роман",
            "quantity": 5,
            "available_quantity": 5,
        })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Война и мир"
    assert data["isbn"] == "9783161484100"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_create_book_duplicate_isbn():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/books", json={
            "title": "Book A", "author": "Author A", "isbn": "9783161484100",
            "published_year": 2000, "genre": "Fiction", "quantity": 1, "available_quantity": 1,
        })
        response = await client.post("/api/v1/books", json={
            "title": "Book B", "author": "Author B", "isbn": "9783161484100",
            "published_year": 2001, "genre": "Fiction", "quantity": 1, "available_quantity": 1,
        })
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/books", json={
            "title": "Test Book", "author": "Test Author", "isbn": "9783161484101",
            "published_year": 2020, "genre": "Test", "quantity": 1, "available_quantity": 1,
        })
        response = await client.get("/api/v1/books")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_book_by_id():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/books", json={
            "title": "Test Book", "author": "Test Author", "isbn": "9783161484102",
            "published_year": 2020, "genre": "Test", "quantity": 1, "available_quantity": 1,
        })
        book_id = create_resp.json()["id"]
        response = await client.get(f"/api/v1/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id


@pytest.mark.asyncio
async def test_get_book_not_found():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/books/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_book():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/books", json={
            "title": "Original Title", "author": "Author", "isbn": "9783161484103",
            "published_year": 2020, "genre": "Test", "quantity": 1, "available_quantity": 1,
        })
        book_id = create_resp.json()["id"]
        response = await client.put(f"/api/v1/books/{book_id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_update_book_not_found():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.put("/api/v1/books/9999", json={"title": "Nope"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_book():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/books", json={
            "title": "To Delete", "author": "Author", "isbn": "9783161484104",
            "published_year": 2020, "genre": "Test", "quantity": 1, "available_quantity": 1,
        })
        book_id = create_resp.json()["id"]
        response = await client.delete(f"/api/v1/books/{book_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_book_not_found():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/api/v1/books/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_search_books():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/books", json={
            "title": "Python Programming", "author": "John Doe", "isbn": "9783161484105",
            "published_year": 2021, "genre": "Education", "quantity": 3, "available_quantity": 3,
        })
        await client.post("/api/v1/books", json={
            "title": "Java Basics", "author": "Jane Doe", "isbn": "9783161484106",
            "published_year": 2022, "genre": "Education", "quantity": 2, "available_quantity": 2,
        })
        response = await client.get("/api/v1/books?search=Python")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Python Programming"


@pytest.mark.asyncio
async def test_invalid_isbn():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/books", json={
            "title": "Bad ISBN", "author": "Author", "isbn": "invalid-isbn",
            "published_year": 2020, "genre": "Test", "quantity": 1, "available_quantity": 1,
        })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_available_quantity_exceeds_total():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/books", json={
            "title": "Invalid Qty", "author": "Author", "isbn": "9783161484107",
            "published_year": 2020, "genre": "Test", "quantity": 1, "available_quantity": 5,
        })
    assert response.status_code == 422
