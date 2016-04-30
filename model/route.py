import flask
from flask import Blueprint

routing = Blueprint('route', __name__,
                    url_prefix='/routing')


@routing.route('/')
def route_answer():
    _dict = {'HELLO': 'WORLD'}
    return flask.jsonify(**_dict)


datarouting = Blueprint('data', __name__, url_prefix='/data')


@datarouting.route('/json')
def json_data():
    try:
        with open('data1.json') as json_file:
            return json_file.read(), 200
    except EnvironmentError as e:
        print(e)
        return flask.jsonify(result={'status': 500})
