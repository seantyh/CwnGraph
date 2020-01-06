import sys
sys.path.append("CwnEdit")
from CwnGraph import CwnBase
from consistency import check_consistency

def test_consistency():
    cwn = CwnBase()
    annot_dfs = {}
    check_consistency(cwn, annot_dfs)    