"""
Frontend activity checker main view

URLs include:
/
"""
import flask
import activity

@activity.app.route('/')
def show_index():
    """Display / route."""
    context = {}
    return flask.render_template("index.html", **context)