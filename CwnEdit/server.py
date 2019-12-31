import sys
import logging
from pathlib import Path
from io import StringIO
from flask import Flask, jsonify
from flask_cors import CORS

sys.path.append(str(Path(__file__).parent))

from update_cwn import update
app = Flask(__name__)
CORS(app)

log_buf = StringIO()
logger = logging.getLogger()
sh = logging.StreamHandler(log_buf)
formatter = logging.Formatter("[%(levelname)s] %(name)s - %(message)s")
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
logger.addHandler(sh)

@app.route("/")
def check_annot_server():
    ret = update()
    resp = jsonify(retCode=ret, logs=log_buf.getvalue().split("\n"))
    return resp

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=5200)
