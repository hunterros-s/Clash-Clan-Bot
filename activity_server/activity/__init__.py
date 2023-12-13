"""Activity manager package initializer."""
import flask

app = flask.Flask(__name__)

import activity.views