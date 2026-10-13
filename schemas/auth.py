from pydantic import BaseModel, ConfigDict, Field, field_validator

from schemas.user import validate_username


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=25,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )

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
