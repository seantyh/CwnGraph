import pickle
from shutil import copyfile
from pathlib import Path
from .cwn_graph_utils import CwnGraphUtils

class CwnBase(CwnGraphUtils):
    def __init__(self):
        home_path = Path.home()                
        fpath = home_path / f".cwn_graph/cwn_graph.pyobj"
        if not fpath.exists():
            print("ERROR: install cwn_graph.pyobj first")
        with open(fpath, "rb") as fin:
            data = pickle.load(fin)
            if len(data) == 2:
                V, E = data
            else:
                V, E, meta = data
        super(CwnBase, self).__init__(V, E, meta)        
    
    @staticmethod
    def install_cwn(cwn_path):
        home_path = Path.home()
        cwn_user_dir = home_path / ".cwn_graph"
        if not cwn_user_dir.exists():
            cwn_user_dir.mkdir()
        try:        
            copyfile(cwn_path, cwn_user_dir / "cwn_graph.pyobj")
            print("CWN data installed")
        except FileNotFoundError as ex:
            print(ex)
            print("ERROR: install failed")