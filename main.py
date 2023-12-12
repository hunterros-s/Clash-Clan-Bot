from flask import Flask, Response
import datacollect
from utils import *

import threading

app = Flask(__name__)

# Start a separate thread to update the dictionary
update_thread = threading.Thread(target=datacollect.data_coroutine)
update_thread.daemon = True
update_thread.start()

# TODO
# 0. manage kicked/leaved players. remove them if they haven't been in the clan for over a week? not sure the criteria?
# 2. Refactor everything in general, maybe new files? not sure. too difficult to read right now.

@app.route('/')
def get_data():
    pretty_json = json.dumps(datacollect.data, indent=4)  # Pretty print JSON with 4 spaces of indentation
    return Response(pretty_json, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=False)