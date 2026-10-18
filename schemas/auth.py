from pydantic import BaseModel, ConfigDict, Field, field_validator

from schemas.user import validate_password, validate_username


class RegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def check_username(cls, value: str) -> str:
        return validate_username(value)

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str) -> str:
        return validate_password(value)

    @field_validator("username")
    @classmethod
    def check_username(cls, value: str) -> str:
        return validate_username(value)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
