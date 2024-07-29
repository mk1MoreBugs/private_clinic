from datetime import timedelta, datetime, timezone

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
from starlette import status

from app.dependencies import TokenDep
from app.schemas.user import User
from app.security.get_secret_key import get_secret_key


secret_key = get_secret_key()


def create_access_token(
        user_id: str,
        roles: str,
        expires_delta: timedelta,
        algorithm: str,
):
    to_encode = {
        "sub_id": user_id,
        "roles": roles
    }

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(
        token: str,
        algorithm: str,
):
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])

    return payload


def get_token_data(token: TokenDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        jwt_payload = decode_access_token(
            token=token,
            algorithm="HS256",
        )
        user_id: str = jwt_payload.get("sub_id")
        roles: str = jwt_payload.get("roles")

        token_data = User(user_id=user_id, roles=roles)
        return token_data
    except InvalidTokenError:
        raise credentials_exception
