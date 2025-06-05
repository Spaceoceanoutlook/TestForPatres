from fastapi import FastAPI
from routers import auth
import uvicorn

app = FastAPI()

app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
