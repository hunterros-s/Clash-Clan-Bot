from flask import Flask, Response
import datacollect
from utils import *

import threading

app = Flask(__name__)

# Start a separate thread to update the dictionary
update_thread = threading.Thread(target=datacollect.data_coroutine)
update_thread.daemon = True
update_thread.start()

@app.route('/')
def get_data():
    pretty_json = json.dumps(datacollect.data, indent=4)  # Pretty print JSON with 4 spaces of indentation
    return Response(pretty_json, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)