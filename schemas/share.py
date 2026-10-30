from pydantic import BaseModel


class ShareResponse(BaseModel):
    share_code: str
