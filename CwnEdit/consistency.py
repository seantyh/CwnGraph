import logging
import pandas as pd
from typing import Dict
from datetime import datetime
from CwnGraph import CwnBase, CwnAnnotator
from CwnEdit.cwnedit_types import *
from CwnEdit.transform import transform_dataframe

logger = logging.getLogger("ConsistencyCheck")

def check_consistency(cwn: CwnBase, annot_dfs: Dict[str, pd.DataFrame]) -> CwnGraphData:   
    """
    Check the semantic relations among senses

    * 2c. Semantic relations consistency Check (AnnotationData -> CwnGraphData)
    
      * 2c.1 Synset identification
      * 2c.1.1 All synsets have the same definition
      * 2c.1.2 All senses having the same definitions are synsets
    
    * 2c.2 Synset check
      * 2c.2.1 All synsets have the same semantic relations
      * 2c.2.2 All senses in a synset have same semantic relations with other senses

    * 2c.3 inverse relations
      * 2c.3.1 All hypernymy noun sense pairs are also hyponymy pairs in reversed direction.
      * 2c.3.2 All hypernyny verb sense pairs are also troponymy pairs in reversed direction.
      * 2c.3.4 All holonymy sense pairs are meronymy pairs in reverse direction.    
    
    Parameters
    -----------
    cwn: CwnBase
         The base cwn reference data
    annot_df: Dict[str, pd.DataFrame]
         The imported dataframe from google sheet
    """

    logger.info("In consistency check")
    V = {}
    E = {}
    cwn_data = (V, E)
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    annot = CwnAnnotator(cwn, f"cwn_edit_{timestamp}")
    transform_dataframe(annot, annot_dfs)
    check_flag = check_cwn_data(annot)
    
    return cwn_data, check_flag

def check_cwn_data(annot: CwnAnnotator):
    return False