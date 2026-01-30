from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "Book 1", "author": "Arabella Sorro", "category": "Outdoor"},
    {"title": "Book 2", "author": "Kristi Hateley", "category": "Fitness"},
    {"title": "Book 3", "author": "Lorne McGillivray", "category": "Accessories"},
    {"title": "Book 4", "author": "Laurens Levane", "category": "Food - Frozen Foods"},
    {"title": "Book 5", "author": "Paton Gifkins", "category": "Storage"},
    {"title": "Book 6", "author": "Glyn Brierton", "category": "Food - Breakfast"},
    {"title": "Book 7", "author": "Cece Bilbie", "category": "Home"},
    {"title": "Book 8", "author": "Jareb Ginnally", "category": "Kitchen"},
    {"title": "Book 9", "author": "Hammad Craufurd", "category": "Food - Snacks"},
    {"title": "Book 10", "author": "Lauralee Kamiyama", "category": "Food - Beverages"},
    {"title": "Book 12", "author": "Farleigh Grant", "category": "Food - Desserts"},
    {"title": "Book 13", "author": "Leland Bastard", "category": "Food - Beverages"},
    {"title": "Book 14", "author": "Gerrilee Pristnor", "category": "Outdoor"},
    {"title": "Book 15", "author": "Ephrayim Hopkins", "category": "Food - Condiments"},
    {"title": "Book 16", "author": "Carey Tomson", "category": "Food - Snacks"},
    {"title": "Book 17", "author": "Kristi Hateley", "category": "Fitness"},
    {"title": "Book 18", "author": "Elysee Dowdam", "category": "Outdoor"},
    {"title": "Book 19", "author": "Michale Gabbat", "category": "Food - Bakery"},
    {"title": "Book 20", "author": "Jillene Tukesby", "category": "Kitchen"},
    {"title": "Book 21", "author": "Ray Drain", "category": "Food - Baking"},
    {"title": "Book 22", "author": "Guy Reast", "category": "Food - Snacks"},
    {"title": "Book 23", "author": "Gertie Plews", "category": "Food - Dairy"},
    {"title": "Book 24", "author": "Fey Vasyutochkin", "category": "Kitchen"},
    {"title": "Book 25", "author": "Horten Burnhill", "category": "Food - Dairy"},
    {"title": "Book 26", "author": "Deirdre Haggarth", "category": "Pets"},
    {"title": "Book 27", "author": "Clarance Bromhead", "category": "Home"},
    {"title": "Book 28", "author": "Gerrilee Pristnor", "category": "Fitness"},
    {"title": "Book 29", "author": "Odell Sommer", "category": "Garden"},
    {"title": "Book 30", "author": "Judas Linny", "category": "Home"}
]

@app.get("/api/v1/books")
async def get_all_books():
    return BOOKS

@app.get("/api/v1/books/{title}")
async def get_book_by_title(title: str):
    for book in BOOKS:
        if book.get("title").casefold() == title.casefold():
            return book
    return None

@app.get("/api/v1/books/")
async def get_book_by_category(category: str):
    return [book for book in BOOKS if book.get("category").casefold() == category.casefold()]

@app.get("/api/v1/books/{author}/")
async def get_book_by_author_category(author: str, category: str):
    return [book for book in BOOKS if book.get("author").casefold() == author.casefold() \
            and book.get("category").casefold() == category.casefold()]

@app.post("/api/v1/books/create_book")
async def create_book(book=Body()):
    BOOKS.append(book)

@app.put("/api/v1/books/update_book")
async def create_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == update_book.get("title").casefold():
            BOOKS[i] = update_book

@app.delete("/api/v1/books/delete_bok/{title}")
async def create_book(title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == title.casefold():
            BOOKS.pop(i)
            break