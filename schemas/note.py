from pydantic import BaseModel, ConfigDict, Field


class NoteRequest(BaseModel):
    id: int


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str


class CreateNoteRequest(BaseModel):
    title: str


class WriteContentRequest(BaseModel):
    id: int
    content: str


class ChangeTitleRequest(BaseModel):
    id: int
    title: str


class DeleteNoteRequest(BaseModel):
    id: int
