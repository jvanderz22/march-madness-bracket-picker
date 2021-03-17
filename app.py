from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse

from api.resources.brackets import BracketResource, BracketsResource
from api.middlewares.user import UserMiddleware

app = Flask(__name__, static_url_path="")
app.wsgi_app = UserMiddleware(app.wsgi_app)
api = Api(app)


api.add_resource(BracketsResource, "/brackets")
api.add_resource(BracketResource, "/brackets/<bracket_id>")
