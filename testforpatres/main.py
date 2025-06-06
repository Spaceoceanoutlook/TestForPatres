from fastapi import FastAPI
from routers import auth, book
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(book.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
