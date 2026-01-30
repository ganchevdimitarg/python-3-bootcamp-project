from typing import Optional

from pydantic import BaseModel, Field


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: Optional[int] = Field(gt=1999, lt=2030, description='Published date is not needed on create',
                                          default=None)

    # Swagger: example value
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book title",
                "author": "An author name",
                "description": "A new book description",
                "rating": 5,
                "published_date": 2021
            }
        }
    }
