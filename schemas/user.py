import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


def validate_username(value: str) -> str:
    if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_.-]*", value):
        raise ValueError(
            "Usernames must start with a letter and can only contain letters, numbers, underscores (_), hyphens (-), or periods (.)."
        )
    return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class UpdateUserRequest(BaseModel):
    new_username: str | None = None

    @field_validator("new_username")
    @classmethod
    def check_username(cls, value: str) -> str:
        return validate_username(value)


class DeleteUserRequest(BaseModel):
    password: str
