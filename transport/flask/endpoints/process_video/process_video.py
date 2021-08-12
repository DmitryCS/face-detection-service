import os
import uuid

from flask import Request, Response

from db.database import DBSession
from db.queries import video_queries
from db.queries.video_queries import get_videos
from transport.flask.endpoints.base import BaseEndpoint


class ProcessingVideoEndpoint(BaseEndpoint):

    def method_get(
            self, request: Request, body: dict, session: DBSession, *args, **kwargs
    ) -> Response:
        videos = get_videos(session)
        dict_response = {"videos": []}
        for video in videos:
            dict_response["videos"].append(
                {
                    "id": str(video.id),
                    "status": video.status,
                    "current_progress": video.current_progress,
                    "result_aggregation": {
                        "faces_count": video.faces_count
                    }
                }
            )
        return self.make_response_json(body=dict_response, status=200)

    def method_post(
            self, request: Request, body: dict, session: DBSession, *args, **kwargs
    ) -> Response:
        if not os.path.exists('raw_videos'):
            os.makedirs('raw_videos')
        video = request.files['video']
        video_name = '.'.join([str(uuid.uuid4()), video.filename.split('.')[-1]])
        path_to_video = os.path.join('raw_videos', video_name)
        video.save(path_to_video)
        db_video = video_queries.create_file(session, video_name)

        return self.make_response_json(body={"video_id": str(db_video.id)}, status=200)
