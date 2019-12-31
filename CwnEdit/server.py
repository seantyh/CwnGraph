import sys
import logging
from pathlib import Path
from io import StringIO
from flask import Flask, jsonify, render_template
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
    log_buf.truncate(0)
    log_buf.seek(0)
    ret = update()
    log_str = log_buf.getvalue()
    if ret:
        return f"<pre style='padding: 1em; border-left: 2px solid blue'>{log_str}</pre>"
    else:
        return f"<pre style='padding: 1em; border-left: 2px solid orange'>{log_str}</pre>"        
    

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=5200, debug=True)
    
