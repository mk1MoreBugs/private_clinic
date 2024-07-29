from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    roles: str


class TokenData(BaseModel):
    username: str | None = None
