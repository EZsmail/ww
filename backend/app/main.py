from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.database import MongoDBClient
from .config.config import DATABASE_URL
from fastapi.staticfiles import StaticFiles




app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# TODO: Change in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(routes.router)


@app.get("/")
def read_root():
    return {"message": "Backend is running!"}


