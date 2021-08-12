from sqlalchemy import Column, VARCHAR, Integer, BOOLEAN

from db.models import BaseModel


class DBVideo(BaseModel):

    __tablename__ = 'videos'

    video_name = Column(
        VARCHAR(1024),
        nullable=False,
    )
    status = Column(
        VARCHAR(1024),
        nullable=False,
    )
    current_progress = Column(
        Integer,
        nullable=False,
        default=0
    )
    faces_count = Column(
        Integer,
        nullable=False,
        default=0
    )
    is_delete = Column(
        BOOLEAN(),
        nullable=False,
        default=False
    )
