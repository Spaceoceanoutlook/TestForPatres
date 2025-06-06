from fastapi import FastAPI
from routers import auth, book, reader, borrowed
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(book.router)
app.include_router(reader.router)
app.include_router(borrowed.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
