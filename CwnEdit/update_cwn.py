from typing import Tuple, Dict
import pandas as pd
import logging


logger = logging.getLogger()


V = Dict[str, any]
E = Dict[(str, str), any]
CwnGraphData = Tuple[V, E]
AnnotationData: Dict[str, pd.DataFrame]
CheckResult = bool
MergeResult = Tuple[CwnGraphData, CheckResult]


def update_cwn(sheet_url, cwn) -> MergeResult:
    # ----- annotation_check.py ----
    # 1. google sheet data import  (sheet -> pd.DataFrame)
    # 2. data validation   (pd.DataFrame -> pd.DataFrame)
    #  2a. duplication check
    #  2b. synonym definition check
    
    # annot_df: AnnotationData
    # import_flag: bool
    annot_df, import_flag = import_from_google_sheets(sheet_url)

    # ----------------------------

    #  2c. synset, 同義詞的連結一致 (AnnotationData -> CwnGraphData)
    #      hyper/hypo, hyper/tropo, holo/mero

    # cwn_data: CwnGraphData
    # check_flag: bool
    cwn_data, check_flag = check_consistency(annot_df)


    return cwn_data, import_flag and check_flag

# 3a. dump to pickle (CwnGraphData -> IO[pickle])
def export_to_pickle(cwn_data: CwnGraphData):
    pass 

# 3a. dump to pickle (CwnGraphData -> IO[json])
def export_to_json(cwn_data: CwnGraphData):
    pass