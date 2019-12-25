import sqlite3
import pickle
import logging
import sys
import os
import pdb
import CwnGraph
from CwnGraph import CWN_Graph, CwnGraphUtils
import CwnEdit.update_cwn as ce
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
timestamp = datetime.now().strftime("%y%m%d%H%M%S")
fh = logging.FileHandler(f"cwn_graph.{timestamp}.log", encoding="UTF-8")
ch = logging.StreamHandler()
formatter = logging.Formatter("%(name)s [%(levelname)s]: %(message)s")
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
ch.setLevel(logging.ERROR)
logger.addHandler(ch)
logger.addHandler(fh)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = sys.argv[1]
    else:
        task = "update"

    if task == "encode":
        conn = sqlite3.connect("data/cwn-2016.sqlite")
        cg = CWN_Graph(conn)
        with open("data/cwn_graph.pyobj", "wb") as fout:
            pickle.dump((cg.V, cg.E), fout)
    elif task == "query":
        with open("data/cwn_graph.pyobj", "rb") as fin:
            V, E = pickle.load(fin)
    
        cgu = CwnGraphUtils(V, E)
        gid = cgu.find_glyph("田")
        print(gid)
        lemmas = [x[0] for x in cgu.find_edges(gid)]
        print(lemmas)
        senses = [x[0] for lid in lemmas for x in cgu.find_edges(lid)]
        print(senses)
        rel = cgu.find_edges("06014001")

        print(rel)
    elif task == "json":
        if not os.path.exists("data/cwn_graph.pyobj"):
            print("Cannot find cwn_graph.pyobj")
            exit()

        with open("data/cwn_graph.pyobj", "rb") as fin:
            V, E = pickle.load(fin)
            CwnGraph.io.dump_json(V, E, "data/cwn_graph")

    elif task == "update":
        logger.info("Running update script")        
        ce.update()

    else:
        print("Not recognized task")
