from sqlalchemy import select
from sqlalchemy.orm import Session

from models.note import Note
from models.share import Share
from repositories.note import get_note_by_id


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


def get_shared_note(session: Session, share_code: str):
    share = session.scalar(select(Share).where(Share.share_code))

    if not share:
        raise ValueError("Share does not exists!")

    note = get_note_by_id(session, share.note_id)

    return note
