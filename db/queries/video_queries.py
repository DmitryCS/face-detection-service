from typing import List

from db.database import DBSession

from db.models.videos import DBVideo


def create_file(session: DBSession, video_name: str) -> DBVideo:
    new_video = DBVideo(
        video_name=video_name,
        status='waiting'
    )

    session.add_model(new_video)
    session.commit_session()
    return new_video


def update_status_video_by_id(session: DBSession, vid: int, status: str):
    session.update_status(vid=vid, status=status)
    session.commit_session()


def get_videos(session: DBSession) -> List[DBVideo]:
    return session.get_videos()


def update_video_data_by_id(session: DBSession, vid: int, cur_progress: int, num_faces: int, status: str = 'processing'):
    session.update_current_progress_video_by_id(vid, cur_progress)
    session.update_num_faces_video_by_id(vid, num_faces)
    if status != 'processing':
        session.update_status(vid=vid, status=status)
    session.commit_session()


def get_last_video_from_queue(session: DBSession) -> DBVideo:
    return session.get_waiting_video()


def get_video_by_id(session: DBSession, vid: int) -> DBVideo:
    return session.get_video_by_id(vid)


def cancel_video_processing(session: DBSession, vid: int) -> None:
    session.update_status(vid, 'canceled')
    session.commit_session()
