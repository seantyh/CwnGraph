import sys
import logging
from pathlib import Path
from itertools import groupby
from io import StringIO
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from CwnGraph import CwnBase, CwnLemma, CwnSense, CwnSynset
from CwnGraph import CwnRelationType

sys.path.append(str(Path(__file__).parent))

app = Flask(__name__)
CORS(app)
cwn = CwnBase()

@app.route("/")
def index():
    return "CwnGraph API Server"     

@app.route("/data/<cwn_id>")
def data(cwn_id):
    if cwn_id in cwn.V:
        data = cwn.V[cwn_id]
        return jsonify(cwn_id=cwn_id, **data)

@app.route("/senses/<lemma_id>")
def senses(lemma_id):
    if not cwn.has_id(lemma_id):
        resp = jsonify(status="id not found")
        resp.status_code = 400
        return resp
    lemma = CwnLemma(lemma_id, cwn)
    ret_data = []
    for sense_x in lemma.senses:
        relations = sorted(sense_x.relations, key=lambda x: x[0])
        rel_groups = {}
        for grp_id, members in groupby(relations, lambda x: x[0]):
            rel_type = CwnRelationType[grp_id]
            if not rel_type.is_semantic_relation():
                continue
            for rel_type, mem_x, rel_direction in members:
                if rel_direction == "reversed": 
                    continue
                lem_x = mem_x.lemmas
                if lem_x and len(lem_x) > 0:
                    rel_item = (lem_x[0].lemma, mem_x.id)
                else:
                    continue
                rel_groups.setdefault(grp_id, []).append(rel_item)
        ret_data.append(dict(
            id=sense_x.id, 
            relations = rel_groups,
            **sense_x.data()))
    return jsonify(ret_data)

@app.route("/search/<search_text>")
def search(search_text):
    lemmas = cwn.find_lemma(search_text)
    ret_data = []
    for lemma_x in lemmas:
        ret_data.append(dict(
            id=lemma_x.id,
            **lemma_x.data()
        ))
    return jsonify(ret_data)

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=5201, debug=True)
    
