import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies import session_db
from app.schemas.token import Token
from app.security.access_token import create_access_token
from app.security.authenticate_user import authenticate_user, define_user_role

router = APIRouter(
    prefix="/authorization",
    tags=["authorization"],
)


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

    user_role = define_user_role(session=session, user_id=form_data.username)  # str like "doctor,patient,"

    # create access token
    access_token = create_access_token(
        user_id=form_data.username,
        roles=user_role,
        expires_delta=access_token_expires,
        algorithm="HS256",
    )

    return Token(access_token=access_token, token_type="bearer", roles=user_role)
