from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import session_db
from app.schemas.token import Token

router = APIRouter(
    prefix="/authorization",
    tags=["authorization"],
)


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # authenticate user

    # access_token_expires

    # create access token

    # return token

    pass


def verify_password(plain_password, hashed_password):
    pass


def authenticate_user(
        user_id: int,
        session: Session = Depends(session_db),

):
    pass


def define_user_role(
        user_id: int,
        session: Session = Depends(session_db),
):
    pass


def create_access_token():
    pass