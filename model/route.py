import flask
from flask import Blueprint

routing = Blueprint('route', __name__,
                    url_prefix='/routing')


@routing.route('/')
def route_answer():
    _dict = {'HELLO': 'WORLD'}
    return flask.jsonify(**_dict)
