from flask import Response, Request

from db.database import DBSession
from db.queries.video_queries import get_video_by_id, cancel_video_processing
from transport.flask.endpoints.base import BaseEndpoint


class CancelProcessingVideoEndpoint(BaseEndpoint):

    def method_post(self, request: Request,  body: dict, session: DBSession, vid: str = None, *args, **kwargs) \
            -> Response:
        video = get_video_by_id(session, int(vid))
        if video and video.status == 'processing':
            cancel_video_processing(session, int(vid))
            return self.make_response_json(status=200)
        else:
            return self.make_response_json(body={'error': str(vid)}, status=200)
