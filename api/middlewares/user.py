from werkzeug.wrappers import Request, Response, ResponseStream

from db.session import session_scope
from models import User


class UserMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        # hardcode this for now
        if True:
            with session_scope() as session:
                user = session.query(User).filter(User.email == "test@test.com").first()
                environ["user"] = user.to_dict()
            return self.app(environ, start_response)

        res = Response(u"Authorization failed", mimetype="text/plain", status=401)
        return res(environ, start_response)
