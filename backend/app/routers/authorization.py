import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies import session_db
from app.schemas.token import Token
from app.schemas.user import User
from app.security.access_token import create_access_token, decode_access_token
from app.security.authenticate_user import authenticate_user, define_user_role


def get_secret_key():
    # run command in .backend/ folder:
    # openssl rand -hex 32 > app/security/secret_key.txt
    with open('app/security/secret_key.txt', encoding="utf-8") as f:
        return f.readline()[0:-2]


router = APIRouter(
    prefix="/authorization",
    tags=["authorization"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./authorization/token")
secret_key = get_secret_key()


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(session_db),
) -> Token:

    # authenticate user
    is_verify_user = authenticate_user(
        session=session,
        user_id=form_data.username,
        password=form_data.password

    )
    if is_verify_user is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = datetime.timedelta(minutes=5)

    user_role = define_user_role(session=session, user_id=form_data.username)

    # create access token
    access_token = create_access_token(
        user_id=form_data.username,
        roles=user_role,
        expires_delta=access_token_expires,
        secret_key=secret_key,
        algorithm="HS256",
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/greeting")
async def get_greeting(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        jwt_payload = decode_access_token(
            token=token,
            secret_key=secret_key,
            algorithm="HS256",
        )
        user_id: str = jwt_payload.get("sub_id")
        roles: str = jwt_payload.get("roles")

        token_data = User(user_id=user_id, roles=roles)
    except InvalidTokenError:
        raise credentials_exception
    return {"greeting": f"Hello {token_data.user_id}"}
