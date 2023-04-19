from fastapi import FastAPI

def mount_route(app):
    @app.get("/")
    async def root():
        return {"message": "Hello World"}