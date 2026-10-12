from pydantic import BaseModel, ConfigDict, Field


class NoteRequest(BaseModel):
    id: int


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str


class NoteSummary(BaseModel):
    id: int
    title: str


class CreateNoteRequest(BaseModel):
    title: str


class UpdateNoteRequest(BaseModel):
    id: int
    title: str | None = None
    content: str | None = None
