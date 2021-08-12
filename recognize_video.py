import os
import time

import cv2
from sqlalchemy import create_engine

from db.config import SQLiteConfig
from db.database import DBSession, DataBase
from db.queries.video_queries import update_status_video_by_id, update_video_data_by_id, get_last_video_from_queue, \
    get_video_by_id


def remove_video(path_to_video: str):
    try:
        os.remove(path_to_video)
    except FileNotFoundError:
        pass    # print('Error: video does not exist')


def detect_new_video(session: DBSession, vid: int, path_to_video, path_to_save_video, rm_files: bool = True):
    update_status_video_by_id(session=session, vid=vid, status='processing')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    video = cv2.VideoCapture(path_to_video)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if not rm_files:
        fps = int(video.get(cv2.CAP_PROP_FPS))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_file = cv2.VideoWriter(path_to_save_video, fourcc, fps, (width, height), True)
    num_faces = 0
    for i in range(num_frames):
        _, img = video.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        num_faces = max(num_faces, len(faces))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            if not rm_files:
                output_file.write(img)
        cur_progress = i * 100 // num_frames
        update_video_data_by_id(session, vid, cur_progress, num_faces)
        db_video = get_video_by_id(session, vid)
        if db_video and db_video.status == 'canceled':
            video.release()
            remove_video(path_to_video)
            session.close_session()
            return None
    video.release()
    if not rm_files:
        output_file.release()
    update_video_data_by_id(session, vid, 100, num_faces, 'completed')
    session.close_session()
    if rm_files:
        remove_video(path_to_video)


def main_predict_video():
    config = SQLiteConfig()  # PostgresConfig()
    engine = create_engine(
        url=config.url,
        pool_pre_ping=True,  # if session dropped, it'll automatically launched
    )
    database = DataBase(connection=engine)
    database.check_connection()
    if not os.path.exists('raw_videos'):
        os.makedirs('raw_videos')
    while True:
        session: DBSession = database.make_session()
        new_video = get_last_video_from_queue(session)
        if new_video:
            path_to_video = os.path.join('raw_videos', new_video.video_name)
            path_to_save_video = path_to_video[:-4] + '_released' + '.mp4'
            detect_new_video(session, new_video.id, path_to_video, path_to_save_video)
            session.commit_session(need_close=True)
        else:
            session.close_session()
            time.sleep(0.5)
