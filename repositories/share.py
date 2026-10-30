from sqlalchemy import select
from sqlalchemy.orm import Session

from models.note import Note
from models.share import Share


def create_share(session: Session, note_id: int, share_code: str):
    existing_share = session.scalar(select(Share).where(Share.share_code == share_code))

    if existing_share:
        raise ValueError("Share already exists")

    share = Share(note_id=note_id, share_code=share_code)

    try:
        session.add(share)
        session.commit()
    except:
        session.rollback()
        raise

    return Share
