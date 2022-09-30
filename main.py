import uvicorn

from fastapi import FastAPI

from api.user_router import router as user_router

from db import models
from db.config import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/api/v1/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
