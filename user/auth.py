from fastapi_users.authentication import JWTAuthentication
from fastapi_users import FastAPIUsers
from user.models import user_db
from user.schemas import User, UserDB, UserCreate, UserUpdate

Secret = ""

auth_backends = []

jwt_authentication = JWTAuthentication(secret=Secret, lifetime_seconds=86400)

auth_backends.append(jwt_authentication)


fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
