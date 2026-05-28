from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas


def get_books(db: Session, skip: int = 0, limit: int = 100, search: str | None = None) -> list[models.Book]:
    query = db.query(models.Book)
    if search:
        query = query.filter(
            or_(
                models.Book.title.ilike(f"%{search}%"),
                models.Book.author.ilike(f"%{search}%"),
                models.Book.isbn.ilike(f"%{search}%"),
            )
        )
    return query.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> models.Book | None:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate) -> models.Book | None:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True
