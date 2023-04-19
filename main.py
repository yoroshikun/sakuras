from fastapi import FastAPI
from routes import mount_routes

app = FastAPI()

mount_routes(app);