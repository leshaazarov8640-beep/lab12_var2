from pydantic import BaseModel, Field, field_validator
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=10, max_length=20)
    published_year: int = Field(..., ge=1450, le=2026)
    genre: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., ge=0, le=10000)
    available_quantity: int = Field(..., ge=0, le=10000)

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        cleaned = v.replace("-", "").replace(" ", "")
        if not (len(cleaned) == 10 or len(cleaned) == 13):
            raise ValueError("ISBN must be 10 or 13 digits")
        if not cleaned.isdigit():
            raise ValueError("ISBN must contain only digits")
        return cleaned

    @field_validator("available_quantity")
    @classmethod
    def validate_available(cls, v: int, info) -> int:
        if "quantity" in info.data and v > info.data["quantity"]:
            raise ValueError("available_quantity cannot exceed quantity")
        return v


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    published_year: Optional[int] = Field(None, ge=1450, le=2026)
    genre: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, ge=0, le=10000)
    available_quantity: Optional[int] = Field(None, ge=0, le=10000)


class BookResponse(BookBase):
    id: int

    model_config = {"from_attributes": True}
