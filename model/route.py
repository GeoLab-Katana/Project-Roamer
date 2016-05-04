import flask
from flask import Blueprint, render_template

from file_source.data_source import DataSource
from file_source.data_source import SQLDataSource
from file_source.data_source import Entry

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
            result = "{ \"type\":\"FeatureCollection\",\n" +"\"features\":["
            # data_source = DataSource.get_instance()
            data_source = SQLDataSource()
            # entryies = data_source.get_entries()
            # while sent < to_send:
            Jsons = []
            for entry in data_source.get_entries():
                Jsons.append(Entry.to_json(entry))
            _join = ','.join(Jsons)
            comma = ']}'# if sent + step > to_send else ','
            result += _join + comma
            return result
        return generate()

    except EnvironmentError as e:
        print(e)
        return flask.jsonify(result={'status': 500})
