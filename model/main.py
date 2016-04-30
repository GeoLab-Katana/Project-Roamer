from flask import Flask

import route

app = Flask(__name__)

app.register_blueprint(route.routing)
app.register_blueprint(route.datarouting)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
