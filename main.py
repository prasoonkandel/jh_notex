from fastapi import FastAPI

from routers.auth import router as auth_router
from routers.note import router as note_router
from routers.user import router as user_router

app = FastAPI(
    title="JingHua Notex API",
    version="0.1.0",
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(note_router)


@app.get("/")
async def root():
    return {"message": "Welcome to JingHua Notex"}
