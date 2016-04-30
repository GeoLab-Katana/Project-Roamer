import flask
from flask import Blueprint, render_template, url_for

routing = Blueprint('route', __name__,
                    url_prefix='/routing')


@routing.route('/')
def route_answer():
    _dict = {'HELLO': 'WORLD'}
    for key, val in flask.request.args.items():
        _dict[key] = val
    return flask.jsonify(**_dict)


@routing.route('/test')
def test():
    return render_template('index.html')


datarouting = Blueprint('data', __name__, url_prefix='/data')


@datarouting.route('/json')
def json_data():
    try:
        with open('data1.json') as json_file:
            return json_file.read(), 200
    except EnvironmentError as e:
        print(e)
        return flask.jsonify(result={'status': 500})
