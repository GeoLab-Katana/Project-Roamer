from flask import Flask, send_from_directory

import route
from reducer.reducer import Reducer

app = Flask(__name__)

app.register_blueprint(route.routing)
app.register_blueprint(route.datarouting)


@app.route('/favicon.ico')
def serve_icon():
    return send_from_directory(app.static_folder, 'favicon.ico')


if __name__ == '__main__':
    # rd = Reducer('file_source/data.csv')
    # rd.reduce_data()
    app.run(host='0.0.0.0', port=8080, debug=True)
