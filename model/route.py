import flask
from flask import Blueprint, render_template, url_for
from flask.wrappers import Response

from model.file_source.server import Handler, Entry

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
        def generate():
            yield "{ \"type\":\"FeatureCollection\",\n" +"\"features\":["
            sent = 0
            to_send = 100000
            step = 10000
            with open('model/file_source/data.csv') as f:
                while sent < to_send:
                    Jsons = []
                    for entry in Handler.read_from_file(f, step):
                        Jsons.append(Entry.to_json(entry))
                    sent += step
                    join = ','.join(Jsons)
                    comma = ']}' if sent + step > to_send else ','
                    yield join+comma
        return Response(generate(), mimetype='application/json')

    except EnvironmentError as e:
        print(e)
        return flask.jsonify(result={'status': 500})
