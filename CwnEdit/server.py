import sys
from flask import Flask
from pathlib import Path

print(Path(__file__).parent)
sys.path.append(Path(__file__).parent)

from update_cwn import update
app = Flask(__name__)

@app.route("/")
def check_annot_server():
    ret = update()
    return "Testing"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200)
