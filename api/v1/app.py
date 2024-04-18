#!/usr/bin/python3
"""First endpoint for API stats"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

# Creating a CORS instance w/ a wildcard for any origin
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(close):
    """ Removes current storage"""
    storage.close()


# the 404 handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


# Setup the host and port to either env values or defaults
host = getenv("HBNB_API_HOST", default="0.0.0.0")
port = getenv("HBNB_API_PORT", default="5000")


if __name__ == "__main__":

    app.run(host=host, port=port, threaded=True)
