from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class UpdateUserRequest(BaseModel):
    old_password: str | None = None
    new_password: str | None = None
    new_username: str | None = None


class DeleteUserRequest(BaseModel):
    password: str
