from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status
from Book import Book
from BookRequest import BookRequest

app = FastAPI()

BOOKS = [
    Book(1, "Book 1", "Author 1", "1 dasdasd adasd asdas dasd asd asd d asdsa", 1, 2000),
    Book(2, "Book 2", "Author 2", "2 dasdasd adasd asdas dasd asd asd d asdsa", 3, 2000),
    Book(3, "Book 3", "Author 3", "3 dasdasd adasd asdas dasd asd asd d asdsa", 4, 2000),
    Book(4, "Book 4", "Author 4", "4 dasdasd adasd asdas dasd asd asd d asdsa", 3, 2024),
    Book(5, "Book 5", "Author 5", "5 dasdasd adasd asdas dasd asd asd d asdsa", 5, 2010),
]


@app.get("/v2/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app.get("/v2/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)): # Path(gt=0) path parameter validation
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(404, "Item not found")


@app.get("/v2/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt=0, lt=6)): # Query(gt=0, lt=6) query parameter validation
    return [book for book in BOOKS if book.rating == rating]


@app.get("/v2/books/published_date/", status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int = Query(gt=1999, lt=2030)):
    return [book for book in BOOKS if book.published_date == published_date]


@app.post("/v2/books/create", status_code=status.HTTP_201_CREATED)
async def create_book(request_body: BookRequest):
    new_book = Book(**request_body.model_dump())
    BOOKS.append(generate_book_id(new_book))


@app.put("/v2/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(request_body: BookRequest):
    is_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == request_body.id:
            BOOKS[i] = request_body
            is_updated = True
    if not is_updated:
        raise HTTPException(404, "Item not found") # HTTPException

@app.delete("/v2/books/delete_book/{title}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(title: str = Path(min_length=3)):
    is_removed = False
    for book in BOOKS:
        if book.title.casefold() == title.casefold():
            BOOKS.remove(book)
            is_removed = True
            break

    if not is_removed:
        raise HTTPException(404, "Item not found")


def generate_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book
