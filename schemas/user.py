import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


def validate_username(value: str) -> str:
    if len(value) < 3:
        raise ValueError("Username must have at least 3 characters")

    if len(value) > 25:
        raise ValueError("Username cannot exceed 25 characters")

    if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_.-]*", value):
        raise ValueError(
            "Username must start with a letter and can only contain letters, numbers, underscores (_), hyphens (-), or periods (.)"
        )

    return value


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must have at least 8 characters")

    if len(value) > 128:
        raise ValueError("Password cannot exceed 128 characters")

    return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def check_password(cls, value: str) -> str:
        return validate_password(value)


class UpdateUserRequest(BaseModel):
    new_username: str | None = None

    @field_validator("new_username")
    @classmethod
    def check_username(cls, value: str) -> str:
        return validate_username(value)


class DeleteUserRequest(BaseModel):
    password: str
