from pydantic import BaseModel, ConfigDict, Field


class NoteRequest(BaseModel):
    id: int
