from datetime import timedelta, datetime, timezone

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
from starlette import status

from app.schemas.user import User


def create_access_token(
        user_id: str,
        roles: str,
        expires_delta: timedelta,
        secret_key: str,
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
        secret_key: str,
        algorithm: str,
):
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])

    return payload
