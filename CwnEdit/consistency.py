import logging
import pandas as pd
from CwnGraph import CwnBase

logger = logging.getLogger("ConsistencyCheck")

def check_consistency(cwn: CwnBase, annot_df: pd.DataFrame):
    logger.info("In consistency check")
    V = {}
    E = {}
    cwn_data = (V, E)
    check_flag = False
    return cwn_data, check_flag