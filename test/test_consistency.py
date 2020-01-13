
import logging
logging.basicConfig()
logging.getLogger().setLevel("INFO")

import sys
sys.path.append("CwnEdit")
from CwnGraph import CwnBase
import pandas as pd
# pylint: disable=import-error
from consistency import check_consistency

from pathlib import Path


def test_consistency(caplog):
    caplog.set_level(logging.INFO)    
    cwn = CwnBase()
    basepath = Path(__file__).parent / "../data"
    annot_dfs = {
        "lemma": pd.read_csv(basepath/"sense_no_relation - lemma.csv"),
        "sense": pd.read_csv(basepath/"sense_no_relation - sense.csv"),
        "lex_rel": pd.read_csv(basepath/"sense_no_relation - lexical relation.csv"),
    }
    check_consistency(cwn, annot_dfs)    
    assert True