from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session

from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBVideo


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs):
        return self._session.query(*args, **kwargs)

    def close_session(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def update_status(self, vid: int, status: str):
        self.query(DBVideo).filter(DBVideo.id == vid).first().status = status

    def get_videos(self) -> List[DBVideo]:
        return self.query(DBVideo).all()

    def update_current_progress_video_by_id(self, vid: int, current_progress: int):
        self.query(DBVideo).filter(DBVideo.id == vid).first().current_progress = current_progress

    def update_num_faces_video_by_id(self, vid: int, num_faces: int):
        self.query(DBVideo).filter(DBVideo.id == vid).first().faces_count = num_faces

    def get_waiting_video(self) -> DBVideo:
        return self.query(DBVideo).filter(DBVideo.status == 'waiting').first()

    def get_video_by_id(self, vid: int):
        return self.query(DBVideo).filter(DBVideo.id == vid).first()

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()


class DataBase:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)
