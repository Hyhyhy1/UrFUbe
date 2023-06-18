import uvicorn
from pathlib import Path
from fastapi import FastAPI
from video.api import video_router
from user.routers import user_router
from followers.api import follower_router
from fastapi.staticfiles import StaticFiles
from db import database, metadata, engine


app = FastAPI()

metadata.create_all(engine)
app.state.database = database

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "templates/static", html=True),
    name="static",
)


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(video_router)
app.include_router(user_router)
app.include_router(follower_router)

if __name__ == '__main__':
    uvicorn.run(app)
