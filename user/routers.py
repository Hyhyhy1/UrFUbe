from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from user.api import on_after_register
from user.auth import jwt_authentication, fastapi_users

templates = Jinja2Templates(directory="templates")

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
user_router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)


@user_router.get('/', response_class=HTMLResponse)
async def auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@user_router.get("/me", response_class=HTMLResponse)
async def user_home(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})


user_router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

