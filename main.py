from fastapi import FastAPI

from routers.auth import router as auth_router

app = FastAPI(
    title="JingHua Notex API",
    version="0.1.0",
)


app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Welcome to JingHua Notex"}
